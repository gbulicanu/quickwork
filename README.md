# Quickwork (qw)

A personal productivity CLI for logging and reporting work time against JIRA — built to collapse two daily chores (logging time, reporting what you did) into single terminal commands instead of clicking through the JIRA UI.

## Why this exists

JIRA is a solid system of record but a slow tool for two very common rituals:

- **"What did I work on today/yesterday?"** — normally means clicking through JIRA's UI, filtering tickets, and manually compiling a summary to paste into standup notes, a status update, or a timesheet.
- **"Log 5 minutes for that PR review."** — a tiny, frequent task that doesn't deserve a full trip through a web form.

This got worse when juggling **two clients at once**, each with their own JIRA host and account. Switching contexts in a browser made it easy to lose track of which tab belonged to which client — and easy to under-report or forget time for whichever client wasn't top-of-mind that day.

`qw` is a thin, opinionated CLI wrapper around the JIRA REST API that encodes sensible defaults (first in-progress ticket, `5m`, `"PR Review"`) and per-client configuration, so both rituals become fast, low-friction terminal commands — and reporting doesn't quietly fall through the cracks when splitting time across multiple clients.

## Features

- `qw log` — log work time against a JIRA ticket, with smart defaults for ticket, duration, and comment
- `qw report` — pull a summary of work for a given day (`today`, `yesterday`, or a relative offset) and copy it straight to your clipboard, ready to paste into Slack/standup notes/timesheets
- Config-driven, per-client setup via `.env` — swap between JIRA hosts/accounts without touching code
- Flexible JQL-based querying instead of hardcoded filters
- Distributed as standalone cross-platform binaries (no Python install required) via PyInstaller + GitHub Releases

## Installation

### Option 1: Prebuilt binary (recommended)

Download the latest release for your OS from the [Releases page](https://github.com/gbulicanu/quickwork/releases) and place the binary on your `PATH`.

### Option 2: From source

```bash
git clone https://github.com/gbulicanu/quickwork.git
cd quickwork
pipenv install
pipenv run python main.py --help
```

## Configuration

Copy `.env.template` to `.env` and fill in your JIRA host and credentials:

```bash
cp .env.template .env
```

If you work across multiple clients, keep a separate `.env` profile per client and point `qw` at the right one for your current context.

## Usage

```bash
# Log 5 minutes as "PR Review" against your current in-progress ticket
qw log

# Log 30 minutes against a specific ticket with a custom comment
qw log -k QW-123 -t 30m -c "Implement retry logic"

# Report what you worked on today (copies to clipboard)
qw report today

# Report yesterday's work
qw report yesterday
```

Run `qw --help` for the full command reference.

## Contributing

Issues labeled [`good first issue`](https://github.com/gbulicanu/quickwork/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are small, well-scoped, and a good place to start. Open a PR against `main` and reference the issue it resolves.

## Documentation

Comprehensive documentation lives in [`docs/`](docs/) (in progress) — covering configuration in depth, multi-client setup, and internal architecture. See open issues for the current documentation roadmap.

## License

TBD.
