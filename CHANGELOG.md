# Changelog

Todos los cambios notables de este proyecto se documentan acá.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-07-11

### Añadido
- Documento de arquitectura (`docs/architecture.md`) con diagrama Mermaid y trade-offs de escalabilidad, multi-tenancy, seguridad, costos y gobernanza.
- Estrategia de multi-tenancy (`docs/multi-tenancy.md`).
- Tres ADRs: elección de proveedor (AWS), serving de inferencia + ruteo/costos, y aislamiento por tenant.
- Gateway de referencia corrible (FastAPI): auth por tenant, rate limiting, caching semántico y ruteo de modelos, con 18 tests.
- Esqueleto Terraform del subconjunto desplegable (DynamoDB, S3, SQS, Cognito, Secrets Manager).
- Archivos de comunidad, CI (GitHub Actions), badges, sitio de GitHub Pages y social preview.
