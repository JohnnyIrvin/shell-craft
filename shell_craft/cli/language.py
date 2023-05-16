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
from shell_craft.factories import PromptFactory
from shell_craft.prompts import languages

ARGUMENTS = {
    'prompt': lambda x: PromptFactory.get_prompt(x) in languages.get_prompts()
}

def add_arguments(parser: ArgumentParser):
    """
    Adds 'request' argument to the parser. This argument is used to
    specify the input to prompt the API with. This argument is required,
    however, it can be piped in from another command or from a file.

    Args:
        parser (ArgumentParser): The parser to add the argument to.
    """
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--refactor',
        action='store_true',
        help='Refactor the code.'
    )
    group.add_argument(
        '--document',
        action='store_true',
        help='Document the code.'
    )
    group.add_argument(
        '--test',
        action='store_true',
        help='Test the code.'
    )
