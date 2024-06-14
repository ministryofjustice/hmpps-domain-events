#!/usr/bin/env python3

""" Generate an ASyncAPI Message Spec from an HMPPS Domain Event Message """

import argparse
import lib.asyncapi
import lib.application_insights


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an AsyncAPI message spec from an HMPPS domain event message."
    )
    parser.add_argument("event", type=str, help="An HMPPS domain event type")
    args = parser.parse_args()

    # Grab a single application insights domain event message
    message = lib.application_insights.single_domain_event(args.event)

    # Write an ASyncAPI YAML message based on the event
    print(lib.asyncapi.create_asyncapi_yaml(message))
