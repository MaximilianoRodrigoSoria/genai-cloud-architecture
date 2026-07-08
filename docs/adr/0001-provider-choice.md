# ADR 0001 — Elección de proveedor cloud

## Estado
Aceptada.

## Contexto
Necesitamos servir modelos LLM multi-tenant con time-to-market corto.

## Decisión
Usar **AWS** con **Bedrock** para inferencia gestionada en el MVP. Alternativa
equivalente: GCP + Vertex AI.

## Consecuencias
- (+) Menos operación, modelos gestionados, escalado administrado.
- (+) Integración con IAM/Secrets Manager/VPC.
- (−) Menor control del costo por token a muy alto volumen (mitigable migrando
  cargas pesadas a SageMaker/GPU propia más adelante).
