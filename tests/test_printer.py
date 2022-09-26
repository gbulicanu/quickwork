""" printer.py test module.
"""

import pytest

from pytest_mock import MockerFixture

from app.printer import print_results


@pytest.mark.parametrize([
    "tickets",
    "pr_reviews",
    "print_time",
    "expected_output"], [
        (
            {
                "TEST-10": ({"Debugging", "Testing"}, 5 * 60 * 60), # 5h
                "TEST-11": ({"Debugging", "Testing"}, 5 * 60 * 60),
            }, {
                "TEST-20": 5 * 60, # 5m
                "TEST-21": 5 * 60, # 5m
            },
            False,
            (
                "* TEST-10 - Debugging, Testing\n"
                "* TEST-11 - Debugging, Testing\n"
                "\n"
                "PR Review(s):\n"
                "* TEST-20\n"
                "* TEST-21"
            )
        ),
        (
            {
                "TEST-10": ({"Debugging", "Testing"}, 5 * 60 * 60), # 5h
                "TEST-11": ({"Debugging", "Testing"}, 5 * 60 * 60),
            }, {
                "TEST-20": 5 * 60, # 5m
                "TEST-21": 5 * 60, # 5m
            },
            True,
            (
                "* TEST-10 - Debugging, Testing - 5h\n"
                "* TEST-11 - Debugging, Testing - 5h\n"
                "\n"
                "PR Review(s) - 10m\n"
                "* TEST-20\n"
                "* TEST-21"
            )
        ),
    ])
def test_print_results(
    tickets,
    pr_reviews,
    print_time,
    expected_output,
    mocker: MockerFixture):
    """ Test print_results.
    """
    pyperclip_copy_patcher = mocker.patch("pyperclip.copy")
    print_patcher = mocker.patch("builtins.print")
    print_results(tickets, pr_reviews, print_time)
    print_patcher.assert_called_once_with(expected_output)
    pyperclip_copy_patcher.assert_called_once_with(expected_output)
