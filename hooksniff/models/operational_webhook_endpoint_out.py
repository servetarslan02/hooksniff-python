from datetime import datetime
from typing import Optional

from .common import BaseModel


class OperationalWebhookEndpointOut(BaseModel):
    id: str
    url: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
