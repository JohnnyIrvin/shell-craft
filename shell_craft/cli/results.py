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
from argparse import ArgumentParser, ArgumentTypeError

def limited_float(min: float, max: float):
    def _ret_func(arg: str):
        if not str(arg).isdecimal:
            raise ArgumentTypeError(f"{arg} is not a decimal")
        
        f = float(arg)
        if f < min or f > max:
            raise ArgumentTypeError(f"{arg} is not between {min} and {max}")
        
        return f
    
    return _ret_func


def add_arguments(parser: ArgumentParser):
    """
    Adds arguments that effect the results of the openai api call.

    '--count (-c)' is used to specify the number of results to return.
    '--temperature (-t)' is used to specify the sampling temperature to use.

    Args:
        parser (ArgumentParser): The parser to add the arguments to.
    """    
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="The number of results to return.",
    )

    parser.add_argument(
        "-t",
        "--temperature",
        type=limited_float(0.0, 2.0),
        default=1.0,
        help="The sampling temperature to use. Must be between 0 and 2.",
    )