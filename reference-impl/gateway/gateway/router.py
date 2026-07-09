"""Ruteo de modelos: manda tareas simples a un modelo barato y complejas a uno caro.

Heurística simple y explicable (longitud + señales de complejidad). Se puede
overridear por tenant/tier con `force`.
"""

from __future__ import annotations

_COMPLEX_HINTS = (
    "analiza",
    "compara",
    "razona",
    "demostra",
    "por que",
    "paso a paso",
    "code",
    "codigo",
    "código",
)

CHEAP_MODEL = "claude-haiku-4-5"
EXPENSIVE_MODEL = "claude-sonnet-5"


def route(prompt: str, force: str | None = None) -> tuple[str, str]:
    """Devuelve (tier_modelo, model_id) con tier_modelo en {cheap, expensive}."""
    if force in ("cheap", "expensive"):
        model_tier = force
    else:
        text = (prompt or "").lower()
        is_long = len(text) > 240
        is_complex = any(hint in text for hint in _COMPLEX_HINTS)
        model_tier = "expensive" if (is_long or is_complex) else "cheap"
    model = CHEAP_MODEL if model_tier == "cheap" else EXPENSIVE_MODEL
    return model_tier, model
