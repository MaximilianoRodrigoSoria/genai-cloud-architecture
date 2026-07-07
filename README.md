<p align="center">
<a href="https://www.linkedin.com/in/soriamaximilianorodrigo/" target="_blank" rel="noopener noreferrer">
<img width="100%" height="100%" src="docs/img/banner.gif" alt="genai-cloud-architecture"></a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Cloud-AWS_%7C_GCP-FF9900?logo=amazonaws&logoColor=white" alt="Cloud"></a>
  <a href="#"><img src="https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white" alt="Terraform"></a>
  <a href="#"><img src="https://img.shields.io/badge/Arquitectura-Multi--tenant-0F6E56" alt="Multi-tenant"></a>
  <a href="#"><img src="https://img.shields.io/badge/Diagramas-draw.io-F08705" alt="draw.io"></a>
</p>

---

# genai-cloud-architecture

**Diagrama de arquitectura cloud** escalable y **multi-tenant** para servir modelos LLM (AWS o GCP), acompañado de una **implementación mínima de referencia** que materializa las decisiones clave.

## Objetivo

Cerrar el portfolio con la mirada de arquitecto: cómo se lleva un sistema GenAI de un notebook a una plataforma que sirve a múltiples clientes (tenants) de forma escalable, segura y con costos bajo control. El entregable central es un **diagrama de arquitectura** bien razonado, sostenido por un conjunto de decisiones documentadas (trade-offs), más una **implementación mínima** que demuestra que el diseño es realizable, no solo un dibujo.

Preguntas que la arquitectura debe responder:

- **Escalabilidad** — ¿cómo absorbe picos de tráfico? (autoscaling, colas, batching de inferencia).
- **Multi-tenancy** — ¿cómo se aíslan datos y costos por tenant? (partición de datos, rate limiting y cuotas por tenant, atribución de costos).
- **Seguridad** — gestión de secretos, aislamiento de red, autenticación/autorización, protección frente a prompt injection.
- **Costos** — caching semántico, ruteo de modelos (barato vs caro según la tarea), observabilidad de gasto por tenant.
- **Gobernanza** — versionado de prompts/modelos, guardrails, auditoría.

## Stack tecnológico sugerido

Elegir **un** proveedor y ser coherente. Dos rutas de referencia:

**AWS**
- Gateway/API: API Gateway + Lambda o ALB + ECS/Fargate
- Inferencia: Amazon Bedrock (modelos gestionados) y/o SageMaker (modelos propios)
- Vector store: OpenSearch (k-NN) o Aurora pgvector
- Colas/async: SQS + (opcional) Step Functions para orquestación
- Datos/tenant: DynamoDB/Aurora con partición por tenant; S3 con prefijos por tenant
- Seguridad: Cognito (authn), IAM, Secrets Manager, VPC + PrivateLink
- Observabilidad: CloudWatch + la capa de `llmops-observability`

**GCP**
- Gateway/API: API Gateway/Cloud Endpoints + Cloud Run
- Inferencia: Vertex AI (modelos gestionados y propios)
- Vector store: Vertex AI Vector Search o AlloyDB/pgvector
- Colas/async: Pub/Sub + (opcional) Workflows
- Datos/tenant: Firestore/Cloud SQL con partición por tenant; GCS con buckets/prefijos por tenant
- Seguridad: Identity Platform, IAM, Secret Manager, VPC Service Controls
- Observabilidad: Cloud Monitoring + la capa de `llmops-observability`

**Infra como código:** Terraform (recomendado, portable) o CDK/Pulumi.
**Diagramas:** `draw.io` / diagrams.net, o `diagrams` (Python, "diagram as code") para versionar el diagrama junto al código.

## Estructura de carpetas propuesta

```
genai-cloud-architecture/
├── README.md
├── docs/
│   ├── architecture.md          # Documento principal: decisiones y trade-offs
│   ├── diagrams/
│   │   ├── architecture.drawio  # Diagrama editable
│   │   ├── architecture.png     # Export para el README
│   │   └── diagram.py           # (Opcional) diagram-as-code con `diagrams`
│   ├── multi-tenancy.md         # Estrategia de aislamiento y cuotas por tenant
│   └── adr/
│       ├── 0001-provider-choice.md
│       ├── 0002-inference-serving.md
│       └── 0003-tenant-isolation.md
├── reference-impl/              # Implementación mínima de referencia
│   ├── infra/                   # Terraform (o CDK) del subconjunto desplegable
│   ├── gateway/                 # API con auth + rate limiting por tenant
│   └── inference/               # Endpoint de inferencia con caching semántico
└── diagrams-src/                # Fuentes auxiliares de diagramas
```

## Componentes del diagrama (checklist de contenido)

- [ ] **Ingreso:** API Gateway / Load Balancer con WAF.
- [ ] **AuthN/AuthZ:** identidad por tenant (claims con `tenant_id`).
- [ ] **Rate limiting y cuotas** por tenant en el gateway.
- [ ] **Capa de aplicación** (contenedores/serverless) stateless y autoescalable.
- [ ] **Orquestación LLM:** RAG + tools (integrando los proyectos previos del portfolio).
- [ ] **Caching semántico** para reducir costo y latencia.
- [ ] **Ruteo de modelos** (modelo barato para tareas simples, caro para complejas).
- [ ] **Vector store** con aislamiento lógico por tenant (namespace/partición).
- [ ] **Almacenamiento de datos** particionado por tenant.
- [ ] **Colas/async** para cargas pesadas (ingesta, batch de embeddings).
- [ ] **Gestión de secretos** y red privada.
- [ ] **Observabilidad y atribución de costos** por tenant (enlaza con `llmops-observability`).
- [ ] **Guardrails** (input/output) y auditoría.

## Checklist de implementación

### Fase 1 — Diseño

- [ ] Elegir proveedor (AWS o GCP) y justificarlo en un ADR.
- [ ] Redactar `architecture.md` con el diseño y los trade-offs de cada decisión.
- [ ] Definir el modelo de multi-tenancy (silo vs pool vs híbrido) en `multi-tenancy.md`.

### Fase 2 — Diagrama

- [ ] Construir el diagrama principal en draw.io con todos los componentes de la lista.
- [ ] Exportar a PNG e incrustarlo en el README/architecture.md.
- [ ] (Opcional) Versionar el diagrama como código con la librería `diagrams`.

### Fase 3 — ADRs (decisiones de arquitectura)

- [ ] ADR: elección de proveedor.
- [ ] ADR: serving de inferencia (gestionado vs self-hosted; batching).
- [ ] ADR: estrategia de aislamiento de tenants (datos, cuotas, costos).

### Fase 4 — Implementación mínima de referencia

- [ ] Terraform que despliegue un subconjunto realista (gateway + un servicio de inferencia).
- [ ] Gateway con **auth por tenant** y **rate limiting/cuotas** por `tenant_id`.
- [ ] Endpoint de inferencia con **caching semántico** demostrable.
- [ ] Atribución de costo por tenant (etiqueta cada request con su `tenant_id`).

### Fase 5 — Documentación

- [ ] README con el diagrama, el resumen de decisiones y cómo desplegar la implementación mínima.
- [ ] Sección de "cómo escalaría esto en producción" (límites conocidos y siguientes pasos).
- [ ] Enlazar explícitamente con los otros 4 proyectos del portfolio (dónde encaja cada uno).

## Criterios de "terminado"

Existe un diagrama claro y defendible de una plataforma GenAI multi-tenant, respaldado por ADRs con trade-offs explícitos, y una implementación mínima que demuestra al menos **aislamiento por tenant + rate limiting + caching semántico**. El diseño integra conceptualmente los otros proyectos del portfolio.
