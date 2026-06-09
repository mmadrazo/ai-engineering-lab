import truststore

truststore.inject_into_ssl()

from fastapi import FastAPI
from app.routers.estimations import router as estimations_router

app = FastAPI(
    title="Estimador CAG API",
    description="API para generar estimaciones de software a partir de transcripciones usando contexto en prompt.",
)

app.include_router(estimations_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok","service": "estimador-cag"}