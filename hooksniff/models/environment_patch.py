from typing import Optional

from .common import BaseModel


class EnvironmentPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
