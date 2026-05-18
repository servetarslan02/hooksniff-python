"""
HookSniff Python SDK

Usage:
    from hooksniff import HookSniff, HookSniffOptions

    hs = HookSniff("hooksniff_xxx")
    endpoints = hs.endpoint.list()

    from hooksniff import Webhook
    wh = Webhook("whsec_...")
    payload = wh.verify(raw_body, headers)
"""

from .api.hooksniff import HookSniff, HookSniffAsync, HookSniffOptions, DEFAULT_SERVER_URL
from .api.pagination import ListResponse, AsyncListResponse, build_list_response
from .webhooks import Webhook, WebhookVerificationError
from .webhook_events import (
    WebhookEvent,
    EndpointCreatedEvent,
    EndpointUpdatedEvent,
    EndpointDeletedEvent,
    EndpointEnabledEvent,
    EndpointDisabledEvent,
    MessageAttemptExhaustedEvent,
    MessageAttemptFailingEvent,
    MessageAttemptRecoveredEvent,
    parse_webhook_event,
)
from .api.common import ResponseMetadata
from .exceptions import (
    HookSniffError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    UnprocessableEntityError,
    RateLimitError,
    InternalServerError,
    BadGatewayError,
    ServiceUnavailableError,
    GatewayTimeoutError,
    HttpError,
    HTTPValidationError,
)

__version__ = '1.2.2'

__all__ = [
    "HookSniff",
    "HookSniffAsync",
    "HookSniffOptions",
    "DEFAULT_SERVER_URL",
    "ListResponse",
    "AsyncListResponse",
    "build_list_response",
    "Webhook",
    "WebhookVerificationError",
    "WebhookEvent",
    "EndpointCreatedEvent",
    "EndpointUpdatedEvent",
    "EndpointDeletedEvent",
    "EndpointEnabledEvent",
    "EndpointDisabledEvent",
    "MessageAttemptExhaustedEvent",
    "MessageAttemptFailingEvent",
    "MessageAttemptRecoveredEvent",
    "parse_webhook_event",
    "HookSniffError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "BadGatewayError",
    "ServiceUnavailableError",
    "GatewayTimeoutError",
    "HttpError",
    "HTTPValidationError",
]
