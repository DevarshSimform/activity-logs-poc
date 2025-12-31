import json
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RequestIDLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to assign a unique request ID to each incoming request and log the request/response.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()

        # Extract additional request details
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        referer = request.headers.get("referer", "unknown")
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)

        # Optional: read request body (only if you need it)
        try:
            body = await request.body()
            body_data = body.decode() if body else None
        except Exception:
            body_data = None

        # Process the request
        response: Response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Add response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        # Response details
        content_length = response.headers.get("Content-Length", "unknown")

        # Structured Log (recommended for Kafka logging or DB logs)
        log_data = {
            "request_id": request_id,
            "method": method,
            "path": path,
            "query_params": query_params,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "referer": referer,
            "status_code": response.status_code,
            "content_length": content_length,
            "process_time": f"{process_time:.4f} seconds",
            "timestamp": time.time(),
            "request_body": body_data,  # Optional
        }

        print(json.dumps(log_data, indent=2))

        return response


def setup_middlewares(app):
    app.add_middleware(RequestIDLoggingMiddleware)
