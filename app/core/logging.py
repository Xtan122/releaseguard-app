# app/core/logging.py
import json
import logging
import sys
from datetime import datetime, timezone

from app.core.config import settings
from app.core.context import request_id_context


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "service": settings.SERVICE_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "message": record.getMessage(),
        }

        req_id = getattr(record, "request_id", None) or request_id_context.get()
        if req_id:
            log_data["request_id"] = req_id

        for field in ["method", "path", "status", "duration_ms"]:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure JSON structured logging for the application."""
    formatter = JSONFormatter()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = []
    root_logger.addHandler(handler)

    # Log một dòng xác nhận app đã khởi động
    logging.getLogger(__name__).info("logging configured")
