from typing import Optional

from .common import BaseModel


class EnvironmentVariableIn(BaseModel):
    key: str
    value: str
    is_secret: Optional[bool] = False
