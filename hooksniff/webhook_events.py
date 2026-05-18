"""
Typed webhook event payloads for HookSniff.

These types represent the structure of webhook event data
that HookSniff sends to your endpoints.
"""

from __future__ import annotations
import typing as t
from datetime import datetime
from dataclasses import dataclass


@dataclass
class WebhookEvent:
    """
    Parsed webhook event from HookSniff.

    Attributes:
        event: Event type name (e.g., "endpoint.created")
        data: Event payload data as a dictionary
        timestamp: ISO 8601 timestamp string
    """
    event: str
    data: t.Dict[str, t.Any]
    timestamp: str

    @property
    def event_type(self) -> str:
        """Alias for `event` — the event type name."""
        return self.event

    def get(self, key: str, default: t.Any = None) -> t.Any:
        """Get a value from the data dict."""
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> t.Any:
        """Access data dict values with bracket notation."""
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists in data dict."""
        return key in self.data


@dataclass
class EndpointCreatedEvent(WebhookEvent):
    """endpoint.created event data."""
    event: str = "endpoint.created"


@dataclass
class EndpointUpdatedEvent(WebhookEvent):
    """endpoint.updated event data."""
    event: str = "endpoint.updated"


@dataclass
class EndpointDeletedEvent(WebhookEvent):
    """endpoint.deleted event data."""
    event: str = "endpoint.deleted"


@dataclass
class EndpointEnabledEvent(WebhookEvent):
    """endpoint.enabled event data."""
    event: str = "endpoint.enabled"


@dataclass
class EndpointDisabledEvent(WebhookEvent):
    """endpoint.disabled event data."""
    event: str = "endpoint.disabled"


@dataclass
class MessageAttemptExhaustedEvent(WebhookEvent):
    """message.attempt.exhausted event data."""
    event: str = "message.attempt.exhausted"


@dataclass
class MessageAttemptFailingEvent(WebhookEvent):
    """message.attempt.failing event data."""
    event: str = "message.attempt.failing"


@dataclass
class MessageAttemptRecoveredEvent(WebhookEvent):
    """message.attempt.recovered event data."""
    event: str = "message.attempt.recovered"


# Map of event type names to their classes
EVENT_TYPE_MAP: t.Dict[str, t.Type[WebhookEvent]] = {
    "endpoint.created": EndpointCreatedEvent,
    "endpoint.updated": EndpointUpdatedEvent,
    "endpoint.deleted": EndpointDeletedEvent,
    "endpoint.enabled": EndpointEnabledEvent,
    "endpoint.disabled": EndpointDisabledEvent,
    "message.attempt.exhausted": MessageAttemptExhaustedEvent,
    "message.attempt.failing": MessageAttemptFailingEvent,
    "message.attempt.recovered": MessageAttemptRecoveredEvent,
}


def parse_webhook_event(data: t.Dict[str, t.Any]) -> WebhookEvent:
    """
    Parse a webhook payload dict into a typed WebhookEvent.

    Args:
        data: Parsed JSON payload with 'event', 'data', and 'timestamp' keys

    Returns:
        Typed WebhookEvent instance (or subclass based on event type)
    """
    event_type = data.get("event", data.get("eventType", ""))
    event_data = data.get("data", {})
    timestamp = data.get("timestamp", "")

    event_class = EVENT_TYPE_MAP.get(event_type, WebhookEvent)
    return event_class(event=event_type, data=event_data, timestamp=timestamp)


__all__ = [
    "WebhookEvent",
    "EndpointCreatedEvent",
    "EndpointUpdatedEvent",
    "EndpointDeletedEvent",
    "EndpointEnabledEvent",
    "EndpointDisabledEvent",
    "MessageAttemptExhaustedEvent",
    "MessageAttemptFailingEvent",
    "MessageAttemptRecoveredEvent",
    "EVENT_TYPE_MAP",
    "parse_webhook_event",
]
