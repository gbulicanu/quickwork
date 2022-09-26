""" JIRA JSON Parser module.
"""
from datetime import date, datetime, timedelta

from jsonpath_ng.ext import parse


def __filter_worklog(current, from_date):
    current_dt = datetime.strptime(current["started"], '%Y-%m-%dT%H:%M:%S.%f%z')
    return current_dt.date() >= from_date

def process_jira(jira_result, days=-1):
    """ Process JIRA JSON result.
    """
    json_path_issues = parse("$.issues[*].key")
    issue_keys = [match.value for match in json_path_issues.find(jira_result)]
    non_pr_review = {}
    pr_review = {}
    from_time = date.today() + timedelta(days=days)

    for issue_key in issue_keys:
        json_path_issue = parse(f"$.issues[?(@.key='{issue_key}')]")
        issue = [match.value for match in json_path_issue.find(jira_result)][0]
        json_path_worklogs = parse(
            f"$.fields.worklog.worklogs[?(@.author.emailAddress='gheorghe@gocontractor.com' \
              & @.started >= '{from_time}')]")
        json_path_time_spends = parse("timeSpentSeconds")
        json_path_comment = parse("comment.content[0].content[0].text")
        worklogs = filter(
            lambda x: __filter_worklog(x, from_time),
            [match.value for match in json_path_worklogs.find(issue)])
        for worklog in worklogs:
            comment = ([match.value for match in json_path_comment.find(worklog)] or [None])[0]
            times_spends = [match.value for match in json_path_time_spends.find(worklog)][0]
            if comment is not None and comment.strip().lower() == "pr review":
                pr_review[issue_key]  = int(times_spends)
            else:
                if non_pr_review.get(issue_key) is not None:
                    comments_set, _ = non_pr_review[issue_key]
                    comments_set.add(comment.strip())
                else:
                    if comment is not None:
                        non_pr_review[issue_key] = ({ comment.strip() }, times_spends)
                    else:
                        non_pr_review[issue_key] = ({ "Missing" }, times_spends)

    return non_pr_review, pr_review
