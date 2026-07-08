"""Gateway multi-tenant de referencia.

Demuestra el núcleo del diseño en el borde: identidad por tenant, rate limiting
por tenant, caching y atribución de costo por tenant. La inferencia está stubbeada.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from gateway.auth import resolve_tenant
from gateway.cache import SemanticCache
from gateway.config import CACHE_TTL_SECONDS, RATE_LIMIT_PER_MINUTE
from gateway.ratelimit import RateLimiter

app = FastAPI(title="genai-gateway (reference)", version="0.1.0")

_limiter = RateLimiter(RATE_LIMIT_PER_MINUTE)
_cache = SemanticCache(CACHE_TTL_SECONDS)


def get_tenant(x_api_key: str | None = Header(default=None)) -> str:
    tenant = resolve_tenant(x_api_key)
    if tenant is None:
        raise HTTPException(status_code=401, detail="API key inválida o ausente")
    return tenant


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


def _infer(prompt: str) -> str:
    # Stub de inferencia; en producción rutea a Bedrock/Vertex/SageMaker.
    return f"respuesta a: {prompt[:60]}"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/generate")
def generate(req: GenerateRequest, tenant: str = Depends(get_tenant)) -> dict:
    if not _limiter.allow(tenant):
        raise HTTPException(status_code=429, detail="Rate limit excedido para el tenant")

    cached = _cache.get(tenant, req.prompt)
    if cached is not None:
        return {"tenant": tenant, "answer": cached, "cached": True}

    answer = _infer(req.prompt)
    _cache.put(tenant, req.prompt, answer)
    return {"tenant": tenant, "answer": answer, "cached": False}
