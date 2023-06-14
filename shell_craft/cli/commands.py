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
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

import shell_craft.prompts as prompts

from .prompt import get_calling_shell
from .types import limited_float


class CommandRestriction(Enum):
    """
    An enumeration of the different types of restrictions that can be placed on
    a command. Restrictions are whitelists of values that can be used for a
    given command.
    """
    PROMPT_TYPE: str = 'prompt_type'
    PROMPT_NAME: str = 'prompt_name'

@dataclass
class Command:
    flags: list
    dest: Optional[str] = None
    type: Optional[Type] = None
    default: Optional[str] = None
    config: Optional[str] = None
    action: Optional[str] = None
    help: Optional[str] = None
    nargs: Optional[str] = None
    choices: Optional[list] = None
    restrictions: Optional[dict[CommandRestriction, list]] = None

@dataclass
class CommandGroup:
    name: str
    commands: list[Command]
    restrictions: Optional[dict[CommandRestriction, list]] = None
    exclusive: Optional[bool] = False

_COMMANDS = [
    Command(
        flags=['request'],
        type=str,
        action='store',
        help='The request to make.',
        nargs='*',
    ),
    Command(
        flags=['--api-key'],
        dest='api_key',
        type=str,
        config='openai_api_key',
        action='store',
        help='The OpenAI API key to use.',
    ),
    Command(
        flags=['--model'],
        type=str,
        config='openai_model',
        default="gpt-3.5-turbo",
        action='store',
        help='The OpenAI model to use.',
        choices=[
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            'gpt-3.5-turbo-16k',
            'gpt-3.5-turbo-16k-0613',
        ]
    ),
    Command(
        flags=['-t', '--temperature'],
        dest='temperature',
        type=limited_float(0.0, 2.0),
        config='openai_temperature',
        default=1.0,
        action='store',
        help='The temperature to use when generating text. Must be between 0 and 2.',
    ),
    Command(
        flags=['-c', '--count'],
        dest='count',
        type=int,
        config='openai_count',
        default=1,
        action='store',
        help='The number of responses to generate.',
    ),
    Command(
        flags=['--prompt'],
        dest='prompt',
        config='shell_craft_prompt',
        type=str,
        choices=[
            prompt.removesuffix('_PROMPT').lower()
            for prompt in dir(prompts)
            if prompt.endswith("PROMPT")
        ],
        default=get_calling_shell(),
        action='store',
        help='The type of prompt to use.',
        nargs='?',
    ),
    Command(
        flags=['--github'],
        type=str,
        config='github_repository',
        action='store',
        help='The URL to the GitHub repository to open an issue or feature request for.',
        restrictions={
            CommandRestriction.PROMPT_NAME: ['BUG_REPORT_PROMPT', 'FEATURE_REQUEST_PROMPT']
        }
    ),
    CommandGroup(
        name='code',
        commands=[
            Command(
                flags=['--refactor'],
                action='store_true',
                help='Refactor the code.',
            ),
            Command(
                flags=['--test'],
                action='store_true',
                help='Test the code.',
            ),
            Command(
                flags=['--document'],
                action='store_true',
                help='Document the code.',
            ),
        ],
        restrictions={
            CommandRestriction.PROMPT_TYPE: ['LanguagePrompt']
        },
        exclusive=True
    ),
    Command(
        flags=['--help'],
        action='help',
        help='Show this help message and exit.',
    )
]


__all__ = [
    'Command',
    'CommandGroup',
    'CommandRestriction',
]
