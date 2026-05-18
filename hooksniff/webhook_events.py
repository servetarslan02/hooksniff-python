"""
Typed webhook event payloads for HookSniff.

Each event type has a specific data class with typed fields.
Backward compatible: WebhookEventBase still works with dict-style access.
"""

from __future__ import annotations
import typing as t


# ─── Event Data Classes ─────────────────────────────────────────────

class EndpointCreatedEventData:
    """Data payload for endpoint.created event."""
    __slots__ = ("app_id", "endpoint_id", "app_uid")

    def __init__(self, app_id: str, endpoint_id: str, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.endpoint_id = endpoint_id
        self.app_uid = app_uid


class EndpointUpdatedEventData:
    """Data payload for endpoint.updated event."""
    __slots__ = ("app_id", "endpoint_id", "app_uid")

    def __init__(self, app_id: str, endpoint_id: str, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.endpoint_id = endpoint_id
        self.app_uid = app_uid


class EndpointDeletedEventData:
    """Data payload for endpoint.deleted event."""
    __slots__ = ("app_id", "endpoint_id", "app_uid")

    def __init__(self, app_id: str, endpoint_id: str, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.endpoint_id = endpoint_id
        self.app_uid = app_uid


class EndpointEnabledEventData:
    """Data payload for endpoint.enabled event."""
    __slots__ = ("app_id", "endpoint_id", "app_uid")

    def __init__(self, app_id: str, endpoint_id: str, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.endpoint_id = endpoint_id
        self.app_uid = app_uid


class EndpointDisabledEventData:
    """Data payload for endpoint.disabled event."""
    __slots__ = ("app_id", "endpoint_id", "app_uid", "fail_since", "trigger")

    def __init__(
        self,
        app_id: str,
        endpoint_id: str,
        app_uid: t.Optional[str] = None,
        fail_since: t.Optional[str] = None,
        trigger: t.Optional[str] = None,
    ):
        self.app_id = app_id
        self.endpoint_id = endpoint_id
        self.app_uid = app_uid
        self.fail_since = fail_since
        self.trigger = trigger


class LastAttemptInfo:
    """Info about the last delivery attempt."""
    __slots__ = ("id", "timestamp", "response_status_code")

    def __init__(self, id: str, timestamp: str, response_status_code: int):
        self.id = id
        self.timestamp = timestamp
        self.response_status_code = response_status_code


class AttemptInfo:
    """Info about a delivery attempt."""
    __slots__ = ("id", "timestamp", "response_status_code")

    def __init__(self, id: str, timestamp: str, response_status_code: int):
        self.id = id
        self.timestamp = timestamp
        self.response_status_code = response_status_code


class MessageAttemptExhaustedEventData:
    """Data payload for message.attempt.exhausted event."""
    __slots__ = ("app_id", "msg_id", "last_attempt", "app_uid")

    def __init__(self, app_id: str, msg_id: str, last_attempt: LastAttemptInfo, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.msg_id = msg_id
        self.last_attempt = last_attempt
        self.app_uid = app_uid


class MessageAttemptFailingEventData:
    """Data payload for message.attempt.failing event."""
    __slots__ = ("app_id", "msg_id", "attempt", "app_uid")

    def __init__(self, app_id: str, msg_id: str, attempt: AttemptInfo, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.msg_id = msg_id
        self.attempt = attempt
        self.app_uid = app_uid


class MessageAttemptRecoveredEventData:
    """Data payload for message.attempt.recovered event."""
    __slots__ = ("app_id", "msg_id", "attempt", "app_uid")

    def __init__(self, app_id: str, msg_id: str, attempt: AttemptInfo, app_uid: t.Optional[str] = None):
        self.app_id = app_id
        self.msg_id = msg_id
        self.attempt = attempt
        self.app_uid = app_uid


# ─── Event Classes ──────────────────────────────────────────────────

# Typed event data aliases for type checkers
EndpointCreatedData = EndpointCreatedEventData
EndpointUpdatedData = EndpointUpdatedEventData
EndpointDeletedData = EndpointDeletedEventData
EndpointEnabledData = EndpointEnabledEventData
EndpointDisabledData = EndpointDisabledEventData
MessageAttemptExhaustedData = MessageAttemptExhaustedEventData
MessageAttemptFailingData = MessageAttemptFailingEventData
MessageAttemptRecoveredData = MessageAttemptRecoveredEventData

# Backward-compatible aliases (same class, for documentation)
EndpointCreatedEvent = WebhookEventBase = None  # replaced below


class WebhookEventBase:
    """
    Parsed webhook event from HookSniff.

    Attributes:
        event: Event type name (e.g., "endpoint.created")
        data: Event payload — either a typed data class or raw dict
        timestamp: ISO 8601 timestamp string
    """

    __slots__ = ("event", "data", "timestamp")

    def __init__(self, event: str, data: t.Any, timestamp: str):
        self.event = event
        self.data = data
        self.timestamp = timestamp

    @property
    def event_type(self) -> str:
        """Alias for `event` — the event type name."""
        return self.event

    def get(self, key: str, default: t.Any = None) -> t.Any:
        """Get a value from the data (dict or typed object)."""
        if isinstance(self.data, dict):
            return self.data.get(key, default)
        return getattr(self.data, key, default)

    def __getitem__(self, key: str) -> t.Any:
        if isinstance(self.data, dict):
            return self.data[key]
        return getattr(self.data, key)

    def __contains__(self, key: str) -> bool:
        if isinstance(self.data, dict):
            return key in self.data
        return hasattr(self.data, key)

    def __repr__(self) -> str:
        return f"WebhookEvent(event={self.event!r}, timestamp={self.timestamp!r})"


# Typed event subclasses — same structure, data field is typed
class EndpointCreatedEvent(WebhookEventBase):
    """Webhook event: endpoint.created — data is EndpointCreatedEventData"""
    pass

class EndpointUpdatedEvent(WebhookEventBase):
    """Webhook event: endpoint.updated — data is EndpointUpdatedEventData"""
    pass

class EndpointDeletedEvent(WebhookEventBase):
    """Webhook event: endpoint.deleted — data is EndpointDeletedEventData"""
    pass

class EndpointEnabledEvent(WebhookEventBase):
    """Webhook event: endpoint.enabled — data is EndpointEnabledEventData"""
    pass

class EndpointDisabledEvent(WebhookEventBase):
    """Webhook event: endpoint.disabled — data is EndpointDisabledEventData"""
    pass

class MessageAttemptExhaustedEvent(WebhookEventBase):
    """Webhook event: message.attempt.exhausted — data is MessageAttemptExhaustedEventData"""
    pass

class MessageAttemptFailingEvent(WebhookEventBase):
    """Webhook event: message.attempt.failing — data is MessageAttemptFailingEventData"""
    pass

class MessageAttemptRecoveredEvent(WebhookEventBase):
    """Webhook event: message.attempt.recovered — data is MessageAttemptRecoveredEventData"""
    pass


# ─── Union Type ─────────────────────────────────────────────────────

WebhookEvent = t.Union[
    EndpointCreatedEvent,
    EndpointUpdatedEvent,
    EndpointDeletedEvent,
    EndpointEnabledEvent,
    EndpointDisabledEvent,
    MessageAttemptExhaustedEvent,
    MessageAttemptFailingEvent,
    MessageAttemptRecoveredEvent,
    WebhookEventBase,
]

# ─── Event Type Map ─────────────────────────────────────────────────

EVENT_TYPE_MAP: dict[str, type[WebhookEventBase]] = {
    "endpoint.created": EndpointCreatedEvent,
    "endpoint.updated": EndpointUpdatedEvent,
    "endpoint.deleted": EndpointDeletedEvent,
    "endpoint.enabled": EndpointEnabledEvent,
    "endpoint.disabled": EndpointDisabledEvent,
    "message.attempt.exhausted": MessageAttemptExhaustedEvent,
    "message.atattempt.failing": MessageAttemptFailingEvent,
    "message.attempt.failing": MessageAttemptFailingEvent,
    "message.attempt.recovered": MessageAttemptRecoveredEvent,
}


# ─── Parsing ────────────────────────────────────────────────────────

def _parse_last_attempt(raw: dict[str, t.Any]) -> LastAttemptInfo:
    return LastAttemptInfo(
        id=raw.get("id", ""),
        timestamp=raw.get("timestamp", ""),
        response_status_code=raw.get("responseStatusCode", raw.get("response_status_code", 0)),
    )


def _parse_attempt(raw: dict[str, t.Any]) -> AttemptInfo:
    return AttemptInfo(
        id=raw.get("id", ""),
        timestamp=raw.get("timestamp", ""),
        response_status_code=raw.get("responseStatusCode", raw.get("response_status_code", 0)),
    )


def _parse_event_data(event_type: str, raw_data: dict[str, t.Any]) -> t.Any:
    """Parse raw data dict into the appropriate typed data class."""
    if event_type == "endpoint.created":
        return EndpointCreatedEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            endpoint_id=raw_data.get("endpointId", raw_data.get("endpoint_id", "")),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type == "endpoint.updated":
        return EndpointUpdatedEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            endpoint_id=raw_data.get("endpointId", raw_data.get("endpoint_id", "")),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type == "endpoint.deleted":
        return EndpointDeletedEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            endpoint_id=raw_data.get("endpointId", raw_data.get("endpoint_id", "")),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type == "endpoint.enabled":
        return EndpointEnabledEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            endpoint_id=raw_data.get("endpointId", raw_data.get("endpoint_id", "")),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type == "endpoint.disabled":
        return EndpointDisabledEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            endpoint_id=raw_data.get("endpointId", raw_data.get("endpoint_id", "")),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
            fail_since=raw_data.get("failSince", raw_data.get("fail_since")),
            trigger=raw_data.get("trigger"),
        )
    elif event_type == "message.attempt.exhausted":
        return MessageAttemptExhaustedEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            msg_id=raw_data.get("msgId", raw_data.get("msg_id", "")),
            last_attempt=_parse_last_attempt(raw_data.get("lastAttempt", raw_data.get("last_attempt", {}))),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type in ("message.attempt.failing", "message.atattempt.failing"):
        return MessageAttemptFailingEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            msg_id=raw_data.get("msgId", raw_data.get("msg_id", "")),
            attempt=_parse_attempt(raw_data.get("attempt", {})),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    elif event_type == "message.attempt.recovered":
        return MessageAttemptRecoveredEventData(
            app_id=raw_data.get("appId", raw_data.get("app_id", "")),
            msg_id=raw_data.get("msgId", raw_data.get("msg_id", "")),
            attempt=_parse_attempt(raw_data.get("attempt", {})),
            app_uid=raw_data.get("appUid", raw_data.get("app_uid")),
        )
    return raw_data


def parse_webhook_event(data: dict[str, t.Any]) -> WebhookEvent:
    """
    Parse a webhook payload dict into a typed WebhookEvent.

    Args:
        data: Parsed JSON payload with 'event', 'data', and 'timestamp' keys

    Returns:
        Typed WebhookEvent subclass instance with typed .data attribute
    """
    event_type = data.get("event", data.get("eventType", ""))
    raw_data = data.get("data", {})
    timestamp = data.get("timestamp", "")

    parsed_data = _parse_event_data(event_type, raw_data)

    event_cls = EVENT_TYPE_MAP.get(event_type, WebhookEventBase)
    return event_cls(event=event_type, data=parsed_data, timestamp=timestamp)


__all__ = [
    # Base
    "WebhookEventBase",
    # Data classes
    "EndpointCreatedEventData",
    "EndpointUpdatedEventData",
    "EndpointDeletedEventData",
    "EndpointEnabledEventData",
    "EndpointDisabledEventData",
    "MessageAttemptExhaustedEventData",
    "MessageAttemptFailingEventData",
    "MessageAttemptRecoveredEventData",
    "LastAttemptInfo",
    "AttemptInfo",
    # Event classes
    "EndpointCreatedEvent",
    "EndpointUpdatedEvent",
    "EndpointDeletedEvent",
    "EndpointEnabledEvent",
    "EndpointDisabledEvent",
    "MessageAttemptExhaustedEvent",
    "MessageAttemptFailingEvent",
    "MessageAttemptRecoveredEvent",
    # Union & Map
    "WebhookEvent",
    "EVENT_TYPE_MAP",
    # Functions
    "parse_webhook_event",
]
