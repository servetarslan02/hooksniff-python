from datetime import datetime
from typing import Optional

from .common import BaseModel


class StreamOut(BaseModel):
    id: str
    name: Optional[str] = None
    created_at: Optional[datetime] = None
