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
from argparse import ArgumentParser

from shell_craft.prompts import PromptFactory
from shell_craft.prompts.templates import (BUG_REPORT_PROMPT,
                                           FEATURE_REQUEST_PROMPT)


ARGUMENTS = {
    'prompt': lambda x: PromptFactory.get_prompt(x) in [ BUG_REPORT_PROMPT, FEATURE_REQUEST_PROMPT ]
}

def add_arguments(parser: ArgumentParser):
    """
    Adds 'github' argument to the parser. This argument is used to
    specify the URL to the GitHub repository to open an issue or feature
    request for.

    Args:
        parser (ArgumentParser): The parser to add the argument to.
    """
    parser.add_argument(
        '--github',
        type=str,
        help='The URL to the GitHub repository to open an issue or feature request for.'
    )