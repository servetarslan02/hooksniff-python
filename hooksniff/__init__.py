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

__version__ = "1.2.1"

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
