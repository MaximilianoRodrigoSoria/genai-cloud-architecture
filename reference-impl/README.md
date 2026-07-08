# Implementación mínima de referencia

- `gateway/` — API multi-tenant (FastAPI) que demuestra **identidad por tenant**,
  **rate limiting por tenant** y **cache**. Corré los tests:

  ```bash
  cd gateway && poetry install --with dev && poetry run pytest
  poetry run uvicorn gateway.app:app --reload
  curl -X POST localhost:8000/v1/generate -H "X-API-Key: key-acme" \
    -H "Content-Type: application/json" -d '{"prompt":"hola"}'
  ```

- `infra/` — esqueleto Terraform (API Gateway + tabla DynamoDB particionada por
  `tenant_id`). Ilustrativo: `terraform init && terraform validate`.
