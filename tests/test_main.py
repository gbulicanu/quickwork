""" main.py test module.
"""

import pytest

from pytest_mock import MockerFixture

from main import create_parser, log_work, main, report


def test_create_parser_returns_parser():
    """ Test create_parser returns an ArgumentParser. """
    import argparse
    arg_parser = create_parser()
    assert isinstance(arg_parser, argparse.ArgumentParser)


@pytest.mark.parametrize(["argv", "expected_day", "expected_print_time"], [
    (["report", "today"], 0, False),
    (["r", "t"], 0, False),
    (["report", "yesterday"], -1, False),
    (["r", "y"], -1, False),
    (["report", "-2"], -2, False),
    (["report", "-3"], -3, False),
    (["report", "-4"], -4, False),
    (["report", "today", "--print-time"], 0, True),
])
def test_report_sub_command(argv, expected_day, expected_print_time, mocker: MockerFixture):
    """ Test report sub-command calls correct functions with correct arguments. """
    execute_jql_patcher = mocker.patch("main.execute_jql", return_value={})
    process_jira_patcher = mocker.patch("main.process_jira", return_value=({}, {}))
    print_results_patcher = mocker.patch("main.print_results")

    arg_parser = create_parser()
    args = arg_parser.parse_args(argv)
    args.func(args)

    execute_jql_patcher.assert_called_once_with(expected_day)
    process_jira_patcher.assert_called_once_with({}, days=expected_day)
    print_results_patcher.assert_called_once_with({}, {}, print_time=expected_print_time)


@pytest.mark.parametrize(["argv", "expected_issue_key", "expected_time", "expected_comment"], [
    (["log"], None, "5m", "PR Review"),
    (["l", "--issue-key", "TEST-01"], "TEST-01", "5m", "PR Review"),
    (["log", "-k", "TEST-02", "-t", "1h", "-c", "Development"], "TEST-02", "1h", "Development"),
])
def test_log_work_sub_command(
    argv,
    expected_issue_key,
    expected_time,
    expected_comment,
    mocker: MockerFixture
):
    """ Test log sub-command calls add_worklog with correct arguments. """
    add_worklog_patcher = mocker.patch("main.add_worklog")

    arg_parser = create_parser()
    args = arg_parser.parse_args(argv)
    args.func(args)

    add_worklog_patcher.assert_called_once_with(expected_issue_key, expected_time, expected_comment)


def test_main_prints_help_when_no_subcommand(mocker: MockerFixture):
    """ Test main prints help when invoked without a sub-command. """
    mocker.patch("sys.argv", ["qw"])
    print_help_patcher = mocker.patch("argparse.ArgumentParser.print_help")
    main()
    print_help_patcher.assert_called_once()


def test_main_calls_subcommand_func(mocker: MockerFixture):
    """ Test main calls the sub-command handler when a valid sub-command is provided. """
    mocker.patch("sys.argv", ["qw", "report", "today"])
    mocker.patch("main.execute_jql", return_value={})
    mocker.patch("main.process_jira", return_value=({}, {}))
    print_results_patcher = mocker.patch("main.print_results")
    main()
    print_results_patcher.assert_called_once()
