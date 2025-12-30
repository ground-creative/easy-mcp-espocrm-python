# app/middleware/MyMiddleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from mcp.server.fastmcp import Context      # Use `ctx: Context` as function param to get mcp context
from core.utils.logger import logger        # Use to add logging capabilities
from core.utils.state import global_state   # Use to add and read global vars

class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, *args, **kwargs
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        try:
            global_state.set(
                "middleware.AuthenticationMiddleware.is_authenticated", False, True
            )
            global_state.set("api_key", "", True)
            global_state.set("api_address", None, True)
            api_key = request.headers.get("x-api-key", None)

            if not api_key:
                global_state.set(
                    "middleware.AuthenticationMiddleware.error_message",
                    f"X-API-KEY is a required header parameter. Please create an API key to access the EspoCRM API.",
                    True,
                )
                return await call_next(request)

            api_address = request.headers.get("x-api-address", None)

            if not api_address:
                global_state.set(
                    "middleware.AuthenticationMiddleware.error_message",
                    f"X-API-ADDRESS is a required header parameter. Please provide an API address to access the EspoCRM API.",
                    True,
                )
                return await call_next(request)

            global_state.set(
                "middleware.AuthenticationMiddleware.is_authenticated", True, True
            )
            global_state.set("api_key", api_key, True)
            global_state.set("api_address", api_address, True)

            return await call_next(request)

        except Exception as e:
            logger.error(f"AuthenticationMiddleware authentication failed: {str(e)}")
            global_state.set(
                "middleware.AuthenticationMiddleware.error_message",
                f"Error trying to set API Key for authentication: {str(e)}",
                True,
            )
            return await call_next(request)

def check_access(returnJsonOnError=False):

    if not global_state.get("middleware.AuthenticationMiddleware.is_authenticated"):
        logger.error("AuthenticationMiddleware: User has not set API key in headers.")

        if returnJsonOnError:
            return {
                "status": "error",
                "error": global_state.get(
                    "middleware.AuthenticationMiddleware.error_message",
                    "User has not set API key in headers.",
                ),
            }

        return "User has not set API key in headers."
    return None  # Return None if authenticated
