import os
import sys
import json
import requests


def ai_request(query):
    APP_INSIGHTS_APPLICATION_GUID = os.environ["APP_INSIGHTS_APPLICATION_GUID"]
    APP_INSIGHTS_API_KEY = os.environ["APP_INSIGHTS_API_KEY"]

    params = {"query": query}
    headers = {"X-Api-Key": APP_INSIGHTS_API_KEY}

    url = f"https://api.applicationinsights.io/v1/apps/{APP_INSIGHTS_APPLICATION_GUID}/query"

    response = requests.get(url, headers=headers, params=params)
    return json.loads(response.text)


def single_domain_event(event_type):

    # Grab the custom events for a single event type
    query = f"""customEvents
         | where cloud_RoleName in ('hmpps-domain-event-logger')
         | where name == '{event_type}'
         | where timestamp between((ago(7d)) .. now())
         | order by timestamp desc
         | limit 1
    """

    full_response = ai_request(query)

    # Do we have any messages?
    if len(full_response["tables"][0]["rows"]) == 0:
        sys.exit(
            f"No domain event message found for '{event_type}' in Application Insights in the previous seven days"
        )

    raw_message = json.loads(full_response["tables"][0]["rows"][0][3])["rawMessage"]
    single_message_json = json.loads(json.loads(raw_message)["Message"])

    return single_message_json


def domain_event_types():

    # Grab all the domain event types from the last week
    query = f"""customEvents
         | where cloud_RoleName in ('hmpps-domain-event-logger')
         | where timestamp between((ago(7d)) .. now())
         | summarize count() by name
    """

    full_response = ai_request(query)

    # Do we have any messages?
    if len(full_response["tables"][0]["rows"]) == 0:
        sys.exit(
            f"No domain event messages found in Application Insights in the previous seven days"
        )

    return [msg[0] for msg in full_response["tables"][0]["rows"]]
