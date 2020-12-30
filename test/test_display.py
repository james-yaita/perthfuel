# Import from a parent directory
import os
import sys
import inspect
import pytest

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import view.display


def test_enclose_div():
    my_content = """\
this is the inner html.
"""
    result = view.display.enclose_in_div(my_content)
    assert(result == f"<div>{my_content}</div>" + os.linesep)

    result = view.display.enclose_in_div(my_content, element_class="class1")
    assert(result == f"<div class=\"class1\">{my_content}</div>" + os.linesep)

    result = view.display.enclose_in_div(my_content,
                                         element_class="class2",
                                         element_id="some_id")
    expected = f"<div class=\"class2\" id=\"some_id\">{my_content}</div>"
    expected += os.linesep
    assert(result == expected)

    result = view.display.enclose_in_div(my_content,
                                         element_id="some_id2")
    expected = f"<div id=\"some_id2\">{my_content}</div>" + os.linesep
    assert(result == expected)

    result = view.display.enclose_in_div(my_content,
                                         element_id="some_id3",
                                         element_class="class3")
    expected = f"<div class=\"class3\" id=\"some_id3\">{my_content}</div>"
    expected += os.linesep
    assert(result == expected)

    result = view.display.enclose_in_div(my_content,
                                         element_id="some_id3",
                                         element_class=None)
    expected = f"<div id=\"some_id3\">{my_content}</div>"
    expected += os.linesep
    assert(result == expected)

    return None


if __name__ == '__main__':
    test_enclose_div()