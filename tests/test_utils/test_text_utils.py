"""Tests for text utilities."""

import os

from samples._libs._utils import read_text, write_text


def test_write_and_read_text():
    """Test for `write_text` and `read_text` functions."""
    text = "Hello world"
    file = "_temporary_file_for_test_write_and_read_text.txt"
    write_text(text, file)
    assert text == read_text(file)
    os.remove(file)
