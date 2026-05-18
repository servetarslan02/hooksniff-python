from datetime import datetime
from typing import Optional

from .common import BaseModel


class IngestEndpointOut(BaseModel):
    id: str
    source_id: str
    target_url: str
    filters: Optional[dict] = None
    created_at: Optional[datetime] = None
