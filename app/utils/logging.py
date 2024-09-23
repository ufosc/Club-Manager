"""
Logging and exception utils.
"""

import logging
import traceback


def print_error():
    """Log an error with stacktrace that's been handled via try/except."""
    tb = traceback.format_exc()
    logging.warning(tb)
