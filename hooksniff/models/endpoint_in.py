# Adapted for HookSniff API — matches CreateEndpointRequest
# NOTE: application_id is required by HookSniff API (not in OpenAPI spec)
from typing import Any, Dict, List, Optional

from .common import BaseModel


class EndpointIn(BaseModel):
    url: str
    application_id: Optional[str] = None
    """Application ID. Required by HookSniff API. Get from /v1/applications"""
    description: Optional[str] = None
    allowed_ips: Optional[List[str]] = None
    event_filter: Optional[List[str]] = None
    custom_headers: Optional[Dict[str, Any]] = None
    retry_policy: Optional[Dict[str, Any]] = None
    routing_strategy: Optional[str] = None
    fallback_url: Optional[str] = None
    format: Optional[str] = "standard"
