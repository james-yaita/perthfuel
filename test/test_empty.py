import os
import sys
import inspect
import pytest
import urllib.parse

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import empty


def test_empty():
    """
Mock no connection

No query

Only region_id

Only region_desc

Invalid region_id

Valid region_id

All region desc



    """
    return None