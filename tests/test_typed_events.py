"""Tests for typed webhook events."""

import importlib.util
import sys
import os

# Load webhook_events directly to avoid pydantic dependency
sys.path.insert(0, os.path.dirname(__file__))
spec = importlib.util.spec_from_file_location(
    "webhook_events",
    os.path.join(os.path.dirname(__file__), "..", "hooksniff", "webhook_events.py"),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_webhook_event = mod.parse_webhook_event
EVENT_TYPE_MAP = mod.EVENT_TYPE_MAP


def test_endpoint_created():
    e = parse_webhook_event({
        "event": "endpoint.created",
        "data": {"appId": "a1", "endpointId": "e1", "appUid": "u1"},
        "timestamp": "2026-05-19",
    })
    assert e.__class__.__name__ == "EndpointCreatedEvent"
    assert e.data.__class__.__name__ == "EndpointCreatedEventData"
    assert e.data.app_id == "a1"
    assert e.data.endpoint_id == "e1"
    assert e.data.app_uid == "u1"
    assert e.event == "endpoint.created"
    assert e.timestamp == "2026-05-19"


def test_endpoint_updated():
    e = parse_webhook_event({
        "event": "endpoint.updated",
        "data": {"appId": "a1", "endpointId": "e1"},
        "timestamp": "",
    })
    assert e.__class__.__name__ == "EndpointUpdatedEvent"
    assert e.data.app_id == "a1"


def test_endpoint_deleted():
    e = parse_webhook_event({
        "event": "endpoint.deleted",
        "data": {"appId": "a1", "endpointId": "e1"},
        "timestamp": "",
    })
    assert e.__class__.__name__ == "EndpointDeletedEvent"


def test_endpoint_enabled():
    e = parse_webhook_event({
        "event": "endpoint.enabled",
        "data": {"appId": "a1", "endpointId": "e1"},
        "timestamp": "",
    })
    assert e.__class__.__name__ == "EndpointEnabledEvent"


def test_endpoint_disabled_with_extras():
    e = parse_webhook_event({
        "event": "endpoint.disabled",
        "data": {"appId": "a1", "endpointId": "e1", "failSince": "2026-01", "trigger": "repeated-failure"},
        "timestamp": "",
    })
    assert e.__class__.__name__ == "EndpointDisabledEvent"
    assert e.data.fail_since == "2026-01"
    assert e.data.trigger == "repeated-failure"


def test_message_attempt_exhausted():
    e = parse_webhook_event({
        "event": "message.attempt.exhausted",
        "data": {
            "appId": "a1",
            "msgId": "m1",
            "lastAttempt": {"id": "att", "timestamp": "t", "responseStatusCode": 500},
        },
        "timestamp": "",
    })
    assert e.__class__.__name__ == "MessageAttemptExhaustedEvent"
    assert e.data.msg_id == "m1"
    assert e.data.last_attempt.id == "att"
    assert e.data.last_attempt.response_status_code == 500


def test_message_attempt_failing():
    e = parse_webhook_event({
        "event": "message.attempt.failing",
        "data": {
            "appId": "a1",
            "msgId": "m1",
            "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 429},
        },
        "timestamp": "",
    })
    assert e.__class__.__name__ == "MessageAttemptFailingEvent"
    assert e.data.attempt.response_status_code == 429


def test_message_attempt_recovered():
    e = parse_webhook_event({
        "event": "message.attempt.recovered",
        "data": {
            "appId": "a1",
            "msgId": "m1",
            "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 200},
        },
        "timestamp": "",
    })
    assert e.__class__.__name__ == "MessageAttemptRecoveredEvent"
    assert e.data.attempt.response_status_code == 200


def test_unknown_event_fallback():
    e = parse_webhook_event({
        "event": "custom.unknown",
        "data": {"x": 1},
        "timestamp": "",
    })
    assert e.__class__.__name__ == "WebhookEventBase"
    assert e.data == {"x": 1}


def test_backward_compat_get():
    e = parse_webhook_event({
        "event": "endpoint.created",
        "data": {"appId": "a1", "endpointId": "e1"},
        "timestamp": "t",
    })
    assert e.get("app_id") == "a1"
    assert e["app_id"] == "a1"
    assert "app_id" in e
    assert e.event_type == "endpoint.created"


def test_backward_compat_bracket():
    e = parse_webhook_event({
        "event": "endpoint.created",
        "data": {"appId": "a1", "endpointId": "e1"},
        "timestamp": "t",
    })
    assert e["endpoint_id"] == "e1"


def test_snake_case_fields():
    """Test that camelCase and snake_case both work."""
    e = parse_webhook_event({
        "event": "endpoint.created",
        "data": {"app_id": "a1", "endpoint_id": "e1", "app_uid": "u1"},
        "timestamp": "",
    })
    assert e.data.app_id == "a1"
    assert e.data.endpoint_id == "e1"
    assert e.data.app_uid == "u1"


def test_event_type_map_count():
    assert len(EVENT_TYPE_MAP) == 9  # 8 + 1 typo


def test_all_event_types():
    types = [
        "endpoint.created",
        "endpoint.updated",
        "endpoint.deleted",
        "endpoint.enabled",
        "endpoint.disabled",
        "message.attempt.exhausted",
        "message.atattempt.failing",
        "message.attempt.failing",
        "message.attempt.recovered",
    ]
    for et in types:
        assert et in EVENT_TYPE_MAP, f"Missing {et}"


def test_empty_data():
    e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": ""})
    assert e.data.app_id == ""
    assert e.data.endpoint_id == ""


def test_missing_fields():
    e = parse_webhook_event({"event": "endpoint.created", "timestamp": ""})
    assert e.data.app_id == ""
