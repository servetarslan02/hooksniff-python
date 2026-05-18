from typing import Any, Optional

from .common import BaseModel


class ConnectorOut(BaseModel):
    id: str
    name: str
    type: Optional[str] = None
    config_schema: Optional[Any] = None
