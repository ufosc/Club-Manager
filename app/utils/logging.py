"""
Logging and exception utils.
"""

import logging
import traceback

from app.settings import IS_TESTING_MODE


def print_error():
    """Log an error with stacktrace that's been handled via try/except."""
    if IS_TESTING_MODE:
        return

    tb = traceback.format_exc()
    logging.warning(tb)
