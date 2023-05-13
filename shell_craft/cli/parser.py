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


def _has_required_args(module: "ModuleType", args: Namespace) -> bool:
    """
    Checks if the module has the required arguments. If the module does not
    have the ARGUMENTS attribute, then it is assumed that the module does not
    require any arguments. If the module does have the ARGUMENTS attribute,
    then it is assumed that the module requires arguments as long as the
    ARGUMENTS attribute is a dictionary
    
    If the ARGUMENTS attribute is a dictionary, then the module will be checked
    to see if it has all of the required arguments. If the module has all of the
    required arguments, then the module will be checked to see if the values of
    the required arguments match the values of the arguments passed to the parser.
    
    If the values of the required arguments match the values of the arguments
    passed to the parser, are in a list of acceptable values, or pass a callable
    function, then the module will be considered to have the required arguments.

    Args:
        module (ModuleType): The module to check for required arguments.
        args (Namespace): The arguments passed to the parser.

    Returns:
        bool: True if the module has the required arguments, False otherwise.
    """    
    if not hasattr(module, "ARGUMENTS"):
        return True
    
    if not isinstance(module.ARGUMENTS, dict):
        return True
    
    for key in module.ARGUMENTS:
        if key not in args:
            return False
        
        arg_value = getattr(args, key)
        mod_value = module.ARGUMENTS[key]

        if isinstance(mod_value, str) and arg_value != mod_value:
            return False

        if isinstance(mod_value, list) and arg_value not in mod_value:
            return False
        
        if callable(mod_value) and not mod_value(arg_value):
            return False
            
    return True

def _add_args_parser(parser: ArgumentParser, module: "ModuleType", args: Namespace):
    """
    Adds the given module's subparsers and arguments to the parser.
    
    Args:
        parser (ArgumentParser): The parser to add the module to.
        module (ModuleType): The module to check for required arguments.
        args (Namespace): The arguments passed to the parser.
    """
    if hasattr(module, "add_parser"):
        module.add_parser(parser)

    if hasattr(module, "add_arguments"):
        module.add_arguments(parser)

def _add_optional_args_parser(parser: ArgumentParser, module: "ModuleType", args: Namespace):
    """
    Checks if the module's required arguments are present in the arguments
    passed to the parser. The module will be checked to see if it has all
    of the required arguments. If the module has all of the required
    arguments, then the module will be added to the parser.

    Args:
        parser (ArgumentParser): The parser to add the module to.
        module (ModuleType): The module to check for required arguments.
        args (Namespace): The arguments passed to the parser.
    """
    if not _has_required_args(module, args):
        return
    
    _add_args_parser(parser, module, args)

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
    modules: list["ModuleType"] = [
        import_module(f".{module.removesuffix('.py')}", package=PARENT_PACKAGE)
        for module in listdir(dirname(__file__))
        if module.endswith(".py") and
        module not in ["main.py", "parser.py", "__init__.py"]
    ]

    modules_without_requirements = [
        module for module in modules if not hasattr(module, "ARGUMENTS")
    ]
    modules_with_requirements = [
        module for module in modules if hasattr(module, "ARGUMENTS")
    ]

    KNOWN_ARGS, _ = parser.parse_known_args()
    for module in modules_without_requirements:
        _add_args_parser(parser, module, KNOWN_ARGS)

    KNOWN_ARGS, _ = parser.parse_known_args() # More arguments may have been added
    for module in modules_with_requirements:
        _add_optional_args_parser(parser, module, KNOWN_ARGS)

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

__all__ = [
    "get_arguments",
]

