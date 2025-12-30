import urllib
import requests
from core.utils.env import EnvConfig
from core.utils.state import global_state
from core.utils.logger import logger
from typing import Dict, Any

class EspoAPIError(Exception):
    pass

def snake_to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

def build_espo_params(
    local_vars: Dict[str, Any],
    *,
    exclude: set[str] = frozenset(),
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    for key, value in local_vars.items():
        if key in exclude or value is None:
            continue
        # Skip common unwanted local names (e.g. `self`, `kwargs`, etc.)
        if key in ("self", "kwargs"):
            continue

        # Convert snake_case keys to camelCase as Espo uses camelCase parameter names
        camel_key = snake_to_camel(key)
        params[camel_key] = value

    return params


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, (list, tuple)):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs

    return urllib.parse.urlencode(r_urlencode(data))


class EspoAPI:
    def __init__(self, url, api_key, default_headers=None):
        self.url = url.rstrip('/')
        self.api_key = api_key
        self.default_headers = default_headers or {}

    def normalize_url(self, action):

        if action is None:
            return self.url

        sa = str(action)
        
        if sa.startswith('http://') or sa.startswith('https://'):
            return sa
        
        return f"{self.url.rstrip('/')}/{sa.lstrip('/')}"

    def request(self, method, action, params=None, extra_headers=None, force_query_params=False, allow_non_2xx: bool = False, timeout: int = 10):
        if params is None:
            params = {}

        result = self.call_api(
            method=method,
            action=action,
            params=params,
            extra_headers=extra_headers,
            timeout=timeout,
            force_query_params=force_query_params,
            allow_non_2xx=allow_non_2xx,
        )

        if result is None:
            return None

        if result.get("status_code") == 204:
            return None

        return result.get("data")

    def call_api(self, method: str, action: str, params=None, extra_headers=None, timeout: int = 10, force_query_params: bool = False, allow_non_2xx: bool = False):
        """Instance convenience wrapper around module-level `call_api`.

        This matches the user's preferred usage: `client.call_api(...)`.
        """
        url = self.normalize_url(action)
        headers = {}
        headers.update(self.default_headers or {})

        if extra_headers:
            headers.update(extra_headers)

        headers["X-Api-Key"] = self.api_key

        kwargs = {"headers": headers, "timeout": timeout}

        if method.upper() in ["POST", "PATCH", "PUT"] and not force_query_params:
            if params:
                kwargs["json"] = params
        else:
            query = http_build_query(params) if params else ""
            if query:
                url = url + "?" + query

        try:
            resp = requests.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            return {
                "status_code": None,
                "ok": False,
                "data": None,
                "error": str(e),
                "error_type": "network",
            }

        status = resp.status_code

        if not allow_non_2xx and status not in (200, 201, 204):
            reason = resp.headers.get('X-Status-Reason', 'Unknown Error')
            msg = f"EspoAPI {method} {action} returned status {status}: {reason}"
            if status >= 500:
                logger.error(msg)
            else:
                logger.warning(msg)

        body = None
        try:
            body = resp.json()
        except ValueError:
            body = resp.text

        ok = 200 <= status < 300
        error = None
        error_type = None

        if not ok:
            error = f"HTTP {status}"
            error_type = "api"

        return {
            "status_code": status,
            "ok": ok,
            "data": body,
            "error": error,
            "error_type": error_type,
        }

    def build_params(self, local_vars: Dict[str, Any], *, exclude: set[str] = frozenset()) -> Dict[str, Any]:
        """Convenience wrapper to build Espo params from a locals() dict.

        Usage: `params = client.build_params(locals())`
        """
        return build_espo_params(local_vars, exclude=exclude)


def get_client(url: str | None = None, api_key: str | None = None):
    """Create and return a new EspoAPI client for each call."""

    if not url or not api_key:
        logger.error('ESPO API client not configured: missing URL or API key')
        return None

    return EspoAPI(url, api_key)


def call_api(
    client: EspoAPI,
    method: str,
    action: str,
    params=None,
    extra_headers=None,
    timeout: int = 10,
    force_query_params: bool = False,
    allow_non_2xx: bool = False,
):
    """Compatibility wrapper that delegates to the instance method
    `EspoAPI.call_api`. Keeping this function prevents breaking callers
    that import `call_api` from the module.
    """
    return client.call_api(
        method=method,
        action=action,
        params=params,
        extra_headers=extra_headers,
        timeout=timeout,
        force_query_params=force_query_params,
        allow_non_2xx=allow_non_2xx,
    )



