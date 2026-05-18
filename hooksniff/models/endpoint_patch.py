# Adapted for HookSniff API
from typing import Any, Dict, List, Optional

from .common import BaseModel


class EndpointPatch(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    allowed_ips: Optional[List[str]] = None
    event_filter: Optional[List[str]] = None
    custom_headers: Optional[Dict[str, Any]] = None
    retry_policy: Optional[Dict[str, Any]] = None
    routing_strategy: Optional[str] = None
    fallback_url: Optional[str] = None
    format: Optional[str] = None
