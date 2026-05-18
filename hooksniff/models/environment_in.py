from typing import Optional

from .common import BaseModel


class EnvironmentIn(BaseModel):
    name: str
    description: Optional[str] = None
