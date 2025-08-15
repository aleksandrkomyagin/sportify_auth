import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Status(Enum):
	activated = "activated"
	deactivated = "deactivated"


class UserStatusHistory(BaseModel):
	id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
	)
	user_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
	)
	status: Mapped[Status] = mapped_column(
		SQLAlchemyEnum(Status, name="user_status_enum"),
		nullable=False,
	)
	timestamp: Mapped[datetime] = mapped_column(
		DateTime,
		nullable=False,
	)
	user = relationship("User", back_populates="status_history")


class User(BaseModel):
	id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True), primary_key=True, unique=True, nullable=False
	)
	phone: Mapped[str] = mapped_column(
		String(11),
		unique=True,
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		nullable=False,
	)
	is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
	status_history = relationship(
		UserStatusHistory,
		back_populates="user",
		cascade="all, delete-orphan",
		passive_deletes=True
	)
