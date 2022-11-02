""" JIRA tests module.
"""
import json
import pytest

from pytest_mock import MockerFixture
from requests_mock import Mocker

from app.environment import JIRA_ENDPOINT
from app.jira import add_worklog, execute_jql
from tests.utils import anything


@pytest.mark.parametrize(["from_days", "expected_jql"], [
    (None, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (0, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (1, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (-1, "worklogAuthor = currentUser() AND worklogDate >= startOfDay(-1)"),
    (-2, "worklogAuthor = currentUser() AND worklogDate >= startOfDay(-2)"),
])
def test_execute_jql(from_days, expected_jql, mocker: MockerFixture, requests_mock: Mocker):
    """ Test execute_jql.
    """
    response_text = "{}"
    request_matcher = requests_mock.request(
        method="POST",
        url=f"{JIRA_ENDPOINT}/search",
        text=response_text)
    logging_info_patcher = mocker.patch("logging.info")
    assert execute_jql(from_days) == json.loads(response_text)
    assert request_matcher.last_request.json()["jql"] == expected_jql
    logging_info_patcher.assert_called_with("%s:'%s' jql executed", "app.jira", expected_jql)


def test_add_worklog_with_none_issue_key_will_get_current(
    mocker: MockerFixture,
    requests_mock: Mocker
):
    """ Test add_worklog with issue_key: None
    """
    response_text = '{"issues": [{"key": "TEST-01"}]}'
    request_matcher = requests_mock.request(
        method="POST",
        url=f"{JIRA_ENDPOINT}/search",
        text=response_text)
    requests_mock.request(
        method="POST",
        url=f"{JIRA_ENDPOINT}/issue/TEST-01/worklog",
        text="{}")
    logging_info_patcher = mocker.patch("logging.info")
    add_worklog(None, "5m", "PR Review")
    current_ticket_request_json = request_matcher.request_history[0].json()
    assert current_ticket_request_json["jql"] \
           == "assignee = currentUser() AND status = 'IN PROGRESS'"
    assert current_ticket_request_json["fields"] == ["summary"]
    assert current_ticket_request_json["maxResults"] == 1
    logging_info_patcher.assert_called_with(
        anything(str),
        anything(str),
        "TEST-01",
        anything(str),
        anything(str))


def test_add_worklog_will_log_error_on_failed_post_to_jira(
    mocker: MockerFixture,
    requests_mock: Mocker
):
    """ Test add_worklog with posting to jira failing.
    """
    requests_mock.request(
        method="POST",
        url=f"{JIRA_ENDPOINT}/issue/TEST-01/worklog",
        text="{}",
        status_code=401,
        reason="Bad Request")
    logging_error_patcher = mocker.patch("logging.error")
    add_worklog("TEST-01", "5m", "PR Review")
    logging_error_patcher.assert_called()
