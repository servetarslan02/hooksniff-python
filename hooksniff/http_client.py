import json
import time
import urllib.request
import urllib.error
from typing import Any, Dict, Optional
from .exceptions import map_error, RateLimitError, HookSniffError

DEFAULT_BASE_URL = "https://hooksniff-api-e6ztf3x2ma-ew.a.run.app"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
SDK_VERSION = "0.4.0"


class HttpClient:
    def __init__(self, api_key: str, base_url: str = None, timeout: int = None, retries: int = None, headers: Dict[str, str] = None):
        if not api_key:
            raise ValueError("HookSniff API key is required")
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.retries = retries if retries is not None else DEFAULT_RETRIES
        self.extra_headers = headers or {}

    def request(self, method: str, path: str, body: Any = None, options: Dict[str, str] = None) -> Any:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"hooksniff-sdk/python/{SDK_VERSION}",
            **self.extra_headers,
        }

        if options and options.get("idempotency_key"):
            headers["Idempotency-Key"] = options["idempotency_key"]

        last_error = None

        for attempt in range(self.retries + 1):
            try:
                data = json.dumps(body).encode("utf-8") if body else None
                req = urllib.request.Request(url, data=data, headers=headers, method=method)
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    response_body = response.read().decode("utf-8")
                    if not response_body:
                        return None
                    return json.loads(response_body)

            except urllib.error.HTTPError as e:
                try:
                    error_body = json.loads(e.read().decode("utf-8"))
                except Exception:
                    error_body = {}

                # Don't retry client errors except 429 and 408
                if 400 <= e.code < 500 and e.code != 429 and e.code != 408:
                    raise map_error(e.code, error_body)

                # Handle rate limiting
                if e.code == 429:
                    retry_after = int(e.headers.get("Retry-After", "60"))
                    if attempt < self.retries:
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError(error_body.get("error", {}).get("detail", "Rate limited"), retry_after)

                # Server errors and timeouts - retry
                last_error = map_error(e.code, error_body)
                if attempt < self.retries:
                    time.sleep(2 ** attempt + 0.5)
                    continue

                raise last_error

            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    time.sleep(2 ** attempt + 0.5)
                    continue

        raise last_error or Exception("Request failed after retries")


class PaginatedList:
    """Auto-paginating list iterator."""

    def __init__(self, http: HttpClient, path: str, params: Dict[str, Any] = None, per_page: int = 50):
        self.http = http
        self.path = path
        self.params = params or {}
        self.per_page = per_page
        self.page = 1
        self.items = []
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.items and not self.exhausted:
            self._fetch_page()
        
        if not self.items:
            raise StopIteration
        
        return self.items.pop(0)

    def _fetch_page(self):
        params = {**self.params, "page": str(self.page), "per_page": str(self.per_page)}
        query = "&".join(f"{k}={v}" for k, v in params.items() if v)
        path = f"{self.path}?{query}" if query else self.path
        
        response = self.http.request("GET", path)
        
        if isinstance(response, list):
            self.items = response
            if len(self.items) < self.per_page:
                self.exhausted = True
        elif isinstance(response, dict):
            # Handle different response formats
            if "deliveries" in response:
                self.items = response["deliveries"]
            elif "data" in response:
                self.items = response["data"]
            elif "applications" in response:
                self.items = response["applications"]
            elif "endpoints" in response:
                self.items = response["endpoints"]
            else:
                self.items = []
            if not self.items or response.get("has_more") is False:
                self.exhausted = True
        
        self.page += 1

    def all(self) -> list:
        """Collect all items into a list."""
        return list(self)
