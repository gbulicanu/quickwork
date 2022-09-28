""" JIRA JSON Parser module.
"""
from datetime import date, datetime, timedelta

from jsonpath_ng.ext import parse

from app.environment import JIRA_USER


def __filter_worklog(current, from_date):
    current_dt = datetime.strptime(current["started"], '%Y-%m-%dT%H:%M:%S.%f%z')
    return current_dt.date() >= from_date

def process_jira(jira_result, days=-1):
    """ Process JIRA JSON result.
    """
    tickets = {}
    pr_review = {}
    from_time = date.today() + timedelta(days=days)

    for issue_key in [match.value for match in parse("$.issues[*].key").find(jira_result)]:
        issue = [match.value for match \
            in parse(f"$.issues[?(@.key='{issue_key}')]").find(jira_result)][0]
        json_path_worklogs = parse(
            f"$.fields.worklog.worklogs[?(@.author.emailAddress='{JIRA_USER}' \
              & @.started >= '{from_time}')]")
        json_path_comment = parse("comment.content[0].content[0].text")
        worklogs = filter(
            lambda x: __filter_worklog(x, from_time),
            [match.value for match in json_path_worklogs.find(issue)])
        for worklog in worklogs:
            comment = ([match.value for match in json_path_comment.find(worklog)] or [None])[0]
            time_spent = [match.value for match in parse("timeSpentSeconds").find(worklog)][0]
            if comment is not None and comment.strip().lower() == "pr review":
                if not issue_key in pr_review:
                    pr_review[issue_key] = int(time_spent)
                else:
                    pr_review[issue_key] += int(time_spent)
            else:
                if issue_key in tickets:
                    comments_set, ticket_spent_time = tickets[issue_key]
                    if comment is not None:
                        comments_set.add(comment.strip())
                    else:
                        comments_set.add("Missing")
                    tickets[issue_key] = (comments_set, ticket_spent_time + time_spent)
                else:
                    if comment is not None:
                        tickets[issue_key] = ({ comment.strip() }, time_spent)
                    else:
                        tickets[issue_key] = ({ "Missing" }, time_spent)

    return tickets, pr_review
