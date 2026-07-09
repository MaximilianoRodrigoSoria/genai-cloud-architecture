"""Cache semántico (stub por similitud léxica) aislado por tenant.

Acá la similitud es Jaccard sobre palabras (determinista, sin dependencias) para
que la demo y los tests corran offline. En producción se reemplaza por embeddings
+ búsqueda por similitud coseno en el vector store, manteniendo la misma interfaz.
"""

from __future__ import annotations


def _tokens(text: str) -> set[str]:
    return set((text or "").lower().split())


def similarity(a: str, b: str) -> float:
    """Similitud de Jaccard entre dos textos (0..1)."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


class SemanticCache:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self._store: dict[str, list[tuple[str, str]]] = {}

    def get(self, tenant_id: str, prompt: str) -> str | None:
        best_response: str | None = None
        best_sim = 0.0
        for cached_prompt, response in self._store.get(tenant_id, []):
            sim = similarity(prompt, cached_prompt)
            if sim > best_sim:
                best_sim, best_response = sim, response
        return best_response if best_sim >= self.threshold else None

    def put(self, tenant_id: str, prompt: str, response: str) -> None:
        self._store.setdefault(tenant_id, []).append((prompt, response))
