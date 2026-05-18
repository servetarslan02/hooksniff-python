from datetime import datetime
from typing import Optional

from .common import BaseModel


class IngestSourceOut(BaseModel):
    id: str
    name: str
    url: str
    secret: Optional[str] = None
    config: Optional[dict] = None
    created_at: Optional[datetime] = None
