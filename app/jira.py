""" JIRA module.
"""
from datetime import datetime, timezone
import json
import logging

from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from .environment import JIRA_ENDPOINT, JIRA_TIMEOUT, JIRA_USER, JIRA_SECRET
from .utils import strpdelta

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def execute_jql(from_days=None, max_results=10):
    """ Execute JIRA JQL against configured Atlassian jira account.
    """
    if from_days is not None and from_days >= 0:
        from_days = None

    auth = HTTPBasicAuth(JIRA_USER, JIRA_SECRET)

    from_days_or_empty = from_days or ""
    jql = f"worklogAuthor = currentUser() AND worklogDate >= startOfDay({from_days_or_empty})"

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
        f"{JIRA_ENDPOINT}/search",
        data=payload,
        headers=headers,
        auth=auth,
        timeout=JIRA_TIMEOUT
    )

    result = json.loads(response.text)
    logging.info("%s:'%s' jql executed", __name__, jql)
    # logging.debug("result from jql: \n%s", json.dumps(result, indent=2))

    return result


def add_worklog(
    issue_key: Optional[str],
    time: Optional[str],
    comment: Optional[str]
):
    """ Add worklog to <issue_key> ticket (or to first assigned in progress ticket if None)
    """

    auth = HTTPBasicAuth(JIRA_USER, JIRA_SECRET)
    time_delta = strpdelta(time)
    now = datetime.now(timezone.utc)

    started = now - time_delta

    if issue_key is None:
        jql = "assignee = currentUser() AND status = 'IN PROGRESS'"

        payload = json.dumps({
            "expand": [],
            "jql": jql,
            "maxResults": 1,
            "fieldsByKeys": False,
            "fields": [
                "summary",
            ],
            "startAt": 0
        })

        response = requests.request(
            "POST",
            f"{JIRA_ENDPOINT}/search",
            data=payload,
            headers=headers,
            auth=auth,
            timeout=JIRA_TIMEOUT
        )

        # logging.info("%s:current_issue_key-json:%s",
        #              __name__, json.dumps(json.loads(response.text),
        #                                   sort_keys=True, indent=4, separators=(",", ": ")))
        issue_key_json = json.loads(response.text)
        issue_key = issue_key_json["issues"][0]["key"]
        comment = "Misc" if comment == "PR Review" else comment

    logging.info("%s:add_worklog(%s, %s, %s) executing",
                 __name__, issue_key, time, comment)

    started_iso = started.isoformat(timespec="milliseconds")
    payload = json.dumps({
        "timeSpentSeconds": time_delta.total_seconds(),
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{
                    "text": comment,
                    "type": "text"
                }]
            }]
        },
        "started": started_iso[:-3] + started_iso[-2:]
    })

    response = requests.request(
        "POST",
        f"{JIRA_ENDPOINT}/issue/{issue_key}/worklog",
        data=payload,
        headers=headers,
        auth=auth,
        timeout=JIRA_TIMEOUT,
    )

    if response.status_code > 299:
        logging.error("%s:http error: %d reason: %s body: %s",
                __name__, response.status_code, response.reason, response.json())
    else:
        logging.info("%s:add_worklog(%s, %s, %s) succeeded",
                    __name__, issue_key, time, comment)
