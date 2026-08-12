from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.api.routes.orders import router as order_router
from app.core.logging import setup_logging
from app.metrics.prometheus import init_metrics
from app.middleware.request_context import RequestContextMiddleware

setup_logging()

app = FastAPI()
app.add_middleware(RequestContextMiddleware)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health/live")
def health_live():
    return {"status": "ok"}

@app.get("/health/ready")  
def health_ready():
    return {"status": "ok"}

app.include_router(order_router, prefix="/api/orders", tags=["orders"])

# Sau khi tạo app:
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
# Gọi trong startup:
init_metrics()