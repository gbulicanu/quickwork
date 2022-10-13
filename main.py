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
    jira_result = execute_jql(int(local_args.days))
    tickets, pr_review = process_jira(jira_result, days=int(local_args.days))
    print_results(tickets, pr_review)

parser = argparse.ArgumentParser(
    description="Quickwork - developer personal admin cli."
)
subparsers = parser.add_subparsers()

report_parser = subparsers.add_parser("report", aliases=["r"])
report_parser.add_argument(
    "days",
    default=-1,
    help="Days delta to build report for.")  # add the name argument
report_parser.set_defaults(func=report)  # set the default function to report

if __name__ == "__main__":
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args.func(args)  # call the default function
