from datetime import datetime
from typing import Optional

from .common import BaseModel


class EnvironmentOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
