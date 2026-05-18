from typing import Optional

from .common import BaseModel


class ApplicationIn(BaseModel):
    name: str
    uid: Optional[str] = None
    rate_limit: Optional[int] = None
