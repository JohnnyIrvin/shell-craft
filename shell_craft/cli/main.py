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
import os
import pathlib
from argparse import ArgumentParser

from shell_craft.cli.github import GitHubArguments
from shell_craft.configuration import AggregateConfiguration
from shell_craft.factories import PromptFactory
from shell_craft.services import OpenAIService, OpenAISettings

from .commands import _COMMANDS
from .parser import get_arguments, initialize_parser


def _get_configuration() -> AggregateConfiguration:
    """
    Returns the configuration for the shell-craft CLI.

    Returns:
        AggregateConfiguration: The configuration for the shell-craft CLI.
    """
    expand = lambda path: pathlib.Path(path).expanduser().absolute().as_posix()
    join_expand = lambda *paths: expand(os.path.join(*paths))
    
    paths = [
        expand(os.path.join(os.getcwd(), 'config.json')),
        expand('~/.shell-craft/config.json'),
    ]
    
    if os.environ.get('SHELLCRAFT_CONFIG'):
        paths.append(expand(os.environ.get('SHELLCRAFT_CONFIG')))

    if os.environ.get('XDG_CONFIG_HOME'):
        paths.append(
            join_expand(
                os.environ.get('XDG_CONFIG_HOME'),
                'shell-craft',
                'config.json'
            )
        )

    return AggregateConfiguration.from_files(paths) | {
        key.lower(): value
        for key, value in os.environ.items() 
        if key.isupper()
    }

def get_github_url_or_error(prompt: str, repository: str) -> str:
    """
    Returns the GitHub URL for the prompt.

    Args:
        prompt (str): The prompt to generate the GitHub URL for.
        repository (str): The GitHub URL to generate the URL for.

    Returns:
        str: The GitHub URL for the prompt.
    """
    try:
        return GitHubArguments.from_prompt(
            prompt
        ).as_url(
            repository
        )
    except Exception:
        return "Error: Unable to generate GitHub URL."


def main():
    """
    Main function that processes the command-line arguments and queries the
    OpenAI API using shell_craft.
    """
    config = _get_configuration()
    args = get_arguments(
        initialize_parser(
            ArgumentParser(
                prog="shell-craft",
                description="Generating shell commands and code using natural language models (OpenAI ChatGPT).",
                add_help=False
            ),
            commands=_COMMANDS,
            configuration=config
        ),
    )
    prompt = PromptFactory.get_prompt(args.prompt)

    if getattr(args, "refactor", False):
        prompt = prompt.refactoring
    elif getattr(args, "document", False):
        prompt = prompt.documentation
    elif getattr(args, "test", False):
        prompt = prompt.testing

    results = OpenAIService(
        OpenAISettings(
            api_key=args.api_key,
            model=args.model,
            count=args.count,
            temperature=args.temperature,
            messages=prompt.messages,
        )
    ).query(
        message=' '.join(args.request),
    )

    github_url = getattr(args, "github", None)
    for _, r in enumerate(results):
        if github_url:
            print(get_github_url_or_error(r, github_url))
        else:
            print(r)
