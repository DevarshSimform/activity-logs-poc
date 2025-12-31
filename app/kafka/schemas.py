from datetime import datetime, timezone
from uuid import uuid4
from typing import Any


class BaseEvent:
    def __init__(
        self,
        *,
        event_type: str,
        actor: dict,
        resource: dict,
        payload: dict,
        request_id: str,
        meta: dict | None = None,
        version: str = "1.0",
    ):
        self.event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "event_version": version,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "actor": actor,
            "resource": resource,
            "payload": payload,
            "meta": meta or {},
        }

    def to_dict(self) -> dict:
        return self.event
