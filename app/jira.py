""" JIRA module.
"""
import json
import logging
import requests

from requests.auth import HTTPBasicAuth

from .environment import JIRA_ENDPOINT, JIRA_USER, JIRA_SECRET


def execute_jql(from_days = None, max_results = 10):
    """ Execute JIRA JQL against configured Atlassian jira account.
    """
    if from_days == 0:
        from_days = None

    auth = HTTPBasicAuth(JIRA_USER, JIRA_SECRET)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    from_days_or_empty = from_days or ""
    jql = f"worklogAuthor = currentUser() AND worklogDate >= startOfDay({from_days_or_empty})" \
    .format()

    payload = json.dumps({
        "expand": [],
        "jql": jql,
        "maxResults": max_results,
        "fieldsByKeys": False,
        "fields": [
            "summary",
            "status",
            "worklog",
        ],
        "startAt": 0
    })

    response = requests.request(
        "POST",
        JIRA_ENDPOINT,
        data=payload,
        headers=headers,
        auth=auth
    )

    result = json.loads(response.text)
    logging.info("%s:'%s' jql executed", __name__, jql)
    # logging.debug("result from jql: \n%s", json.dumps(result, indent=2))

    return result
