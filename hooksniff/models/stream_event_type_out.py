from typing import Optional
from .common import BaseModel


class StreamEventTypeOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
