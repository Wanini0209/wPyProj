# -*- coding: utf-8 -*-
"""Tests for Text-Utilities.

Created on Thu Sep 29 12:24:30 2022

@author: Wanini
"""

import os

from samples._libs._utils import read_text, write_text


def test_write_and_read_text():
    """Test for `write_text` and `read_text` functions."""
    text = 'Hollow world'
    file = '_tempory_file_for_test_write_and_read_text.txt'
    write_text(text, file)
    assert text == read_text(file)
    os.remove(file)
