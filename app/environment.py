""" Environment module.
"""
import logging
import sys

from environment import Environment
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logging.info("%s:%s", __name__, "Loading environment ...")
load_dotenv()

env = Environment(
  QW_ENVIRONMENT=str,
  QW_JIRA_HOST=str,
  QW_JIRA_ENDPOINT=str,
  QW_JIRA_USER=str,
  QW_JIRA_SECRET=str
)

logging.info("%s:%s=%s", __name__, "ENVIRONMENT", env.qw_environment)

ENV=str(env.qw_environment)
JIRA_HOST=str(env.qw_jira_host)
JIRA_ENDPOINT=str(env.qw_jira_endpoint)
JIRA_USER=str(env.qw_jira_user)
JIRA_SECRET=str(env.qw_jira_secret)
