from typing import TypedDict


class EventData(TypedDict):
	topic: str
	payload: dict
