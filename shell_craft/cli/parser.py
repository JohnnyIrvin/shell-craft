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
from argparse import ArgumentParser, Namespace
from importlib import import_module
from os import listdir
from os.path import dirname
from sys import argv, stdin


def initialize_parser(parser: ArgumentParser) -> ArgumentParser:
    """ 
    Add arguments to the parser. Loops through all modules in this package and
    calls the add_arguments function in each one if it exists and is callable.
    The modules are imported dynamically, so adding a new module to this package
    will automatically add its arguments to the parser as long as the module
    has an add_arguments function.

    While looping through each module in this package, we'll attempt to add
    any subparsers that are defined in the module. Modules which contain
    subparsers should define add_parser as a function which takes a parser as
    an argument.

    This function will skip the main and parser modules, as they are not
    intended to be used as subparsers or intended to add arguments to the
    parser.

    Args:
        parser (ArgumentParser): The parser to add arguments to.

    Returns:
        ArgumentParser: The parser with arguments added. Fluent interface.
    """
    PARENT_PACKAGE = __name__.rsplit(".", 1)[0]
    for module in listdir(dirname(__file__)):
        module = module.removesuffix(".py")

        if module in ["main", "parser", "__init__"]:
            continue
        
        try:
            import_module(f".{module}", package=PARENT_PACKAGE).add_arguments(parser)
        except AttributeError:
            pass

        try:
            import_module(f".{module}", package=PARENT_PACKAGE).add_parser(parser)
        except AttributeError:
            pass

    return parser

def get_arguments(parser: ArgumentParser) -> Namespace:
    """
    Get the arguments from the parser. If there is no input from stdin, then
    the arguments will be parsed from the command line. If there is input from
    stdin, then the arguments will be parsed from the command line and stdin after
    calling a flush on stdin.

    Args:
        parser (ArgumentParser): The parser to get arguments from.

    Returns:
        Namespace: The arguments from the parser.
    """
    arguments: list[str] = argv[1:]

    if not stdin.isatty():
        stdin.flush()
        arguments += stdin.readlines()

    return parser.parse_args(arguments)

PARSER = initialize_parser(ArgumentParser(
    prog="shell-craft",
    description="Generating shell commands and code using natural language models (OpenAI ChatGPT).",
))

__all__ = [
    "get_arguments",
    "PARSER"
]

