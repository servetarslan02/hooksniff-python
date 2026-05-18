from datetime import datetime
from typing import Any, Optional

from .background_task_status import BackgroundTaskStatus
from .background_task_type import BackgroundTaskType
from .common import BaseModel


class BackgroundTaskOut(BaseModel):
    id: str
    status: BackgroundTaskStatus
    task: BackgroundTaskType
    data: Optional[Any] = None
    updated_at: Optional[datetime] = None
