"""
HookSniff Python SDK - Webhook infrastructure for developers.

Usage:
    from hooksniff import HookSniff

    hs = HookSniff("hr_live_...")

    # Create application
    app = hs.application.create(name="My App")

    # Create endpoint
    ep = hs.endpoint.create(url="https://app.com/webhook", application_id=app["id"])

    # Send webhook
    delivery = hs.webhook.send(endpoint_id=ep["id"], event="order.created", data={"id": "123"})
"""

from .client import HookSniff
from .webhook import Webhook, WebhookVerificationError
from .exceptions import (
    HookSniffError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    ServerError,
)

__version__ = "0.4.3"
__all__ = [
    "HookSniff",
    "Webhook",
    "WebhookVerificationError",
    "HookSniffError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
]
