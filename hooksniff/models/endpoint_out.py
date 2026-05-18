# Adapted for HookSniff API — matches /v1/endpoints response
from datetime import datetime
from typing import Any, Dict, List, Optional

from .common import BaseModel


class EndpointOut(BaseModel):
    id: str
    url: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    allowed_ips: Optional[List[str]] = None
    event_filter: Optional[List[str]] = None
    custom_headers: Optional[Dict[str, Any]] = None
    routing_strategy: str = "round-robin"
    fallback_url: Optional[str] = None
    avg_response_ms: int = 0
    failure_streak: int = 0
    format: str = "standard"
    application_id: Optional[str] = None
