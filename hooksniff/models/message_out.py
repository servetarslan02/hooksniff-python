# Adapted for HookSniff API — matches Delivery schema
from datetime import datetime
from typing import Optional

from .common import BaseModel


class MessageOut(BaseModel):
    id: str
    endpoint_id: str
    event: Optional[str] = None
    status: str = "pending"
    attempt_count: int = 0
    response_status: Optional[int] = None
    replay_count: int = 0
    created_at: datetime
