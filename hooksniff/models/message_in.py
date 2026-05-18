# Adapted for HookSniff API — matches CreateWebhookRequest
from typing import Any, Dict, Optional

from .common import BaseModel


class MessageIn(BaseModel):
    endpoint_id: str
    """Target endpoint ID."""

    event: Optional[str] = None
    """Event type (e.g. "order.created")."""

    data: Dict[str, Any]
    """Webhook payload."""
