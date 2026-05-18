import typing as t
from datetime import datetime
from standardwebhooks.webhooks import Webhook as StdWh
from standardwebhooks.exceptions import WebhookVerificationError

from .webhook_events import WebhookEvent, parse_webhook_event


class Webhook:
    _inner: StdWh

    def __init__(self, whsecret: t.Union[str, bytes]):
        self._inner = StdWh(whsecret)

    def verify(self, data: t.Union[bytes, str], headers: t.Dict[str, str]) -> WebhookEvent:
        """
        Verify and parse a webhook payload.

        Verifies the HMAC-SHA256 signature, then parses the payload
        into a typed WebhookEvent with `event`, `data`, and `timestamp`.

        Args:
            data: Raw request body (bytes or str)
            headers: Request headers containing hooksniff-id, hooksniff-timestamp, hooksniff-signature

        Returns:
            Parsed WebhookEvent with typed fields

        Raises:
            WebhookVerificationError: If signature is invalid or timestamp is outside tolerance
        """
        headers = {k.lower(): v for k, v in headers.items()}

        headers["webhook-id"] = headers.get("hooksniff-id", headers.get("webhook-id", ""))
        headers["webhook-signature"] = headers.get(
            "hooksniff-signature", headers.get("webhook-signature", "")
        )
        headers["webhook-timestamp"] = headers.get(
            "hooksniff-timestamp", headers.get("webhook-timestamp", "")
        )

        raw = self._inner.verify(data, headers)

        if isinstance(raw, (bytes, bytearray)):
            import json
            raw = json.loads(raw)

        if isinstance(raw, dict):
            return parse_webhook_event(raw)

        if isinstance(raw, str):
            import json
            return parse_webhook_event(json.loads(raw))

        return parse_webhook_event(raw)

    def verify_raw(self, data: t.Union[bytes, str], headers: t.Dict[str, str]) -> t.Any:
        """
        Verify and return raw payload without parsing.
        Use this when you need the raw JSON instead of a typed event.
        """
        headers = {k.lower(): v for k, v in headers.items()}

        headers["webhook-id"] = headers.get("hooksniff-id", headers.get("webhook-id", ""))
        headers["webhook-signature"] = headers.get(
            "hooksniff-signature", headers.get("webhook-signature", "")
        )
        headers["webhook-timestamp"] = headers.get(
            "hooksniff-timestamp", headers.get("webhook-timestamp", "")
        )

        return self._inner.verify(data, headers)

    def sign(self, msg_id: str, timestamp: datetime, data: str) -> str:
        return self._inner.sign(msg_id, timestamp, data)


__all__ = ["Webhook", "WebhookVerificationError"]
