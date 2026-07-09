"""Gateway GenAI de referencia (FastAPI).

Flujo de POST /v1/chat:
  auth por tenant → rate limit → cache → ruteo de modelo → inferencia → cache + costo

`create_app(...)` permite inyectar inferencia, rate limiter y cache (usado en tests).
"""

from __future__ import annotations

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .auth import authenticate
from .cache import SemanticCache
from .config import TIERS
from .inference import MockInference
from .ratelimit import RateLimiter
from .router import route

_PRICES = {"claude-haiku-4-5": (0.0008, 0.004), "claude-sonnet-5": (0.003, 0.015)}


def _cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p_in, p_out = _PRICES.get(model, (0.0, 0.0))
    return round(input_tokens / 1000 * p_in + output_tokens / 1000 * p_out, 6)


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


def _api_key_from_header(authorization: str | None) -> str | None:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return None


def create_app(inference=None, rate_limiter=None, cache=None) -> FastAPI:
    app = FastAPI(title="genai-gateway", version="0.1.0")
    app.state.inference = inference or MockInference()
    app.state.rate_limiter = rate_limiter or RateLimiter()
    app.state.cache = cache or SemanticCache()

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/v1/chat")
    def chat(req: ChatRequest, authorization: str | None = Header(default=None)):
        tenant = authenticate(_api_key_from_header(authorization))
        if tenant is None:
            return JSONResponse(status_code=401, content={"error": "unauthorized"})

        tier = TIERS[tenant.tier]
        if not app.state.rate_limiter.allow(tenant, tier):
            return JSONResponse(
                status_code=429, content={"error": "rate_limited", "tenant": tenant.id}
            )

        cached = app.state.cache.get(tenant.id, req.prompt)
        if cached is not None:
            return {"tenant": tenant.id, "cached": True, "answer": cached}

        _model_tier, model = route(req.prompt, force=tier.force_model)
        result = app.state.inference.complete(model, req.prompt)
        app.state.cache.put(tenant.id, req.prompt, result.text)
        return {
            "tenant": tenant.id,
            "cached": False,
            "model": model,
            "answer": result.text,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "cost_usd": _cost(model, result.input_tokens, result.output_tokens),
        }

    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    run()
