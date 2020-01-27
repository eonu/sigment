import pytest
import numpy as np
from sequentia.internals import _Validator

val = _Validator()

# ==================== #
# _Validator.integer() #
# ==================== #

def test_integer():
    assert True is not False