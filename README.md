# HMPPS Domain Events

Specification of the set of HMPPS Domain Events published by HMPPS services.

JSON Schema for domain events is [here](./schema/hmpps-domain-event.json)

ASyncAPI schemas for individual messages [here](./spec/schemas/)

Validation of example messages:
```sh
check-jsonschema --schemafile=schema/hmpps-domain-event.json <example-message.json>
```
