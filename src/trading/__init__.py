"""
Initialize package.
"""
# https://docs.python-guide.org/writing/logging/

import logging

from .backtester import *

logging.getLogger(__name__).addHandler(logging.NullHandler())
