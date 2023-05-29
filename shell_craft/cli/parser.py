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
from dataclasses import asdict
from sys import argv, stdin
from typing import Callable

from shell_craft.configuration import Configuration
from shell_craft.factories import PromptFactory

from .commands import Command, CommandGroup, CommandRestriction


class ShellCraftParser:
    def __init__(self, parser: ArgumentParser, config: Configuration) -> None:
        """
        Initialize the application parser with the given argparse parser. This
        is known as a proxy pattern or facade pattern.

        Args:
            parser (ArgumentParser): The argparse parser to use for the application.
        """        
        self._parser = parser
        self._config = config
        self._commands: list[Command | CommandGroup] = []

    @property
    def flags(self) -> list[str]:
        """
        Get the flags for the parser.

        Returns:
            list[str]: The flags for the parser.
        """
        return [
            flag
            for command in self._commands
            for flag in command.flags
        ]

    def add_command(self, command: Command, override: Callable = None) -> "ShellCraftParser":
        """
        Add a command to the parser.

        Args:
            command (Command): The command to add to the parser.
            override (Callable, optional): A function to call to override
                the add_argument function. Defaults to None.

        Returns:
            ShellCraftParser: The parser with the command added.
        """
        adder = override or self._parser.add_argument

        flags = ' '.join(command.flags)
        kwargs = {
            key: value
            for key, value in asdict(command).items()
            if value is not None
            and key not in ['flags', 'restrictions', 'config']
        }
        kwargs['default'] = self._config.get(command.config) or command.default

        adder(flags, **kwargs)
        self._commands.append(command)

        return self
    
    def add_group(self, group: CommandGroup) -> "ShellCraftParser":
        """
        Add a command group to the parser.

        Args:
            group (CommandGroup): The command group to add to the parser.

        Returns:
            ShellCraftParser: The parser with the command group added.
        """
        adder = self._parser.add_argument
        if group.exclusive:
            adder = self._parser.add_mutually_exclusive_group().add_argument

        for command in group.commands:
            self.add_command(command, adder)

        return self

    def can_add(self, command: Command | CommandGroup) -> bool:
        """
        Determine if the given command can be added to the parser.

        Args:
            command (Command): The command to check.

        Returns:
            bool: True if the command can be added, otherwise False.
        """
        if not command.restrictions:
            return True
        
        if '--prompt' not in self.flags:
            return False
        
        known_args, l = self._parser.parse_known_args()
        if not known_args.prompt:
            return False
        
        prompt = PromptFactory.get_prompt(known_args.prompt)
        
        for restriction in command.restrictions:
            if restriction == CommandRestriction.PROMPT_TYPE:
                if type(prompt).__name__ in command.restrictions[restriction]:
                    continue

            if restriction == CommandRestriction.PROMPT_NAME:
                prompt_name = known_args.prompt.upper() + "_PROMPT"

                if prompt_name in command.restrictions[restriction]:
                    continue
            
            return False
        
        return True


def initialize_parser(parser: ArgumentParser, commands: list[Command | CommandGroup], configuration: Configuration) -> ArgumentParser:
    """
    Initialize the parser with the given commands and command groups. This will add
    the commands and command groups to the parser and return the parser.

    Args:
        parser (ArgumentParser): The parser to initialize.
        commands (list[Command  |  CommandGroup]): The commands and command groups to add to the parser.
        configuration (Configuration): The configuration to use for the parser.

    Returns:
        ArgumentParser: The parser with the commands and command groups added.
    """
    _parser = ShellCraftParser(parser, configuration)
    for command in commands:
        if not _parser.can_add(command):
            continue

        if isinstance(command, Command):
            _parser.add_command(command)
        elif isinstance(command, CommandGroup):
            _parser.add_group(command)
        
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
    "initialize_parser"
    "ShellCraftParser"
]

