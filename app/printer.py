import pyperclip

from datetime import timedelta

from .utils import strfdelta


def print_results(tickets, pr_review, print_time = False, print_to_clipboard = True):
  lines = []

  for key, (comments, time_in_secs) in tickets.items():
    comments_list = list(comments)
    comments_list.sort()
    if print_time:
      time_rep = strfdelta(timedelta(seconds=int(time_in_secs)), '{H}h {M}m')
      lines.append("* {} - {} - {}".format(key, ", ".join(comments), time_rep))
    else:
      lines.append("* {} - {}".format(key, ", ".join(comments)))

  lines.append("")

  if print_time:
    pr_seconds = sum(pr_review.values())
    pr_time_rep = strfdelta(timedelta(seconds=int(pr_seconds)), '{H}h {M}m')
    lines.append("PR Review(s) - {}".format(pr_time_rep))
  else:
    lines.append("PR Review(s):")

  for pr in pr_review.keys():
    lines.append("* {}".format(pr))

  status = '\n'.join(lines)
  print(status)

  if print_to_clipboard:
    pyperclip.copy(status)
