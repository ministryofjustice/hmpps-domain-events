#!/usr/bin/env python3

""" Generate an ASyncAPI Message Spec from an HMPPS Domain Event Message """

import argparse
import os
import requests
import sys
import json
import yaml
from collections import OrderedDict


def application_insights_request(event_type):
    APP_INSIGHTS_APPLICATION_GUID = os.environ["APP_INSIGHTS_APPLICATION_GUID"]
    APP_INSIGHTS_API_KEY = os.environ["APP_INSIGHTS_API_KEY"]

    query = f""" customEvents
         | where cloud_RoleName in ('hmpps-domain-event-logger')
         | where name == '{event_type}'
         | where timestamp between((ago(3d)) .. now())
    """

    params = {"query": query}
    headers = {"X-Api-Key": APP_INSIGHTS_API_KEY}

    url = f"https://api.applicationinsights.io/v1/apps/{APP_INSIGHTS_APPLICATION_GUID}/query"

    response = requests.get(url, headers=headers, params=params)

    full_response = json.loads(response.text)

    # Do we have any messages?
    if len(full_response["tables"][0]["rows"]) == 0:
        sys.exit(
            f"No domain event message found for '{event_type}' in Application Insights in the previous three days"
        )

    raw_message = json.loads(full_response["tables"][0]["rows"][0][3])["rawMessage"]
    single_message_json = json.loads(json.loads(raw_message)["Message"])

    return single_message_json


def api_string(field, value):
    node = OrderedDict(
        {
            "type": "string",
            "example": value,
        }
    )

    return node


def api_int(field, value):
    node = OrderedDict(
        {
            "type": "integer",
            "example": value,
        }
    )

    return node


def api_object(field, value):
    node = OrderedDict(
        {
            "type": "object",
            "properties": {},
        }
    )

    for sub_field in value:
        node["properties"][sub_field] = process_field(sub_field, value[sub_field])

    return node


def api_list(field, value):
    node = OrderedDict({"type": "array", "items": []})

    for item in value:
        node["items"].append(process_field("list_item", item))

    return node


def process_field(field, value):
    type_name = type(value).__name__

    if type_name == "str":
        field = api_string(field, value)

    if type_name == "int":
        field = api_int(field, value)

    if type_name == "dict":
        field = api_object(field, value)

    if type_name == "list":
        field = api_list(field, value)

    return field


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an AsyncAPI message spec from an HMPPS domain event message."
    )
    parser.add_argument("event", type=str, help="An HMPPS domain event type")
    args = parser.parse_args()

    # Grab a single application insights domain event message
    message = application_insights_request(args.event)

    new_message = OrderedDict({})
    new_message["name"] = message["eventType"]
    new_message["title"] = message["eventType"]
    new_message["summary"] = message["description"]
    new_message["contentType"] = "application/json"
    new_message["payload"] = OrderedDict({"type": "object", "properties": {}})

    for field in message:
        new_message["payload"]["properties"][field] = process_field(
            field, message[field]
        )

    yaml.add_representer(
        OrderedDict,
        lambda dumper, data: dumper.represent_mapping(
            "tag:yaml.org,2002:map", data.items()
        ),
    )

    print(yaml.dump(new_message))
