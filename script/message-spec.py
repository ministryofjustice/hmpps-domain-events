#!/usr/bin/env python3

""" Generate an ASyncAPI Message Spec from an HMPPS Domain Event Message """

import argparse
import lib.asyncapi
import lib.application_insights
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an AsyncAPI message spec from an HMPPS domain event message."
    )
    parser.add_argument("event", type=str, help="An HMPPS domain event type")
    parser.add_argument("-j", "--json", action="store_true")
    args = parser.parse_args()

    # Grab a single application insights domain event message
    message = lib.application_insights.single_domain_event(args.event)

    if args.json:
        print(json.dumps(message))
    else:
        # Write an ASyncAPI YAML message based on the event
        print(lib.asyncapi.create_asyncapi_yaml(message))
