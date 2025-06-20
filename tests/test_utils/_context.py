# -*- coding: utf-8 -*-
"""Context common used in test modules in this package.

Created on Thu Sep 29 12:32:59 2022

@author: Wanini
"""

import os
import sys

_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, _PROJECT_PATH)

# pylint: disable=wrong-import-position, unused-import, wrong-import-order
from samples._libs._utils import read_text, write_text  # noqa: E402, F401

# pylint: enable=wrong-import-position, unused-import, wrong-import-order
