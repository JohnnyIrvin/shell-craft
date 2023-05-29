# Copyright (c) 2023 Johnathan P. Irvin and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import pytest
from shell_craft.cli.types import limited_float
from argparse import ArgumentTypeError


@pytest.mark.parametrize(
    'value, min_value, max_value, expected',
    [
        (0.0, 0.0, 1.0, 0.0),
        (0.5, 0.0, 1.0, 0.5),
        (1.0, 0.0, 1.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.5, 0.0, 1.0, 0.5),
        (1.0, 0.0, 1.0, 1.0),
    ]
)
def test_limited_float(value: float, min_value: float, max_value: float, expected: float):
    assert limited_float(min_value, max_value)(value) == expected

@pytest.mark.parametrize(
    'value, min_value, max_value, expected',
    [
        (0.0, 0.0, 1.0, 0.0),
        (0.5, 0.0, 1.0, 0.5),
        (1.0, 0.0, 1.0, 1.0),
    ]
)
def test_limited_float_min(value: float, min_value: float, max_value: float, expected: float):
    assert limited_float(min_value, max_value)(value) == expected

@pytest.mark.parametrize(
    'value, min_value, max_value, expected',
    [
        (0.0, 0.0, 1.0, 0.0),
        (0.5, 0.0, 1.0, 0.5),
        (1.0, 0.0, 1.0, 1.0),
    ]
)
def test_limited_float_max(value: float, min_value: float, max_value: float, expected: float):
    assert limited_float(min_value, max_value)(value) == expected

@pytest.mark.parametrize(
    'value, min_value, max_value, exception',
    [
        (-1.0, 0.0, 1.0, ArgumentTypeError),
        (2.0, 0.0, 1.0, ArgumentTypeError),
        (float('inf'), 0.0, 1.0, ArgumentTypeError),
        (float('nan'), 0.0, 1.0, ArgumentTypeError),
        (float('-inf'), 0.0, 1.0, ArgumentTypeError),
        (None, 0.0, 1.0, ArgumentTypeError),
    ]
)
def test_limited_float_range_exception(value: float, min_value: float, max_value: float, exception: Exception):
    with pytest.raises(exception):
        limited_float(min_value, max_value)(value)