""" Main entry point module.
"""
import argparse
import sys

from app.jira import execute_jql
from app.parser import process_jira
from app.printer import print_results

def report(local_args):
    """
    Reports sub-command main entry point.
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

parser = argparse.ArgumentParser(
    prog="qw",
    description="Quickwork - developer personal admin cli."
)
subparsers = parser.add_subparsers()

report_parser = subparsers.add_parser("report", aliases=["r"])
report_parser.add_argument(
    "day",
    type=str,
    default="t",
    choices=["today", "t", "yesterday", "y", "-2", "-3", "-4"],
    help="Day to build report for.")

report_parser.add_argument(
    "--print-time",
    type=bool,
    default=False,
    choices=[False, True],
    help="Print time in generated report.")
report_parser.set_defaults(func=report)

if __name__ == "__main__":
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args.func(args)
