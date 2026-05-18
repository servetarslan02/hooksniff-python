from datetime import datetime
from typing import Optional

from .common import BaseModel


class OperationalWebhookDeliveryOut(BaseModel):
    id: str
    endpoint_id: str
    event_type: Optional[str] = None
    status: str
    response_status: Optional[int] = None
    created_at: Optional[datetime] = None
