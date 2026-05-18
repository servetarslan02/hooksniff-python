# Adapted for HookSniff API — matches DeliveryAttempt schema
from datetime import datetime
from typing import Optional

from .common import BaseModel


class MessageAttemptOut(BaseModel):
    id: str
    attempt_number: int = 1
    status_code: Optional[int] = None
    response_body: Optional[str] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
