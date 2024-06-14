from collections import OrderedDict
import yaml


def api_string(value):
    node = OrderedDict(
        {
            "type": "string",
            "example": value,
        }
    )

    return node


def api_int(value):
    node = OrderedDict(
        {
            "type": "integer",
            "example": value,
        }
    )

    return node


def api_object(value):
    node = OrderedDict(
        {
            "type": "object",
            "properties": {},
        }
    )

    for sub_field in value:
        node["properties"][sub_field] = process_field(sub_field, value[sub_field])

    return node


def api_list(value):
    node = OrderedDict({"type": "array", "items": []})

    for item in value:
        node["items"].append(process_field("list_item", item))

    return node


def process_field(field, value):
    type_name = type(value).__name__

    if type_name == "str":
        field = api_string(value)

    if type_name == "int":
        field = api_int(value)

    if type_name == "dict":
        field = api_object(value)

    if type_name == "list":
        field = api_list(value)

    return field


def create_asyncapi_yaml(message):

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

    return yaml.dump(new_message)
