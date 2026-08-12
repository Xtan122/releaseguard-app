import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context import request_id_context
from app.metrics.prometheus import http_request_duration_seconds, http_requests_total

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Lưu request ID vào context variable
        token = request_id_context.set(req_id)
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
        finally:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            status_code = response.status_code if 'response' in locals() else 500
            
            logger.info(
                "request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status": status_code,
                    "duration_ms": duration_ms,
                    "request_id": req_id,
                }
            )
            
            duration = time.time() - start_time
            http_requests_total.labels(
                method=request.method,
                path=request.url.path,
                status=str(status_code),
            ).inc()
            http_request_duration_seconds.labels(
                method=request.method,
                path=request.url.path,
            ).observe(duration)
            
            if 'response' in locals():
                response.headers["X-Request-ID"] = req_id
                
            request_id_context.reset(token)
            
        return response