import sys
import os
sys.path.insert(0, os.path.abspath(__file__))

import pytest

import hasm


@pytest.mark.parametrize(("filters", "data", "expected"), (
    ([], [], []),
    ([lambda x: x + 1], list(range(0, 5)), list(range(1, 6))),
    ([lambda x: x + 1, lambda x: x * 2], range(0, 5), range(2, 10, 2)),
))
def test_apply_filters(filters, data, expected):

    assert hasm.apply_filters(filters, data) == expected
