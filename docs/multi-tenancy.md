# Estrategia de multi-tenancy

| Modelo | Aislamiento | Costo | Cuándo |
|---|---|---|---|
| **Silo** | recursos dedicados por tenant | alto | tenants regulados / enterprise |
| **Pool** | recursos compartidos, partición lógica | bajo | mayoría de tenants |
| **Híbrido** | pool por defecto, silo para los que lo requieran | medio | recomendado |

## Cómo se aísla cada capa (modelo pool)

- **Identidad:** `tenant_id` en el token; el gateway lo propaga en cada request.
- **Datos:** partición por `tenant_id` (fila) o namespace (vector store).
- **Cuotas:** rate limit y presupuesto por tenant en el gateway.
- **Costos:** cada request se etiqueta con `tenant_id` para atribución.

La implementación mínima (`reference-impl/gateway`) demuestra identidad por tenant,
rate limiting por tenant y caching, que son el núcleo del aislamiento en el borde.
