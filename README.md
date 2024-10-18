# HMPPS Domain Events

This repository serves as a reference point for all the published domain events.

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

## Working with this repository

The domain events that have been manually added can be found under spec/schemas. They are then divided according to the
prefix of the event, which normally indicates which system(s) publish the event.

Failing that, under spec/auto contains all the auto discovered domain event that have yet to be claimed. These files
have been created by dumping the recent events from our dev environment and then converting them to yaml files.

## Creating event publishing documentation

There are two parts to providing documentation about what events your service publishes / consumes.

### Documenting the individual messages

These go into this repository under spec/schemas. There should be a separate file per event, together with examples
to make it easier for people to visualise the payload.

### Documenting the publishing

In your own repository create an `asyncapi.yml` file which should contain all the events that your service publishes.  
An [example file](https://github.com/ministryofjustice/hmpps-restricted-patients-api/blob/main/async-api.yml) can be
found in restricted patients. This file shows that there are three events published by restricted patients and each
message contains a `$ref` linking to the individual message definitions in this repository. Your README.md can then
contain a badge and a link to open that file in asyncapi.com, again
see [restricted patients README](https://github.com/ministryofjustice/hmpps-restricted-patients-api/blob/main/README.md?plain=1)
for an example.

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

### Scripts

`script/message-spec.py` can be used to go to application insights to get the message json and / or yaml. You'll need to
run:

```shell
python3 -m venv .venv
source .venv/bin/activate
cd script
pip3 install -r requirements.txt
```

to create a virtual environment and install the requirements to run the script. The script requires two environment
variables set:

1. `APP_INSIGHTS_APPLICATION_GUID`. This can be found in application insights by going into the environment page and
   then clicking on the JSON view. It can be found in `properties.AppId`.
2. `APP_INSIGHTS_API_KEY`. This needs to be generated for you by #ask-digital-studio-ops e.g. see
   https://mojdt.slack.com/archives/C6D94J81E/p1728051239823909.

Note that if retrieving messages from systems other than dev, the example data needs to be changed so that it doesn't
refer to real prisoners etc.

