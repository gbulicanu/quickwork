""" JIRA tests module.
"""
import json
import pytest

from pytest_mock import MockerFixture
from requests_mock import Mocker

from app.environment import JIRA_ENDPOINT
from app.jira import execute_jql

@pytest.mark.parametrize(["from_days", "expected_jql"], [
    (None, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (0, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (1, "worklogAuthor = currentUser() AND worklogDate >= startOfDay()"),
    (-1, "worklogAuthor = currentUser() AND worklogDate >= startOfDay(-1)"),
    (-2, "worklogAuthor = currentUser() AND worklogDate >= startOfDay(-2)"),
])

def test_execute_jql(from_days, expected_jql, mocker: MockerFixture, requests_mock: Mocker):
    """ Test execute_jql default.
    """
    response_text = "{}"
    request_matcher = requests_mock.request(
        method="POST",
        url=JIRA_ENDPOINT,
        text=response_text)
    logging_info_patcher = mocker.patch("logging.info")
    assert execute_jql(from_days) == json.loads(response_text)
    assert request_matcher.last_request.json()["jql"] == expected_jql
    logging_info_patcher.assert_called_with("%s:'%s' jql executed", "app.jira", expected_jql)
