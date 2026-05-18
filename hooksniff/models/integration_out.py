from datetime import datetime
from typing import Optional

from .common import BaseModel


class IntegrationOut(BaseModel):
    id: str
    name: str
    connector_id: Optional[str] = None
    endpoint_id: Optional[str] = None
    config: Optional[dict] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
