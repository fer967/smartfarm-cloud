## Arquitectura

- FastAPI como API principal
- Ingesta desacoplada mediante BackgroundTasks
- Retry y Dead-letter para eventos fallidos
- Rate limiting simulando API Gateway
- Versionado de API (/api/v1)
- Observabilidad básica (logs + healthchecks)
- MongoDB para telemetría
- MySQL para datos relacionales
