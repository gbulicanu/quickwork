""" parser.py test module.
"""

from datetime import date, timedelta
import json

from pybars import Compiler

from app.environment import JIRA_USER
from app.parser import process_jira


def test_module_name():
    """ Test module_name
    """
    assert "tests.test_parser" == __name__

def test_process_jira():
    """ Test process_jira
    """
    test_file_prefix = __name__.lower().replace("tests.", "")
    with open(f"tests/templates/{test_file_prefix}.handlebars", encoding="utf-8") as test_file:
        compiler = Compiler()
        test_template = compiler.compile(test_file.read())
        test_out = test_template({
            "yesterday_ymd": (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d"),
            "users": [{ "email": JIRA_USER }],
            "tickets" : [
                {
                    "id": "31032",
                    "key": "TEST-10",
                    "summary": "First test",
                    "status_name": "Dev Done",
                    "status_id": "10513",
                    "worklogs": [
                        {
                            "id": "11257",
                            "author_accountId": "target-account-id",
                            "updateAuthor_accountId": "target-account-id",
                            "author_email": JIRA_USER,
                            "updateAuthor_email": JIRA_USER,
                            "author_dn": "Target User",
                            "updateAuthor_dn": "Target User",
                            "time": 5 * 3600,
                            "comment": "Debugging"
                        },
                        {
                            "id": "11258",
                            "author_accountId": "other-account-id",
                            "updateAuthor_accountId": "other-account-id",
                            "author_dn": "Other User",
                            "updateAuthor_dn": "Other User",
                            "time": 5 * 3600,
                            "comment": "Some other comment"
                        },
                        {
                            "id": "11259",
                            "author_accountId": "target-account-id",
                            "updateAuthor_accountId": "target-account-id",
                            "author_email": JIRA_USER,
                            "updateAuthor_email": JIRA_USER,
                            "author_dn": "Target User",
                            "updateAuthor_dn": "Target User",
                            "time": 3 * 3600,
                            "comment": "Testing"
                        },
                        {
                            "id": "11260",
                            "author_accountId": "other-account-id",
                            "updateAuthor_accountId": "other-account-id",
                            "author_email": "other@company.com",
                            "updateAuthor_email": "other@company.com",
                            "author_dn": "Other User",
                            "updateAuthor_dn": "Other User",
                            "time": 2 * 3600,
                        },
                    ]
                },
                {
                    "id": "31033",
                    "key": "TEST-11",
                    "summary": "Second test",
                    "status_name": "In Progress",
                    "status_id": "10513",
                    "worklogs": [
                        {
                            "id": "11492",
                            "author_accountId": "target-account-id",
                            "updateAuthor_accountId": "target-account-id",
                            "author_email": JIRA_USER,
                            "updateAuthor_email": JIRA_USER,
                            "author_dn": "Target User",
                            "updateAuthor_dn": "Target User",
                            "time": 30 * 60,
                            "comment": "PR Review"
                        },
                        {
                            "id": "11493",
                            "author_accountId": "other-account-id",
                            "updateAuthor_accountId": "other-account-id",
                            "updateAuthor_email": "other@company.com",
                            "author_dn": "Other User",
                            "updateAuthor_dn": "Other User",
                            "time": 5 * 60,

                        },
                        {
                            "id": "11494",
                            "author_accountId": "target-account-id",
                            "updateAuthor_accountId": "target-account-id",
                            "author_email": JIRA_USER,
                            "updateAuthor_email": JIRA_USER,
                            "author_dn": "Target User",
                            "updateAuthor_dn": "Target User",
                            "time": 30 * 60,
                            "comment": "PR Review"
                        },
                        {
                            "id": "11495",
                            "author_accountId": "other-account-id",
                            "updateAuthor_accountId": "other-account-id",
                            "updateAuthor_email": "other@company.com",
                            "author_dn": "Other User",
                            "updateAuthor_dn": "Other User",
                            "time": 5 * 60,
                        },
                    ]
                }
            ],
        })
        tickets, pr_tickets = process_jira(json.loads(str(test_out)))
        comment, time = tickets["TEST-10"]

        assert tickets.get("TEST-10") is not None
        assert pr_tickets.get("TEST-11") is not None
        assert set(comment) == { "Testing", "Debugging" }
        assert int(time) == 28800
        assert int(pr_tickets["TEST-11"]) == 3600
