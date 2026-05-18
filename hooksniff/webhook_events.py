"""
Typed webhook event payloads for HookSniff.

These types represent the structure of webhook event data
that HookSniff sends to your endpoints.
"""

from __future__ import annotations
import typing as t


class WebhookEvent:
    """
    Parsed webhook event from HookSniff.

    Attributes:
        event: Event type name (e.g., "endpoint.created")
        data: Event payload data as a dictionary
        timestamp: ISO 8601 timestamp string
    """

    __slots__ = ("event", "data", "timestamp")

    def __init__(self, event: str, data: t.Dict[str, t.Any], timestamp: str):
        self.event = event
        self.data = data
        self.timestamp = timestamp

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

    def __repr__(self) -> str:
        return f"WebhookEvent(event={self.event!r}, timestamp={self.timestamp!r})"


# Named event type aliases (same class, just for documentation)
EndpointCreatedEvent = WebhookEvent
EndpointUpdatedEvent = WebhookEvent
EndpointDeletedEvent = WebhookEvent
EndpointEnabledEvent = WebhookEvent
EndpointDisabledEvent = WebhookEvent
MessageAttemptExhaustedEvent = WebhookEvent
MessageAttemptFailingEvent = WebhookEvent
MessageAttemptRecoveredEvent = WebhookEvent

# Map of event type names to their classes
EVENT_TYPE_MAP: t.Dict[str, t.Type[WebhookEvent]] = {
    "endpoint.created": WebhookEvent,
    "endpoint.updated": WebhookEvent,
    "endpoint.deleted": WebhookEvent,
    "endpoint.enabled": WebhookEvent,
    "endpoint.disabled": WebhookEvent,
    "message.attempt.exhausted": WebhookEvent,
    "message.attempt.failing": WebhookEvent,
    "message.attempt.recovered": WebhookEvent,
}


def parse_webhook_event(data: t.Dict[str, t.Any]) -> WebhookEvent:
    """
    Parse a webhook payload dict into a typed WebhookEvent.

    Args:
        data: Parsed JSON payload with 'event', 'data', and 'timestamp' keys

    Returns:
        WebhookEvent instance
    """
    event_type = data.get("event", data.get("eventType", ""))
    event_data = data.get("data", {})
    timestamp = data.get("timestamp", "")

    return WebhookEvent(event=event_type, data=event_data, timestamp=timestamp)


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
