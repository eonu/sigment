import pytest
import numpy as np
from sigment.internals import _Validator

val = _Validator()

# ==================== #
# _Validator.integer() #
# ==================== #

def test_integer():
    assert True is not False