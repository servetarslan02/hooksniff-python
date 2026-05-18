from typing import Optional

from .common import BaseModel


class OperationalWebhookEndpointIn(BaseModel):
    url: str
    description: Optional[str] = None
    event_types: Optional[list[str]] = None
