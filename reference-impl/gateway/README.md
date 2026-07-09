# Gateway de referencia

Implementación mínima y **corrible** del gateway multi-tenant descrito en
`docs/architecture.md`. Demuestra que el diseño es realizable: auth por tenant,
rate limiting, caching semántico y ruteo de modelos, todo testeado y offline
(inferencia mock).

## Correr

```bash
python -m pip install --user -r requirements.txt
uvicorn gateway.app:app --reload --port 8080
```

```bash
# Un tenant válido (pro):
curl -X POST localhost:8080/v1/chat -H "Authorization: Bearer key-pro-def" \
  -H "Content-Type: application/json" -d "{\"prompt\": \"hola\"}"
```

Claves demo: `key-free-abc` (free), `key-pro-def` (pro), `key-ent-ghi` (enterprise).

## Qué demuestra

| Pieza | Módulo | Concepto de arquitectura |
|---|---|---|
| Auth por tenant | `auth.py` | Identidad y `tenant_id` (en prod: Cognito) |
| Rate limit | `ratelimit.py` | Token bucket por tenant, cuotas por tier |
| Cache semántico | `cache.py` | Ahorro de costo/latencia (stub léxico; en prod: embeddings) |
| Ruteo de modelos | `router.py` | Barato vs caro según complejidad, override por tier |
| Inferencia | `inference.py` | Mock (en prod: Bedrock/SageMaker) |
| Orquestación | `app.py` | Flujo auth → rate limit → cache → ruteo → inferencia → costo |

## Tests

```bash
python -m pytest -q
```
