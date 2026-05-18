from typing import List

from .common import BaseModel
from .environment_variable_in import EnvironmentVariableIn


class EnvironmentVariableBulkUpsertIn(BaseModel):
    variables: List[EnvironmentVariableIn]
