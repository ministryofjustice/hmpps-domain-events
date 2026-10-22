# Contacts domain events

This directory contains all domain event types published by the Personal Relationships API
(previously known as the Contacts API):

30 with the `contacts-api.*` prefix and newer events with the `personal-relationships-api.*` prefix.
They are grouped together by publishing service; the existing event names are unchanged.

Each YAML file defines one AsyncAPI message and includes a synthetic example payload. Event names,
record identifiers and person references follow the publisher in `hmpps-personal-relationships-api`.
`additionalInformation.source` distinguishes changes originating in DPS from changes received
through NOMIS synchronisation. `username` identifies the actor; system operations may use `SYS`.

## Deprecated active caseload field (VB-6932)

`additionalInformation.activeCaseLoadId` is deprecated and is no longer populated. The publisher
omits it from JSON when null. It remains an optional, deprecated property in the schemas so
consumers can recognise historical messages, which may contain a string value, and tolerate
messages where it is absent. Null is also permitted by the property schema.

Consumers must not require this field or use it to establish the prison context of a change.
The publisher does not provide a replacement field. This deprecation applies to every event
documented in this directory. The current examples omit the field.

## Current envelope representation

These schemas describe the existing publisher: `version` is the string `"1"`, and `occurredAt` is
a local ISO-8601 date-time without a UTC offset. The timestamp is therefore documented as a string,
without claiming RFC 3339 `date-time` conformance or an inferred timezone.

The repository-wide `schema/hmpps-domain-event.json` instead expects an integer version and a
timestamp with a timezone. Current Contacts payloads do not satisfy those parts of the generic
envelope schema. These message definitions preserve the actual contract; changing the publisher's
envelope representation requires a separate compatibility review.
