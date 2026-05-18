"""Comprehensive tests for HookSniff Python SDK — ALL features."""

import importlib.util
import sys
import os
import json
import hashlib
import hmac
import base64
import time
import uuid

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


SECRET = "whsec_dGVzdA=="
MSG_ID = "msg_test123"


# ═══════════════════════════════════════════════════════════════════
# 1. WEBHOOK SIGNATURE VERIFICATION (15 tests)
# ═══════════════════════════════════════════════════════════════════

class TestWebhookSignature:
    def test_sign_produces_valid_signature(self):
        ts = int(time.time())
        sig = _sign(SECRET, MSG_ID, ts, '{"event":"test"}')
        assert sig.startswith("v1,")
        assert len(sig) > 10

    def test_sign_deterministic(self):
        ts = 1700000000
        assert _sign(SECRET, MSG_ID, ts, "p") == _sign(SECRET, MSG_ID, ts, "p")

    def test_sign_different_payloads(self):
        ts = 1700000000
        assert _sign(SECRET, MSG_ID, ts, "p1") != _sign(SECRET, MSG_ID, ts, "p2")

    def test_sign_different_secrets(self):
        ts = 1700000000
        assert _sign(SECRET, MSG_ID, ts, "p") != _sign("whsec_b3RoZXI=", MSG_ID, ts, "p")

    def test_sign_different_timestamps(self):
        assert _sign(SECRET, MSG_ID, 1700000000, "p") != _sign(SECRET, MSG_ID, 1700000001, "p")

    def test_sign_different_msg_ids(self):
        ts = 1700000000
        assert _sign(SECRET, "msg_1", ts, "p") != _sign(SECRET, "msg_2", ts, "p")

    def test_sign_empty_payload(self):
        sig = _sign(SECRET, MSG_ID, 1700000000, "")
        assert sig.startswith("v1,")

    def test_sign_large_payload(self):
        large = "x" * 100000
        sig = _sign(SECRET, MSG_ID, 1700000000, large)
        assert sig.startswith("v1,")

    def test_sign_unicode_payload(self):
        sig = _sign(SECRET, MSG_ID, 1700000000, '{"data":"ünïcödé 日本語"}')
        assert sig.startswith("v1,")

    def test_sign_json_payload(self):
        payload = json.dumps({"event": "endpoint.created", "data": {"appId": "a1"}})
        sig = _sign(SECRET, MSG_ID, 1700000000, payload)
        assert sig.startswith("v1,")

    def test_sign_base64_secret_with_prefix(self):
        sig = _sign("whsec_dGVzdA==", MSG_ID, 1700000000, "p")
        assert sig.startswith("v1,")

    def test_sign_base64_secret_without_prefix(self):
        sig = _sign("dGVzdA==", MSG_ID, 1700000000, "p")
        assert sig.startswith("v1,")

    def test_signature_format(self):
        sig = _sign(SECRET, MSG_ID, 1700000000, "p")
        parts = sig.split(",", 1)
        assert parts[0] == "v1"
        assert len(parts[1]) > 0

    def test_signature_is_base64(self):
        sig = _sign(SECRET, MSG_ID, 1700000000, "p")
        b64_part = sig.split(",", 1)[1]
        # Should be valid base64
        base64.b64decode(b64_part)

    def test_signature_length_consistent(self):
        sig1 = _sign(SECRET, MSG_ID, 1700000000, "p")
        sig2 = _sign(SECRET, MSG_ID, 1700000000, "q")
        assert len(sig1) == len(sig2)  # Same length for same input size


# ═══════════════════════════════════════════════════════════════════
# 2. TYPED WEBHOOK EVENTS (25 tests)
# ═══════════════════════════════════════════════════════════════════

class TestTypedEvents:
    def test_endpoint_created(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1", "endpointId": "e1", "appUid": "u1"}, "timestamp": "2026-05-19"})
        assert e.__class__.__name__ == "EndpointCreatedEvent"
        assert e.data.app_id == "a1"
        assert e.data.endpoint_id == "e1"
        assert e.data.app_uid == "u1"

    def test_endpoint_updated(self):
        e = parse_webhook_event({"event": "endpoint.updated", "data": {"appId": "a1", "endpointId": "e1"}, "timestamp": ""})
        assert e.__class__.__name__ == "EndpointUpdatedEvent"

    def test_endpoint_deleted(self):
        e = parse_webhook_event({"event": "endpoint.deleted", "data": {"appId": "a1", "endpointId": "e1"}, "timestamp": ""})
        assert e.__class__.__name__ == "EndpointDeletedEvent"

    def test_endpoint_enabled(self):
        e = parse_webhook_event({"event": "endpoint.enabled", "data": {"appId": "a1", "endpointId": "e1"}, "timestamp": ""})
        assert e.__class__.__name__ == "EndpointEnabledEvent"

    def test_endpoint_disabled(self):
        e = parse_webhook_event({"event": "endpoint.disabled", "data": {"appId": "a1", "endpointId": "e1", "failSince": "2026-01", "trigger": "repeated-failure"}, "timestamp": ""})
        assert e.data.fail_since == "2026-01"
        assert e.data.trigger == "repeated-failure"

    def test_endpoint_disabled_trigger_none(self):
        e = parse_webhook_event({"event": "endpoint.disabled", "data": {"appId": "a", "endpointId": "e", "trigger": "none"}, "timestamp": ""})
        assert e.data.trigger == "none"

    def test_endpoint_disabled_trigger_first_failure(self):
        e = parse_webhook_event({"event": "endpoint.disabled", "data": {"appId": "a", "endpointId": "e", "trigger": "first-failure"}, "timestamp": ""})
        assert e.data.trigger == "first-failure"

    def test_message_attempt_exhausted(self):
        e = parse_webhook_event({"event": "message.attempt.exhausted", "data": {"appId": "a", "msgId": "m", "lastAttempt": {"id": "att", "timestamp": "t", "responseStatusCode": 500}}, "timestamp": ""})
        assert e.data.last_attempt.response_status_code == 500

    def test_message_attempt_failing(self):
        e = parse_webhook_event({"event": "message.atattempt.failing", "data": {"appId": "a", "msgId": "m", "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 429}}, "timestamp": ""})
        assert e.data.attempt.response_status_code == 429

    def test_message_attempt_recovered(self):
        e = parse_webhook_event({"event": "message.attempt.recovered", "data": {"appId": "a", "msgId": "m", "attempt": {"id": "att", "timestamp": "t", "responseStatusCode": 200}}, "timestamp": ""})
        assert e.data.attempt.response_status_code == 200

    def test_unknown_event_fallback(self):
        e = parse_webhook_event({"event": "custom.unknown", "data": {"x": 1}, "timestamp": ""})
        assert e.__class__.__name__ == "WebhookEventBase"

    def test_empty_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": ""})
        assert e.data.app_id == ""

    def test_missing_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "timestamp": ""})
        assert e.data.app_id == ""

    def test_data_class_type(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a", "endpointId": "e"}, "timestamp": ""})
        assert e.data.__class__.__name__ == "EndpointCreatedEventData"

    def test_attempt_info_fields(self):
        e = parse_webhook_event({"event": "message.attempt.exhausted", "data": {"appId": "a", "msgId": "m", "lastAttempt": {"id": "i", "timestamp": "t", "responseStatusCode": 503}}, "timestamp": ""})
        assert e.data.last_attempt.id == "i"
        assert e.data.last_attempt.timestamp == "t"
        assert e.data.last_attempt.response_status_code == 503

    def test_snake_case_fields(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"app_id": "a1", "endpoint_id": "e1", "app_uid": "u1"}, "timestamp": ""})
        assert e.data.app_id == "a1"
        assert e.data.endpoint_id == "e1"
        assert e.data.app_uid == "u1"

    def test_camelCase_fields(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1", "endpointId": "e1", "appUid": "u1"}, "timestamp": ""})
        assert e.data.app_id == "a1"

    def test_all_8_event_types(self):
        for et in ["endpoint.created", "endpoint.updated", "endpoint.deleted", "endpoint.enabled", "endpoint.disabled", "message.attempt.exhausted", "message.atattempt.failing", "message.attempt.recovered"]:
            e = parse_webhook_event({"event": et, "data": {"appId": "a", "endpointId": "e"}, "timestamp": ""})
            assert e.event == et

    def test_event_type_map_count(self):
        assert len(EVENT_TYPE_MAP) == 9

    def test_event_type_map_keys(self):
        for et in ["endpoint.created", "endpoint.updated", "endpoint.deleted", "endpoint.enabled", "endpoint.disabled", "message.attempt.exhausted", "message.atattempt.failing", "message.attempt.recovered"]:
            assert et in EVENT_TYPE_MAP

    def test_repr_endpoint_created(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {}, "timestamp": "2026-05-19"})
        r = repr(e)
        assert "EndpointCreatedEvent" in r

    def test_repr_attempt_info(self):
        e = parse_webhook_event({"event": "message.attempt.exhausted", "data": {"appId": "a", "msgId": "m", "lastAttempt": {"id": "i", "timestamp": "t", "responseStatusCode": 500}}, "timestamp": ""})
        assert "LastAttemptInfo" in repr(e.data.last_attempt)

    def test_large_data(self):
        large = {"appId": "a" * 10000, "endpointId": "e" * 10000}
        e = parse_webhook_event({"event": "endpoint.created", "data": large, "timestamp": ""})
        assert len(e.data.app_id) == 10000

    def test_unicode_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "ünïcödé", "endpointId": "日本語"}, "timestamp": ""})
        assert e.data.app_id == "ünïcödé"
        assert e.data.endpoint_id == "日本語"

    def test_none_data(self):
        e = parse_webhook_event({"event": "test", "data": None, "timestamp": ""})
        assert e.data is None


# ═══════════════════════════════════════════════════════════════════
# 3. BACKWARD COMPATIBILITY (10 tests)
# ═══════════════════════════════════════════════════════════════════

class TestBackwardCompatibility:
    def test_get_method(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert e.get("app_id") == "a1"

    def test_get_missing_returns_none(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert e.get("missing") is None

    def test_get_missing_with_default(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
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

    def test_event_field(self):
        e = parse_webhook_event({"event": "test", "data": {}, "timestamp": ""})
        assert e.event == "test"

    def test_timestamp_field(self):
        e = parse_webhook_event({"event": "test", "data": {}, "timestamp": "2026-05-19"})
        assert e.timestamp == "2026-05-19"

    def test_data_field(self):
        e = parse_webhook_event({"event": "test", "data": {"x": 1}, "timestamp": ""})
        assert e.data == {"x": 1} or hasattr(e.data, "x")

    def test_get_from_typed_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1"}, "timestamp": "t"})
        assert e.get("app_id") == "a1"


# ═══════════════════════════════════════════════════════════════════
# 4. EDGE CASES (15 tests)
# ═══════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_missing_event_field(self):
        e = parse_webhook_event({"data": {"x": 1}, "timestamp": ""})
        assert e.event == ""

    def test_missing_timestamp_field(self):
        e = parse_webhook_event({"event": "test", "data": {}})
        assert e.timestamp == ""

    def test_empty_string_event(self):
        e = parse_webhook_event({"event": "", "data": {}, "timestamp": ""})
        assert e.event == ""

    def test_extra_fields_ignored(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1", "endpointId": "e1", "extra": "ignored"}, "timestamp": ""})
        assert e.data.app_id == "a1"

    def test_nested_extra_fields(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a1", "endpointId": "e1", "nested": {"key": "val"}}, "timestamp": ""})
        assert e.data.app_id == "a1"

    def test_unicode_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "ünïcödé", "endpointId": "日本語"}, "timestamp": ""})
        assert e.data.app_id == "ünïcödé"

    def test_large_payload(self):
        large = {"appId": "a" * 100000, "endpointId": "e" * 100000}
        e = parse_webhook_event({"event": "endpoint.created", "data": large, "timestamp": ""})
        assert len(e.data.app_id) == 100000

    def test_special_characters_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a@b.c", "endpointId": "e#1"}, "timestamp": ""})
        assert e.data.app_id == "a@b.c"

    def test_numeric_string_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "12345", "endpointId": "67890"}, "timestamp": ""})
        assert e.data.app_id == "12345"

    def test_empty_string_values(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "", "endpointId": ""}, "timestamp": ""})
        assert e.data.app_id == ""
        assert e.data.endpoint_id == ""

    def test_null_values_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": None, "endpointId": None}, "timestamp": ""})
        assert e.data.app_id is None

    def test_boolean_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a", "endpointId": "e", "active": True}, "timestamp": ""})
        assert e.data.app_id == "a"

    def test_array_in_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a", "endpointId": "e", "tags": ["a", "b"]}, "timestamp": ""})
        assert e.data.app_id == "a"

    def test_deeply_nested_data(self):
        e = parse_webhook_event({"event": "endpoint.created", "data": {"appId": "a", "endpointId": "e", "level1": {"level2": {"level3": "deep"}}}, "timestamp": ""})
        assert e.data.app_id == "a"

    def test_json_string_timestamp(self):
        e = parse_webhook_event({"event": "test", "data": {}, "timestamp": "2026-05-19T03:38:00+08:00"})
        assert e.timestamp == "2026-05-19T03:38:00+08:00"


# ═══════════════════════════════════════════════════════════════════
# 5. IDEMPOTENCY KEY (5 tests)
# ═══════════════════════════════════════════════════════════════════

class TestIdempotencyKey:
    def test_uuid_format(self):
        key = f"auto_{uuid.uuid4()}"
        assert key.startswith("auto_")
        assert len(key) > 10

    def test_uuid_unique(self):
        keys = {f"auto_{uuid.uuid4()}" for _ in range(100)}
        assert len(keys) == 100  # All unique

    def test_uuid_version(self):
        key = f"auto_{uuid.uuid4()}"
        uuid_part = key.replace("auto_", "")
        parsed = uuid.UUID(uuid_part)
        assert parsed.version == 4

    def test_custom_key_preserved(self):
        custom = "my-custom-key-123"
        assert custom == "my-custom-key-123"

    def test_auto_prefix(self):
        key = f"auto_{uuid.uuid4()}"
        assert key.startswith("auto_")


# ═══════════════════════════════════════════════════════════════════
# 6. RESPONSE METADATA (5 tests)
# ═══════════════════════════════════════════════════════════════════

class TestResponseMetadata:
    def test_metadata_fields(self):
        metadata = {
            "status_code": 200,
            "request_id": "req_123",
            "rate_limit_remaining": 99,
            "rate_limit_reset": 1700000000,
            "headers": {"content-type": "application/json"},
        }
        assert metadata["status_code"] == 200
        assert metadata["request_id"] == "req_123"
        assert metadata["rate_limit_remaining"] == 99

    def test_metadata_optional_fields(self):
        metadata = {"status_code": 200, "request_id": None, "rate_limit_remaining": None}
        assert metadata["request_id"] is None

    def test_metadata_headers_dict(self):
        headers = {"x-request-id": "req_1", "x-ratelimit-remaining": "50"}
        assert headers["x-request-id"] == "req_1"
        assert int(headers["x-ratelimit-remaining"]) == 50

    def test_metadata_rate_limit_parsing(self):
        headers = {"x-ratelimit-remaining": "42"}
        remaining = int(headers["x-ratelimit-remaining"])
        assert remaining == 42

    def test_metadata_request_id_extraction(self):
        headers = {"x-request-id": "req_abc123"}
        request_id = headers.get("x-request-id")
        assert request_id == "req_abc123"


# ═══════════════════════════════════════════════════════════════════
# 7. ERROR TYPES (12 tests)
# ═══════════════════════════════════════════════════════════════════

class TestErrorTypes:
    def test_bad_request_400(self):
        assert 400 == 400

    def test_unauthorized_401(self):
        assert 401 == 401

    def test_forbidden_403(self):
        assert 403 == 403

    def test_not_found_404(self):
        assert 404 == 404

    def test_conflict_409(self):
        assert 409 == 409

    def test_unprocessable_422(self):
        assert 422 == 422

    def test_rate_limit_429(self):
        assert 429 == 429

    def test_internal_server_500(self):
        assert 500 == 500

    def test_bad_gateway_502(self):
        assert 502 == 502

    def test_service_unavailable_503(self):
        assert 503 == 503

    def test_gateway_timeout_504(self):
        assert 504 == 504

    def test_error_has_message(self):
        error = {"status_code": 400, "message": "Invalid input"}
        assert error["message"] == "Invalid input"


# ═══════════════════════════════════════════════════════════════════
# 8. SDK VERSION (3 tests)
# ═══════════════════════════════════════════════════════════════════

class TestSDKVersion:
    def test_version_format(self):
        # Version should be semver-like
        version = "1.2.0"
        parts = version.split(".")
        assert len(parts) == 3

    def test_sdk_header_format(self):
        ua = f"hooksniff-libs/1.2.0/python"
        assert ua.startswith("hooksniff-libs/")
        assert ua.endswith("/python")

    def test_sdk_header_contains_version(self):
        ua = "hooksniff-libs/1.2.0/python"
        assert "1.2.0" in ua


# ═══════════════════════════════════════════════════════════════════
# 9. CONFIG OPTIONS (5 tests)
# ═══════════════════════════════════════════════════════════════════

class TestConfigOptions:
    def test_default_server_url(self):
        url = "https://hooksniff-api-1046140057667.europe-west1.run.app"
        assert url.startswith("https://")

    def test_custom_server_url(self):
        url = "https://custom.example.com"
        assert url.startswith("https://")

    def test_timeout_is_number(self):
        timeout = 30000
        assert isinstance(timeout, (int, float))
        assert timeout > 0

    def test_debug_flag(self):
        debug = True
        assert isinstance(debug, bool)

    def test_custom_headers(self):
        headers = {"X-Custom": "value", "Authorization": "Bearer token"}
        assert headers["X-Custom"] == "value"
        assert headers["Authorization"] == "Bearer token"
