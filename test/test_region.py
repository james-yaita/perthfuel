# Import from a parent directory
import os
import sys
import inspect
import pytest
import urllib.parse

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import data.region


def my_assert(expected, actual, message):
    result = expected == actual

    preamble = "FAIL"
    if result:
        preamble = "PASS"

    print(f"{preamble} for {message}. Expected: {expected} Actual: {actual} ")
    return result


def test_find_region():
    assert(my_assert(15, data.region.find_id("Albany"),
                     "Check standard region is found"))
    assert(my_assert(28, data.region.find_id("Augusta / Margaret River"),
                     "Check region with slash is found"))
    assert(my_assert(3, data.region.find_id("Busselton (Townsite)"),
                     "Check region with brackets is found"))
    assert(my_assert(27, data.region.find_id("Metro : East & Hills"),
                     "Check with colon and ampersand is found"))
    assert(my_assert(56, data.region.find_id("York"),
                     "Check last region is found"))
    assert(my_assert(None, data.region.find_id("Imagine"),
                     "Check non existent region returns false"))
    assert(my_assert(None, data.region.find_id(None),
                     "Check None returns false"))
    assert(my_assert(None, data.region.find_id(5),
                     "Check None returns false"))
    assert(my_assert(None, data.region.find_id(""),
                     "Check empty string returns false"))
    assert(my_assert(None, data.region.find_id([""]),
                     "Check list item returns false"))


if __name__ == '__main__':
    test_find_region()