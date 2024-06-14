#!/usr/bin/env python3

""" Generate ASyncAPI Message Specs from HMPPS Domain Event Messages """

import argparse
import re
import os
import requests
import sys
import json
import yaml
import hiyapyco
import pathvalidate
import lib.application_insights
import lib.asyncapi

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AsyncAPI message specs from HMPPS domain event messages."
    )

    # Change working dir to script location
    os.chdir(sys.path[0])

    # Find all the recent domain event messages
    domain_event_types = lib.application_insights.domain_event_types()

    # Query Application Insights for each specific domain event message content
    for domain_event_type in domain_event_types:
        message = lib.application_insights.single_domain_event(domain_event_type)
        message_yaml = lib.asyncapi.create_asyncapi_yaml(message)

        path_parts = domain_event_type.split(".")
        dir, filename = path_parts[0], "-".join(path_parts[1:])

        # Remove special characters from file path
        alphanum_dir = re.sub(r"[^\w\d-]", "", dir)
        alphanum_filename = re.sub(r"[^\w\d-]", "", filename)
        sanitised_dir = pathvalidate.sanitize_filepath(alphanum_dir)
        sanitised_filename = pathvalidate.sanitize_filename(alphanum_filename) + ".yaml"

        # Merge with any local information
        override_yaml = None
        combined_message = None
        override_file = f"../spec/override/{sanitised_dir}/{sanitised_filename}"

        if os.path.exists(override_file):
            with open(override_file) as stream:
                override_yaml = stream.read()

        if override_yaml:
            combined_message = hiyapyco.load(
                message_yaml, override_yaml, method=hiyapyco.METHOD_MERGE
            )
        else:
            combined_message = yaml.safe_load(message_yaml)

        # Write to file system
        path = os.path.join("../spec/auto/", sanitised_dir)
        if not os.path.exists(path):
            os.makedirs(path)

        filepath = os.path.join(path, sanitised_filename)

        with open(filepath, "w") as file:
            file.write(yaml.dump(combined_message))
