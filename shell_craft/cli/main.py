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
import subprocess
from argparse import ArgumentParser, Namespace
from typing import Optional, Union

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
    
def _get_sub_prompt_name(args: Union[Namespace, dict]) -> Optional[str]:
    """
    Returns the name of the sub-prompt.

    Args:
        args (Union[Namespace, dict]): The arguments to parse. Should be a
            Namespace or a dictionary.

    Returns:
        Optional[str]: The name of the sub-prompt.
    """
    _getattr = lambda key, default: getattr(args, key, default)
    _get = lambda key, default: (
        _getattr(key, default)
        if isinstance(args, Namespace)
        else args.get(key, default)
    )
    
    if _get("refactor", False):
        return "refactor"
    elif _get("document", False):
        return "document"
    elif _get("test", False):
        return "test"
    
    return None
    
def _get_prompt(prompt_name: str, sub_prompt_name: Optional[str] = None) -> str:
    """
    Returns the prompt to use for the CLI.

    Args:
        prompt_name (str): The name of the prompt.
        sub_prompt_name (str): The name of the sub-prompt, defaults to None.

    Returns:
        str: The prompt to use for the CLI.
    """
    subprompts = {
        "refactor": "refactoring",
        "document": "documentation",
        "test": "testing",
    }
    
    prompt = PromptFactory.get_prompt(prompt_name)
    
    if sub_prompt_name:
        sub_prompt = subprompts.get(sub_prompt_name, '')
        prompt = getattr(prompt, sub_prompt, prompt)
        
    return prompt.messages

def _generate_service(args: Namespace) -> OpenAIService:
    """
    Generates the OpenAI service for the CLI.

    Args:
        args (Namespace): The arguments to generate the service with.

    Returns:
        OpenAIService: The OpenAI service for the CLI.
    """
    return OpenAIService(
        OpenAISettings(
            api_key=args.api_key,
            model=args.model,
            count=args.count,
            temperature=args.temperature,
            messages=_get_prompt(args.prompt, _get_sub_prompt_name(args)),
        )
    )
        
def _single_request(service: OpenAIService, args: Namespace) -> None:
    """
    Handles a single request.

    Args:
        service (OpenAIService): The OpenAI service to use.
        args (Namespace): The arguments to use.
    """
    results = service.query(message=' '.join(args.request))
    
    github_url = getattr(args, "github", None)
    for _, r in enumerate(results):
        if github_url:
            print(get_github_url_or_error(r, github_url))
        else:
            print(r)

def _interactive(service: OpenAIService, shell: str = "bash") -> None:
    """
    Handles an interactive session.
    
    ..  warning::
    
        Interactive mode does not store the history of the session. This means
        that the model will not be able to learn from the previous messages.
        Which is different from how ChatGPT or other LLM models handle threads.

    :param service: The OpenAI service to use.
    :type service: OpenAIService
    """    
    print("Welcome to Shell Craft interactive mode.")
    print("Type 'exit' or Ctrl+C to exit the program.")
    print()
    
    while True:
        try:
            message = input(">>> ")
            
            if message == "exit":
                break
            
            results = service.query(message=message)[0]
            print(results)
            
            print()
            if input("Execute? (y/n) ").lower() == "y":
                results = subprocess.run(
                    f'{shell} -c "{results}"',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                print(results.stdout.decode("utf-8"))
    
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break
            
    
def main() -> None:
    """
    Main function that processes the command-line arguments and queries the
    OpenAI API using shell_craft.
    """
    args = get_arguments(
        initialize_parser(
            ArgumentParser(
                prog="shell-craft",
                description="Generating shell commands and code using natural language models (OpenAI ChatGPT).",
                add_help=False
            ),
            commands=_COMMANDS,
            configuration=_get_configuration()
        ),
    )
    
    service = _generate_service(args)
    
    if args.interactive:
        shell = "powershell" if args.prompt == "powershell" else "bash"
        _interactive(service, shell)
    else:
        _single_request(service, args)
