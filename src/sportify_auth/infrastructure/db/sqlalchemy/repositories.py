from datetime import datetime, timedelta

from sqlalchemy import delete, insert, select, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from sportify_auth.application.dto.event import OutboxEventDTO
from sportify_auth.application.protocols.repositories import IUserRepository
from sportify_auth.application.protocols.repositories.outbox_event.types import EventData
from sportify_auth.application.protocols.repositories.user.types import UpdateUserData, UserData
from sportify_auth.application.protocols.repositories.outbox_event.outbox_repository import IOutboxRepository
from sportify_auth.domain.entities import User
from sportify_auth.domain.value_objects import IsActive, Phone, UserUUID
from sportify_auth.infrastructure.db.sqlalchemy.decorators import db_operation
from sportify_auth.infrastructure.db.sqlalchemy.models import OutboxEvent, UserModel, UserStatusHistory


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
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)

    @db_operation
    async def update_user(
        self,
        user_id: str,
        user_data: UpdateUserData,
        status_history: list[dict] | None = None
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
        timeout_threshold = datetime.now() - timedelta(minutes=2)
        select_stmt = (
            select(OutboxEvent)
            .where(
                or_(
                    OutboxEvent.status == "not_processed",
                    and_(
                        OutboxEvent.status == "processing",
                        OutboxEvent.updated_at <= timeout_threshold
                    )
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
                    updated_at=datetime.now(),
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
                updated_at=datetime.now(),
            )
        )
        async with self.session.begin():
            await self.session.execute(update_stmt)
