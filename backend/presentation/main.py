import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

from backend.presentation.routes import router

REQUEST_COUNT = Counter("http_requests_total", "HTTP Requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["method", "path"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        latency = time.time() - start
        REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, request.url.path).observe(latency)
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="Menna API", default_response_class=Response)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type="text/plain")

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": os.getenv("APP_ENV", "development")}

    return app


app = create_app()
