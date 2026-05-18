from datetime import datetime
from typing import Optional

from .common import BaseModel


class ApplicationOut(BaseModel):
    id: str
    name: str
    uid: Optional[str] = None
    rate_limit: Optional[int] = None
    created_at: datetime
    updated_at: datetime
