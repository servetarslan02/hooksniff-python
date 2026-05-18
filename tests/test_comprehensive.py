"""Comprehensive tests for HookSniff Python SDK."""

import importlib.util
import sys
import os
import json
import hashlib
import hmac
import base64
import time

sys.path.insert(0, os.path.dirname(__file__))
spec = importlib.util.spec_from_file_location(
    "webhook_events",
    os.path.join(os.path.dirname(__file__), "..", "hooksniff", "webhook_events.py"),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_webhook_event = mod.parse_webhook_event
EVENT_TYPE_MAP = mod.EVENT_TYPE_MAP


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

def _sign(secret_b64, msg_id, timestamp, payload):
    key = base64.b64decode(secret_b64)
    to_sign = f"{msg_id}.{timestamp}.{payload}"
    sig = base64.b64encode(
        hmac.new(key, to_sign.encode(), hashlib.sha256).digest()
    ).decode()
    return f"v1,{sig}"


SECRET = "whsec_dGVzdA=="  # base64("test")
MSG_ID = "msg_test123"


# ═══════════════════════════════════════════════════════════════════
# 1. WEBHOOK SIGNATURE VERIFICATION
# ═══════════════════════════════════════════════════════════════════

class TestWebhookSignature:
    """Test webhook signature creation and verification."""

    def test_sign_produces_valid_signature(self):
        ts = int(time.time())
        sig = _sign(SECRET, MSG_ID, ts, '{"event":"test"}')
        assert sig.startswith("v1,")
        assert len(sig) > 10

    def test_sign_deterministic(self):
        ts = 1700000000
        sig1 = _sign(SECRET, MSG_ID, ts, "payload")
        sig2 = _sign(SECRET, MSG_ID, ts, "payload")
        assert sig1 == sig2

    def test_sign_different_payloads_differ(self):
        ts = 1700000000
        sig1 = _sign(SECRET, MSG_ID, ts, "payload1")
        sig2 = _sign(SECRET, MSG_ID, ts, "payload2")
        assert sig1 != sig2

    def test_sign_different_secrets_differ(self):
        ts = 1700000000
        sig1 = _sign(SECRET, MSG_ID, ts, "payload")
        sig2 = _sign("whsec_b3RoZXI=", MSG_ID, ts, "payload")
        assert sig1 != sig2

    def test_sign_different_timestamps_differ(self):
        sig1 = _sign(SECRET, MSG_ID, 1700000000, "payload")
        sig2 = _sign(SECRET, MSG_ID, 1700000001, "payload")
        assert sig1 != sig2


# ═══════════════════════════════════════════════════════════════════
# 2. TYPED WEBHOOK EVENTS
# ═══════════════════════════════════════════════════════════════════

class TestTypedEvents:
    """Test all 8 typed webhook event types."""

    def test_endpoint_created(self):
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

    def test_endpoint_updated(self):
        e = parse_webhook_event({
            "event": "endpoint.updated",
            "data": {"appId": "a1", "endpointId": "e1"},
            "timestamp": "",
        })
        assert e.__class__.__name__ == "EndpointUpdatedEvent"
        assert e.data.app_id == "a1"

    def test_endpoint_deleted(self):
        e = parse_webhook_event({
            "event": "endpoint.deleted",
            "data": {"appId": "a1", "endpointId": "e1"},
            "timestamp": "",
        })
        assert e.__class__.__name__ == "EndpointDeletedEvent"

    def test_endpoint_enabled(self):
        e = parse_webhook_event({
            "event": "endpoint.enabled",
            "data": {"appId": "a1", "endpointId": "e1"},
            "timestamp": "",
        })
        assert e.__class__.__name__ == "EndpointEnabledEvent"

    def test_endpoint_disabled_with_extras(self):
        e = parse_webhook_event({
            "event": "endpoint.disabled",
            "data": {"appId": "a1", "endpointId": "e1", "failSince": "2026-01", "trigger": "repeated-failure"},
            "timestamp": "",
        })
        assert e.__class__.__name__ == "EndpointDisabledEvent"
        assert e.data.fail_since == "2026-01"
        assert e.data.trigger == "repeated-failure"

    def test_endpoint_disabled_trigger_values(self):
        for trigger in ["none", "first-failure", "repeated-failure"]:
            e = parse_webhook_event({
                "event": "endpoint.disabled",
                "data": {"appId": "a1", "endpointId": "e1", "trigger": trigger},
                "timestamp": "",
            })
            assert e.data.trigger == trigger

    def test_message_attempt_exhausted(self):
        e = parse_webhook_event({
            "event": "message.attempt.exhausted",
            "data": {
                "appId": "a1", "msgId": "m1",
                "lastAttempt": {"id": "att", "timestamp": "t", "responseStatusCode": 500},
            },
            "timestamp": "",
        })
        assert e.__class__.__name__ == "MessageAttemptExhaustedEvent"
        assert e.data.msg_id == "m1"
        assert e.data.last_attempt.id == "att"
        assert e.data.last_attempt.response_status_code == 500

    def test_message_attempt_failing(self):
        e = parse_webhook_event({
            "event": "message.attempt.failing",
            "data": {
                "appId": "a1", "msgId": "m1",
                "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 429},
            },
            "timestamp": "",
        })
        assert e.data.attempt.response_status_code == 429

    def test_message_attempt_recovered(self):
        e = parse_webhook_event({
            "event": "message.attempt.recovered",
            "data": {
                "appId": "a1", "msgId": "m1",
                "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 200},
            },
            "timestamp": "",
        })
        assert e.data.attempt.response_status_code == 200

    def test_unknown_event_fallback(self):
        e = parse_webhook_event({"event": "custom.unknown", "data": {"x": 1}, "timestamp": ""})
        assert e.__class__.__name__ == "WebhookEventBase"
        assert e.data == {"x": 1}

    def test_empty_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": ""})
        assert e.data.app_id == ""
        assert e.data.endpoint_id == ""

    def test_missing_data_key(self):
        e = parse_webhook_event({"event": "endpoint.created", "timestamp": ""})
        assert e.data.app_id == ""


# ═══════════════════════════════════════════════════════════════════
# 3. BACKWARD COMPATIBILITY
# ═══════════════════════════════════════════════════════════════════

class TestBackwardCompatibility:
    """Test that old dict-style access still works."""

    def test_get_method(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert e.get("app_id") == "a1"
        assert e.get("missing") is None
        assert e.get("missing", "default") == "default"

    def test_bracket_access(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert e["app_id"] == "a1"

    def test_contains(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert "app_id" in e
        assert "missing" not in e

    def test_event_type_alias(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": ""})
        assert e.event_type == "endpoint.created"

    def test_snake_case_fields(self):
        e = parse_webhook_event({
            "event": "endpoint.created",
            "data": {"app_id": "a1", "endpoint_id": "e1", "app_uid": "u1"},
            "timestamp": "",
        })
        assert e.data.app_id == "a1"
        assert e.data.endpoint_id == "e1"
        assert e.data.app_uid == "u1"


# ═══════════════════════════════════════════════════════════════════
# 4. EVENT TYPE MAP
# ═══════════════════════════════════════════════════════════════════

class TestEventTypeMap:
    """Test EVENT_TYPE_MAP completeness."""

    def test_map_count(self):
        assert len(EVENT_TYPE_MAP) == 9

    def test_all_known_types_present(self):
        for et in [
            "endpoint.created", "endpoint.updated", "endpoint.deleted",
            "endpoint.enabled", "endpoint.disabled",
            "message.attempt.exhausted", "message.attempt.failing",
            "message.atattempt.failing", "message.attempt.recovered",
        ]:
            assert et in EVENT_TYPE_MAP, f"Missing {et}"

    def test_map_values_are_classes(self):
        for et, cls in EVENT_TYPE_MAP.items():
            assert isinstance(cls, type), f"{et} value is not a class"


# ═══════════════════════════════════════════════════════════════════
# 5. EDGE CASES
# ═══════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_missing_event_field(self):
        e = parse_webhook_event({"data": {"x": 1}, "timestamp": ""})
        assert e.event == ""

    def test_missing_timestamp_field(self):
        e = parse_webhook_event({"event": "test", "data": {}})
        assert e.timestamp == ""

    def test_none_data(self):
        e = parse_webhook_event({"event": "test", "data": None, "timestamp": ""})
        assert e.data is None

    def test_extra_fields_ignored(self):
        e = parse_webhook_event({
            "event": "endpoint.created",
            "data": {"appId": "a1", "endpointId": "e1", "extra": "ignored"},
            "timestamp": "",
        })
        assert e.data.app_id == "a1"

    def test_nested_extra_fields(self):
        e = parse_webhook_event({
            "event": "endpoint.created",
            "data": {"appId": "a1", "endpointId": "e1", "nested": {"key": "val"}},
            "timestamp": "",
        })
        assert e.data.app_id == "a1"

    def test_unicode_in_data(self):
        e = parse_webhook_event({
            "event": "endpoint.created",
            "data": {"appId": "ünïcödé", "endpointId": "日本語"},
            "timestamp": "",
        })
        assert e.data.app_id == "ünïcödé"
        assert e.data.endpoint_id == "日本語"

    def test_large_payload(self):
        large_data = {"appId": "a" * 10000, "endpointId": "e" * 10000}
        e = parse_webhook_event({"event": "endpoint.created", "data": large_data, "timestamp": ""})
        assert len(e.data.app_id) == 10000

    def test_empty_string_event(self):
        e = parse_webhook_event({"event": "", "data": {}, "timestamp": ""})
        assert e.event == ""
        assert e.__class__.__name__ == "WebhookEventBase"


# ═══════════════════════════════════════════════════════════════════
# 6. DATA CLASS PROPERTIES
# ═══════════════════════════════════════════════════════════════════

class TestDataClasses:
    """Test data class attributes and defaults."""

    def test_endpoint_created_defaults(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a", "endpointId": "e"}, "timestamp": ""})
        assert e.data.app_uid is None

    def test_endpoint_disabled_defaults(self):
        e = parse_webhook_event({"event": "endpoint.disabled", "data": {"appId": "a", "endpointId": "e"}, "timestamp": ""})
        assert e.data.fail_since is None
        assert e.data.trigger is None

    def test_attempt_info_fields(self):
        e = parse_webhook_event({
            "event": "message.attempt.exhausted",
            "data": {"appId": "a", "msgId": "m", "lastAttempt": {"id": "i", "timestamp": "t", "responseStatusCode": 503}},
            "timestamp": "",
        })
        assert e.data.last_attempt.id == "i"
        assert e.data.last_attempt.timestamp == "t"
        assert e.data.last_attempt.response_status_code == 503

    def test_last_attempt_info_repr(self):
        e = parse_webhook_event({
            "event": "message.attempt.exhausted",
            "data": {"appId": "a", "msgId": "m", "lastAttempt": {"id": "i", "timestamp": "t", "responseStatusCode": 500}},
            "timestamp": "",
        })
        r = repr(e.data.last_attempt)
        assert "LastAttemptInfo" in r

    def test_event_repr(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": "2026-05-19"})
        r = repr(e)
        assert "EndpointCreatedEvent" in r
        assert "2026-05-19" in r
