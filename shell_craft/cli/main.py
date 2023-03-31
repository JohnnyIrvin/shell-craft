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
from shell_craft import Service
from shell_craft.factories import PromptFactory

from .parser import PARSER, get_arguments


def main():
    """
    Main function that processes the command-line arguments and queries the
    OpenAI API using shell_craft.
    """
    args = get_arguments(PARSER)
    prompt = PromptFactory.get_prompt(args.prompt)

    if getattr(args, "refactor", False):
        prompt = prompt.refactoring
    elif getattr(args, "document", False):
        prompt = prompt.documentation
    elif getattr(args, "test", False):
        prompt = prompt.testing

    print(
        Service(
            api_key=args.api_key,
            prompt=prompt,
            model=args.model
        ).query(
            message=' '.join(args.request)
        )
    )
