"""Main entry point module."""

import argparse
import sys

from app.jira import add_worklog, execute_jql
from app.parser import process_jira
from app.printer import print_results


__version__ = "0.1.1"


def report(local_args):
    """
    Reports sub-command handler.
    """
    day = 0
    day_arg = local_args.day
    print_time = bool(local_args.print_time)
    try:
        day = int(day_arg)
    except ValueError:
        if day_arg in ("yesterday", "y"):
            day = -1

    jira_result = execute_jql(day)
    tickets, pr_review = process_jira(jira_result, days=day)
    print_results(tickets, pr_review, print_time=print_time)


def log_work(local_args):
    """
    Low work sub-command handler.
    """
    add_worklog(local_args.issue_key, local_args.time, local_args.comment)


parser = argparse.ArgumentParser(
    prog="qw", description="Quickwork - developer personal admin cli."
)
subparsers = parser.add_subparsers()

report_parser = subparsers.add_parser("report", aliases=["r"])
report_parser.add_argument(
    "day",
    type=str,
    default="t",
    choices=["today", "t", "yesterday", "y", "-2", "-3", "-4"],
    help="Day to build report for.",
)

report_parser.add_argument(
    "--print-time", action="store_true", help="Print time in generated report."
)

report_parser.set_defaults(func=report)

log_parser = subparsers.add_parser("log", aliases=["l"])
log_parser.add_argument(
    "--issue-key",
    "-k",
    type=str,
    help="Issue tracker number (JIRA i.e. PROJ-311) (default "
    "first in progress ticket found for current user) .",
)

log_parser.add_argument(
    "--time",
    "-t",
    type=str,
    default="5m",
    help="Time amount to to log (default '5m' five minutes).",
)

log_parser.add_argument(
    "--comment",
    "-c",
    type=str,
    default="PR Review",
    help="Comment to add to work log (default 'PR Review').",
)

log_parser.set_defaults(func=log_work)

if __name__ == "__main__":
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args.func(args)
