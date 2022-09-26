""" Main entry point module.
"""
import sys

from app.jira import execute_jql
from app.parser import process_jira
from app.printer import print_results


def main(days = -1):
    """
    Main entry point.
    """
    jira_result = execute_jql(days)
    tickets, pr_review = process_jira(jira_result, days=days)
    print_results(tickets, pr_review)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Invalid arguments provided.")
        sys.exit(1)

    DAYS_INPUT = sys.argv[1].strip()
    main(int(DAYS_INPUT))
