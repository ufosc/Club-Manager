"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


# mocking check command to simulate response
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(TestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # when check is called, just return true to mock ready
        patched_check.return_value = True

        # tests if db ready and if command is setup properly
        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")  # mocks sleep command so don't have to wait
    # add arguments from "inside-out"
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting operationalError."""
        # mock raising an exception with .side_effect
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )
        # first 2 times called, raise psycopg2error
        # then next 3 times raise operationalerror
        # need this to test catching both.
        # number of times called is variable/relative

        call_command("wait_for_db")

        # only call command 6 times (2 + 3 + 1)
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
