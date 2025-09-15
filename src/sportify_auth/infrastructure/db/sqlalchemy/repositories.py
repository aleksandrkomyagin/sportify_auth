from datetime import datetime, timedelta, timezone
from logging import getLogger

from sqlalchemy import and_, delete, func, insert, or_, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from sportify_auth.application.dto.event import OutboxEventDTO
from sportify_auth.application.dto.session import (
	DeviceIdDTO,
	DeviceInfoDTO,
	SessionDTO,
	SessionIdDTO,
)
from sportify_auth.application.protocols.repositories import (
	ISessionRepository,
	IUserRepository,
)
from sportify_auth.application.protocols.repositories.outbox_event.outbox_repository import (
	IOutboxRepository,
)
from sportify_auth.application.protocols.repositories.outbox_event.types import EventData
from sportify_auth.application.protocols.repositories.session.types import (
	DeviceData,
	SessionData,
	SessionEvent,
)
from sportify_auth.application.protocols.repositories.user.types import (
	UpdateUserData,
	UserData,
)
from sportify_auth.domain.entities import User
from sportify_auth.domain.value_objects import IsActive, Phone, UserUUID
from sportify_auth.infrastructure.db.sqlalchemy.decorators import db_operation
from sportify_auth.infrastructure.db.sqlalchemy.models import (
	Device,
	OutboxEvent,
	Session,
	SessionEventLog,
	UserDevice,
	UserModel,
	UserStatusHistory,
)

logger = getLogger(__name__)


class SQLAlchemyUserRepository(IUserRepository):
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	@db_operation
	async def create_user(self, user_data: UserData) -> UserUUID:
		history_data: list[dict] = user_data.pop("status_history")
		stmt = insert(UserModel).values(**user_data).returning(UserModel.id)
		result = await self.session.execute(stmt)
		user_id = result.scalar_one()
		if history_data:
			stmt = insert(UserStatusHistory).values(history_data)
			await self.session.execute(stmt)
		return UserUUID(str(user_id))

	@db_operation
	async def get_user_by_id(self, user_id: str) -> User | None:
		stmt = select(UserModel).where(UserModel.id == user_id)
		result = await self.session.scalar(stmt)
		if not result:
			return None
		return User(
			id=UserUUID(str(result.id)),
			phone=Phone(result.phone),
			created_at=result.created_at,
			is_active=IsActive(result.is_active),
		)

	@db_operation
	async def get_user_by_phone(self, phone: str) -> User | None:
		stmt = select(UserModel).where(UserModel.phone == phone)
		result = await self.session.scalar(stmt)
		if not result:
			return None
		return User(
			id=UserUUID(str(result.id)),
			phone=Phone(result.phone),
			created_at=result.created_at,
			is_active=IsActive(result.is_active),
		)

	@db_operation
	async def delete_user(self, user_id: str) -> None:
		current_device_ids_before_deleting_result = await self.session.execute(
			select(UserDevice.device_id).where(UserDevice.user_id == user_id)
		)
		await self.session.execute(delete(UserModel).where(UserModel.id == user_id))
		current_device_ids_before_deleting = current_device_ids_before_deleting_result.scalars().all()
		count_stmt = (
			select(UserDevice.device_id)
			.where(UserDevice.device_id.in_(current_device_ids_before_deleting))
			.group_by(UserDevice.device_id)
		)
		current_device_ids_after_deleting_result = await self.session.execute(count_stmt)
		devices_with_users = {row for row in current_device_ids_after_deleting_result.scalars().all()}
		devices_to_delete = list(set(current_device_ids_before_deleting) - devices_with_users)
		if devices_to_delete:
			stmt = (
				update(Device)
				.where(Device.id.in_(devices_to_delete))
				.values(
					is_deleted=True,
					deleted_at=func.now(),
				)
			)
			await self.session.execute(stmt)

	@db_operation
	async def update_user(
		self,
		user_id: str,
		user_data: UpdateUserData,
		status_history: list[dict] | None = None,
	) -> UserUUID:
		stmt = (
			update(UserModel)
			.where(UserModel.id == user_id)
			.values(dict(user_data))
			.returning(UserModel.id)
		)
		result = await self.session.execute(stmt)
		user_id = result.scalar_one_or_none()
		if status_history:
			status_stmt = insert(UserStatusHistory).values(status_history)
			await self.session.execute(status_stmt)
		return UserUUID(str(user_id))


class SQLAlchemyOutboxRepository(IOutboxRepository):
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	@db_operation
	async def create_event(self, event: EventData) -> None:
		insert_stmt = insert(OutboxEvent).values(**event).returning(OutboxEvent.id)
		await self.session.execute(insert_stmt)

	@db_operation
	async def get_events(self, limit: int = 100) -> list[OutboxEventDTO]:
		timeout_threshold = datetime.now(timezone.utc) - timedelta(minutes=2)
		select_stmt = (
			select(OutboxEvent)
			.where(
				or_(
					OutboxEvent.status == "not_processed",
					and_(
						OutboxEvent.status == "processing",
						OutboxEvent.updated_at <= timeout_threshold,
					),
				)
			)
			.order_by(OutboxEvent.created_at)
			.limit(limit)
			.with_for_update(skip_locked=True)
		)
		async with self.session.begin():
			result = await self.session.execute(select_stmt)
			events = result.scalars().all()
			ids = [event.id for event in events]

			update_stmt = (
				update(OutboxEvent)
				.where(OutboxEvent.id.in_(ids))
				.values(
					status="processing",
					updated_at=func.now(),
				)
				.returning(OutboxEvent)
			)

			result = await self.session.execute(update_stmt)
			events = result.scalars().all()

		return [
			OutboxEventDTO(
				id=event.id,
				topic=event.topic,
				payload=event.payload,
				created_at=event.created_at,
				updated_at=event.updated_at,
				status=str(event.status),
			)
			for event in events
		]

	@db_operation
	async def update_events(self, event_ids: list[int], status: str) -> None:
		update_stmt = (
			update(OutboxEvent)
			.where(OutboxEvent.id.in_(event_ids))
			.values(
				status=status,
				updated_at=func.now(),
			)
		)
		async with self.session.begin():
			await self.session.execute(update_stmt)


class SQLAlchemySessionRepository(ISessionRepository):
	def __init__(self, session: AsyncSession) -> None:
		self.session = session

	@db_operation
	async def upsert_session(self, session_data: SessionData) -> SessionDTO:
		stmt = (
			pg_insert(Session)
			.values(**session_data)
			.on_conflict_do_update(
				constraint="uq_user_device",
				set_={
					"refresh_token": session_data["refresh_token"],
					"expires_at": session_data["expires_at"],
				},
			)
			.returning(Session)
		)

		result = await self.session.execute(stmt)
		session = result.scalar_one()

		return SessionDTO(
			session_id=str(session.id),
			user_id=str(session.user_id),
			device_id=str(session.device_id),
			refresh_token=session.refresh_token,
			expires_at=session.expires_at,
			last_activity=session.last_activity,
			created_at=session.created_at,
		)

	@db_operation
	async def delete_session(
		self, session_ids: list[str], delete_devices: bool
	) -> tuple[list[SessionIdDTO], list[DeviceIdDTO]]:
		stmt = delete(Session).where(Session.id.in_(session_ids)).returning(Session.device_id)
		result = await self.session.execute(stmt)
		device_ids = result.scalars().all()
		deleted_device_ids = []

		if delete_devices:
			await self.session.execute(
				delete(UserDevice).where(UserDevice.device_id.in_(device_ids))
			)
			count_stmt = (
				select(UserDevice.device_id)
				.where(UserDevice.device_id.in_(device_ids))
				.group_by(UserDevice.device_id)
			)
			result = await self.session.execute(count_stmt)
			devices_with_users = {row for row in result.scalars().all()}
			devices_to_delete = list(set(device_ids) - devices_with_users)
			if devices_to_delete:
				stmt = (
					update(Device)
					.where(Device.id.in_(devices_to_delete))
					.values(
						is_deleted=True,
						deleted_at=func.now(),
					)
				)
				await self.session.execute(stmt)
				deleted_device_ids = devices_to_delete

		return (
			[SessionIdDTO(session_id) for session_id in session_ids],
			[DeviceIdDTO(str(device_id)) for device_id in deleted_device_ids],
		)

	@db_operation
	async def add_device(self, device_data: DeviceData) -> DeviceInfoDTO:
		stmt = insert(Device).values(**device_data).returning(Device)
		result = await self.session.execute(stmt)
		device = result.scalar_one()

		return DeviceInfoDTO(
			device_id=str(device.id),
			device_type=device.device_type,
			device_name=device.device_name,
			os_version=device.os_version,
			push_token=device.push_token,
			created_at=device.created_at,
		)

	@db_operation
	async def attach_device_to_user(self, device_id: str, user_id: str) -> None:
		await self.session.execute(
			insert(UserDevice).values(**{"user_id": user_id, "device_id": device_id})
		)

	@db_operation
	async def get_device_by_id(self, device_id: str) -> DeviceInfoDTO | None:
		stmt = select(Device).where(Device.id == device_id)
		result = await self.session.execute(stmt)
		device = result.scalar()
		if not device:
			return None
		if device.is_deleted:
			stmt = (
				update(Device)
				.where(Device.id == device_id)
				.values(
					is_deleted=False,
					deleted_at=None,
				)
			)
			await self.session.execute(stmt)
		return DeviceInfoDTO(
			device_id=str(device.id),
			device_name=device.device_name,
			device_type=device.device_type,
			os_version=device.os_version,
			push_token=device.push_token,
			created_at=device.created_at,
		)

	@db_operation
	async def log_event(self, events: list[SessionEvent]) -> None:
		stmt = insert(SessionEventLog).values(events)
		await self.session.execute(stmt)
