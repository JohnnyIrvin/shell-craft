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
from argparse import ArgumentTypeError
from typing import Callable


def limited_float(min: float, max: float) -> Callable:
    """
    Create a function that will validate a float is between the given min and
    max values for use with argparse.

    Args:
        min (float): The minimum value for the float.
        max (float): The maximum value for the float.

    Returns:
        Callable: A function that will validate a float is between the given min
    """    
    def _ret_func(arg: str) -> float:
        if arg is None or not str(arg).isdecimal:
            raise ArgumentTypeError(f"{arg} is not a decimal")
        
        f = float(arg)
        if f in [float("inf"), float("-inf")]:
            raise ArgumentTypeError(f"{arg} is not a decimal")
        
        if f != f:
            raise ArgumentTypeError(f"{arg} is not a decimal")

        if f < min or f > max:
            raise ArgumentTypeError(f"{arg} is not between {min} and {max}")
        
        return f
    
    return _ret_func
