from datetime import datetime
from typing import Optional

from .common import BaseModel


class StreamSinkOut(BaseModel):
    id: str
    stream_id: str
    url: Optional[str] = None
    type: Optional[str] = None
    created_at: Optional[datetime] = None
