# Arquitectura — plataforma GenAI multi-tenant

Documento principal de decisiones y trade-offs. El diagrama vive en
`docs/diagrams/architecture.mmd`; la implementación mínima en `reference-impl/`.

## Componentes

1. **Ingreso** — API Gateway / Load Balancer con WAF.
2. **AuthN/AuthZ por tenant** — la identidad lleva `tenant_id` en los claims.
3. **Rate limiting y cuotas** por tenant en el gateway.
4. **Capa de aplicación** stateless y autoescalable.
5. **Orquestación LLM** — RAG + tools (reusa `rag-pipeline-eval` y `mcp-server-demo`).
6. **Caching semántico** — reduce costo y latencia.
7. **Ruteo de modelos** — barato para tareas simples, caro para complejas.
8. **Vector store** con aislamiento lógico por tenant (namespace/partición).
9. **Almacenamiento** particionado por tenant.
10. **Colas/async** para cargas pesadas (ingesta, batch de embeddings).
11. **Secretos + red privada**.
12. **Observabilidad y atribución de costos por tenant** (enlaza con `llmops-observability`).
13. **Guardrails** (input/output) y auditoría.

## Trade-offs clave

- **Gestionado vs self-hosted** (Bedrock/Vertex vs SageMaker/GPU propia): gestionado
  acelera el time-to-market y descarga la operación; self-hosted baja el costo por
  token a alto volumen y da control de datos. Se elige gestionado para el MVP.
- **Aislamiento silo vs pool** (ver `multi-tenancy.md`): pool para eficiencia de costo,
  silo para tenants regulados. Se adopta un modelo **híbrido**.
- **Caching semántico**: baja costo/latencia pero arriesga respuestas obsoletas;
  se acota con TTL y umbral de similitud alto.

## Cómo escalaría en producción

Autoscaling horizontal de la capa stateless; colas para desacoplar ingesta;
particionado del vector store por tenant; presupuesto y alertas de costo por tenant;
CDN/caché para respuestas frecuentes; y despliegue multi-AZ.
