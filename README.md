# HMPPS Domain Events

## What is an HMPPS Domain Event?

HMPPS domain events are intended to capture and broadcast the occurrence of
significant activity in an HMPPS domain. They can be used to facilitate
choreographed processes across HMPPS systems. Capturing and publishing
business-level events as workflows are completed in different systems supports
the architectural direction of HMPPS, which is based on small, domain-oriented
services working together to support justice system processes.

## HMPPS Domain Event Message Specification

HMPPS domain event messages must conform to the JSON Schema for domain events
defined [here](./schema/hmpps-domain-event.json).

ASyncAPI schemas for individual domain event messages are
[here](./spec/schemas/)

## Infrastructure

HMPPS domain events may be published as notifications to a shared SNS topic.
There is a topic for each application environment:

- [Development SNS Topic Definition](https://github.com/ministryofjustice/cloud-platform-environments/blob/main/namespaces/live.cloud-platform.service.justice.gov.uk/hmpps-domain-events-dev/resources/hmpps-domain-events-topic.tf)
- [PreProd SNS Topic Definition](https://github.com/ministryofjustice/cloud-platform-environments/blob/main/namespaces/live.cloud-platform.service.justice.gov.uk/hmpps-domain-events-preprod/resources/hmpps-domain-events-topic.tf)
- [Production SNS Topic Definition](https://github.com/ministryofjustice/cloud-platform-environments/blob/main/namespaces/live.cloud-platform.service.justice.gov.uk/hmpps-domain-events-prod/resources/hmpps-domain-events-topic.tf)

Message filtering for SQS queues may be done using the `eventType` message
attribute.

## Tooling

Message flows in the development environment can be viewed using the
[Offender Events UI](https://offender-events-ui-dev.prison.service.justice.gov.uk/messages)

Domain event messages in all environments are logged to Application Insights
via the [HMPPS Domain Event Logger](https://github.com/ministryofjustice/hmpps-domain-event-logger)

Validation of example messages:
```shell
check-jsonschema --schemafile=schema/hmpps-domain-event.json <example-message.json>
```

Validation of AsyncAPI message schemas:
```shell
check-jsonschema --verbose --schemafile=https://asyncapi.com/definitions/3.0.0/messageObject.json ./spec/schemas/[path-to.yml]
```
