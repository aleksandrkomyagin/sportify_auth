import uuid

from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, UUID, DateTime, String, func, text
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class EventStatus(Enum):
	not_processed = "not_processed"
	processing = "processing"
	processed = "processed"


class OutboxEvent(BaseModel):
	id: Mapped[uuid.UUID] = mapped_column(
		UUID,
		primary_key=True,
		default=uuid.uuid4,
	)
	topic: Mapped[str] = mapped_column(String(100), nullable=False)
	payload: Mapped[dict] = mapped_column(JSON, nullable=False)
	status: Mapped[EventStatus] = mapped_column(
		SQLAlchemyEnum(EventStatus, name="event_status_enum"),
		default=EventStatus.not_processed,
		server_default=text("'not_processed'"),
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
		onupdate=func.now(),
	)
