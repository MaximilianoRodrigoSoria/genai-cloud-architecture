<p align="center">
<a href="https://www.linkedin.com/in/soriamaximilianorodrigo/" target="_blank" rel="noopener noreferrer">
<img width="100%" height="100%" src="docs/img/banner.gif" alt="genai-cloud-architecture"></a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Cloud-AWS_%7C_GCP-FF9900?logo=amazonaws&logoColor=white&style=flat-square" alt="Cloud"></a>
  <a href="#"><img src="https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white&style=flat-square" alt="Terraform"></a>
  <a href="#"><img src="https://img.shields.io/badge/Arquitectura-Multi--tenant-14B8A6?style=flat-square" alt="Multi-tenant"></a>
  <a href="#"><img src="https://img.shields.io/badge/Diagramas-Mermaid-22D3EE?style=flat-square" alt="Mermaid"></a>
</p>

<p align="center">
  <a href="https://github.com/DietrichGebert/ponytail"><img src="https://img.shields.io/badge/built_with-ponytail-111111?style=flat-square" alt="ponytail"></a>
  <img src="https://img.shields.io/badge/layout-src%2Fpackage-14B8A6?style=flat-square" alt="src layout">
  <img src="https://img.shields.io/badge/license-MIT-success?style=flat-square" alt="MIT">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=1DE9B6&center=true&vCenter=true&width=820&lines=Arquitectura+GenAI+cloud%2C+escalable+y+multi-tenant;aislamiento+por+tenant+%C2%B7+rate+limit+%C2%B7+caching+sem%C3%A1ntico;AWS%2FGCP+%2B+Terraform+%2B+gateway+de+referencia" alt="typing SVG">
</p>

<hr/>

<h1 align="center">genai-cloud-architecture</h1>

<p align="center">
<b>Arquitectura cloud</b> escalable y <b>multi-tenant</b> para servir modelos LLM (AWS o GCP),
con ADRs, diagrama e implementación mínima de referencia.
</p>

## ¿Qué resuelve este proyecto?

Cierra el portfolio con la mirada de arquitecto: cómo se lleva un sistema GenAI de un notebook a una plataforma que sirve a múltiples clientes (tenants) de forma escalable, segura y con costos bajo control. El entregable central es un **diagrama de arquitectura** bien razonado, sostenido por un conjunto de decisiones documentadas (trade-offs), más una **implementación mínima** que demuestra que el diseño es realizable, no solo un dibujo.

Preguntas que la arquitectura debe responder:

- **Escalabilidad** — ¿cómo absorbe picos de tráfico? (autoscaling, colas, batching de inferencia).
- **Multi-tenancy** — ¿cómo se aíslan datos y costos por tenant? (partición de datos, rate limiting y cuotas por tenant, atribución de costos).
- **Seguridad** — gestión de secretos, aislamiento de red, autenticación/autorización, protección frente a prompt injection.
- **Costos** — caching semántico, ruteo de modelos (barato vs caro según la tarea), observabilidad de gasto por tenant.
- **Gobernanza** — versionado de prompts/modelos, guardrails, auditoría.

## ¿Qué pasos sigue?

Cada request atraviesa el gateway en este orden: **autenticación por tenant → rate limit y cuota → cache semántico → ruteo de modelo (barato vs caro) → orquestación RAG e inferencia → atribución de costo y respuesta**. El diagrama completo de la plataforma está en [`docs/architecture.md`](docs/architecture.md).

## Qué hace cada parte

| Pieza | Rol |
|---|---|
| **API Gateway + WAF** | Ingreso protegido; authorizer Cognito con `tenant_id`. |
| **Gateway** | Rate limit, cuotas y ruteo de modelos por tenant. |
| **Cache semántico** | Evita pagar inferencia por preguntas repetidas o similares. |
| **Ruteo de modelos** | Modelo barato para tareas simples, caro para las complejas. |
| **Orquestación RAG** | Recupera del vector store (namespace por tenant) e invoca el modelo. |
| **Datos por tenant** | DynamoDB / S3 / OpenSearch particionados por `tenant_id`. |
| **Observabilidad** | Costo, latencia y errores por tenant (capa `llmops-observability`). |

## Por qué es bueno tenerlo

Muestra cómo llevar un GenAI de notebook a plataforma multi-tenant sin que exploten el costo ni el aislamiento. No es solo un dibujo: las decisiones quedan documentadas como **ADRs con trade-offs**, y el diseño se respalda con un **gateway corrible y testeado** (`reference-impl/gateway/`) más un esqueleto Terraform, que prueban que es realizable.

## Stack tecnológico

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

## Estructura de carpetas

```
genai-cloud-architecture/
├── README.md
├── AGENTS.md                        # Ruleset ponytail (código mínimo)
├── docs/
│   ├── architecture.md             # Documento principal: diagrama Mermaid + trade-offs
│   ├── multi-tenancy.md            # Estrategia de aislamiento y cuotas por tenant
│   └── adr/
│       ├── 0001-provider-choice.md
│       ├── 0002-inference-serving.md
│       └── 0003-tenant-isolation.md
└── reference-impl/                 # Implementación mínima de referencia
    ├── gateway/                    # Gateway FastAPI corrible + tests (offline)
    │   ├── gateway/               # auth · ratelimit · cache · router · inference · app
    │   └── tests/
    └── infra/                     # Terraform skeleton (DynamoDB, S3, SQS, Cognito, Secrets)
```

## Componentes del diagrama

Cubiertos en el diagrama de [`docs/architecture.md`](docs/architecture.md):

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
