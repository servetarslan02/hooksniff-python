from datetime import datetime
from typing import Optional

from .common import BaseModel


class EnvironmentVariableOut(BaseModel):
    id: str
    environment_id: str
    key: str
    value: Optional[str] = None
    is_secret: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
