from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

STATUS_TOTAL = Counter("status_requests_total", "Total /status requests received")

@app.get("/status")
def status():
    STATUS_TOTAL.inc()
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
