import uuid

from datetime import datetime
from enum import Enum

from sqlalchemy import (
	UUID,
	Boolean,
	DateTime,
	ForeignKey,
	String,
	Text,
	UniqueConstraint,
	func,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Event(Enum):
	signin = "signin"
	signup = "signup"
	sign_out = "sign_out"
	token_refresh = "token_refresh"


class SessionEventLog(BaseModel):
	id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		primary_key=True,
		default=uuid.uuid4
	)
	user_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	device_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("devices.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	event: Mapped[Event] = mapped_column(
		SQLAlchemyEnum(Event, name="session_event_enum"),
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now()
	)
	device = relationship("Device")


class Device(BaseModel):
	id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
	device_type: Mapped[str] = mapped_column(String(50), nullable=False)
	device_name: Mapped[str] = mapped_column(String(50), nullable=False)
	os_version: Mapped[str] = mapped_column(String(50), nullable=False)
	push_token: Mapped[str] = mapped_column(String(100), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
	sessions = relationship(
		"Session",
		back_populates="device",
		cascade="all, delete-orphan",
		passive_deletes=True,
	)
	user_devices = relationship(
		"UserDevice",
		back_populates="device",
		cascade="all, delete-orphan",
		passive_deletes=True
	)
	users = relationship(
		"User",
		secondary="userdevices",
		viewonly=True,
		back_populates="devices"
	)


class UserDevice(BaseModel):
	user_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		primary_key=True,
	)
	device_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("devices.id", ondelete="CASCADE"),
		primary_key=True,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		nullable=False,
	)
	user = relationship("User", back_populates="user_devices")
	device = relationship("Device", back_populates="user_devices")


class Session(BaseModel):
	__table_args__ = (UniqueConstraint("user_id", "device_id", name="uq_user_device"),)
	id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	device_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("devices.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	refresh_token: Mapped[str] = mapped_column(Text, nullable=False)
	expires_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False
	)
	last_activity: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now()
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now()
	)
	user = relationship("User", back_populates="sessions")
	device = relationship("Device", back_populates="sessions")
