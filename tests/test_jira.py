""" JIRA tests module.
"""
import json

from pytest_mock import MockerFixture
from requests_mock import Mocker

from app.environment import JIRA_ENDPOINT
from app.jira import execute_jql

def test_execute_jql_default(mocker: MockerFixture, requests_mock: Mocker):
    """ Test execute_jql default.
    """
    response_text = "{}"
    requests_mock.request(
        method="POST",
        url=JIRA_ENDPOINT,
        text=response_text)
    mocker.patch("logging.info")
    assert execute_jql() == json.loads(response_text)

def test_execute_jql_zero(mocker: MockerFixture, requests_mock: Mocker):
    """ Test execute_jql zero days.
    """
    response_text = "{}"
    requests_mock.request(
        method="POST",
        url=JIRA_ENDPOINT,
        text=response_text)
    mocker.patch("logging.info")
    assert execute_jql(from_days=0) == json.loads(response_text)
