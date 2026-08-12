from prometheus_client import Counter, Gauge, Histogram

from app.core.config import settings

# RED metrics for HTTP
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)

# App metadata
application_info = Gauge(
    "application_info",
    "Application metadata",
    ["version", "environment"],
)

# Order business metrics
orders_created_total = Counter(
    "orders_created_total",
    "Total orders successfully created",
)
orders_failed_total = Counter(
    "orders_failed_total",
    "Total order creation failures",
)
# Database metrics
database_operation_duration_seconds = Histogram(
    "database_operation_duration_seconds",
    "Database operation duration in seconds",
    ["operation"],  # e.g. "insert", "select"
)

def init_metrics() -> None:
    """Set static gauge values at startup."""
    application_info.labels(
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    ).set(1)