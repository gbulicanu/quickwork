""" Printing to stdout and clipboard.
"""
from datetime import timedelta

import pyperclip

from .utils import strfdelta


def print_results(tickets, pr_reviews, print_time = False, print_to_clipboard = True):
    """ Print results to stdout and clipboard.
    """
    lines = []

    for key, (comments, time_in_secs) in tickets.items():
        comments_list = list(comments)
        comments_list.sort()
        comments_str = ", ".join(comments_list)
        if print_time:
            time_rep = strfdelta(timedelta(seconds=int(time_in_secs)), '{H}h {M}m')
            lines.append(f"* {key} - {comments_str} - {time_rep}")
        else:
            lines.append(f"* {key} - {comments_str}")

    lines.append("")

    if print_time:
        pr_seconds = sum(pr_reviews.values())
        pr_time_rep = strfdelta(timedelta(seconds=int(pr_seconds)), '{H}h {M}m')
        lines.append(f"PR Review(s) - {pr_time_rep}")
    else:
        lines.append("PR Review(s):")

    for pr_reviews_keys in pr_reviews.keys():
        lines.append(f"* {pr_reviews_keys}")

    status = '\n'.join(lines)
    print(status)

    if print_to_clipboard:
        pyperclip.copy(status)
