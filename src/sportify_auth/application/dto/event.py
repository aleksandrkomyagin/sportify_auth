from uuid import UUID

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OutboxEventDTO:
    id: UUID
    topic: str
    payload: dict
    created_at: datetime
    updated_at: datetime
    status: str


@dataclass
class NewOutboxEventDTO:
    topic: str
    payload: dict
