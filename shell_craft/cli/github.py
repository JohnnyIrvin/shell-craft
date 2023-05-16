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
import json
import os
from argparse import ArgumentParser
from dataclasses import dataclass
from urllib.parse import urlencode, urljoin

from shell_craft.factories import PromptFactory
from shell_craft.prompts.templates import (BUG_REPORT_PROMPT,
                                           FEATURE_REQUEST_PROMPT)

ARGUMENTS = {
    'prompt': lambda x: PromptFactory.get_prompt(x) in [ BUG_REPORT_PROMPT, FEATURE_REQUEST_PROMPT ]
}

@dataclass
class GitHubArguments:
    title: str
    labels: list[str]
    body: str

    def as_url(self, repository: str) -> str:
        """
        Generates a URL to open an issue or feature request for the
        GitHub repository.

        Args:
            repository (str): The URL to the GitHub repository.

        Returns:
            str: The URL to open an issue or feature request for the
                GitHub repository.
        """        
        return (
            urljoin(
                repository.rstrip('/') + '/',
                'issues/new'
            )
            + '?'
            + urlencode({
                'title': self.title,
                'labels': ','.join(self.labels),
                'body': self.body
            })
        )
    
    @staticmethod
    def from_prompt(prompt: str) -> 'GitHubArguments':
        """
        Parses data from

        ```
        ---
        name: <Name Of Bug>
        about: <Short Description>
        labels: < Documentation, Enhancement, Question, Bug, etc. >
        ---

        <body>
        ```
        """
        tokens = prompt.split('---')

        if len(tokens) != 3:
            raise ValueError('Invalid prompt.')
        
        _, metadata, body = tokens

        tokens = metadata.split('\n')
        metadata = {
            token.split(':')[0].strip(): ':'.join(token.split(':')[1:]).strip()
            for token in tokens
        }

        return GitHubArguments(
            title=metadata['name'],
            labels=metadata['labels'].split(','),
            body=metadata['about'] + '\n\n' + body.strip()
        )

def get_github_url() -> str:
    """
    Gets the Github URL from the environment variable GITHUB_REPOSITORY, or from the
    config.json file. If neither are found, a ValueError is raised. The config.json
    file should be in the following format:

    {
        "github_repository": "https://github.com/username/repository"
    }

    Raises:
        ValueError: If no GitHub repository is found.

    Returns:
        str: The URL to the GitHub repository.
    """
    api_key = os.environ.get("GITHUB_REPOSITORY")
    if api_key:
        return api_key

    candidates = ["config.json"]

    if 'SHELLCRAFT_CONFIG' in os.environ:
        candidates.append(os.environ['SHELLCRAFT_CONFIG'])

    config_dir = None
    if 'XDG_CONFIG_HOME' in os.environ:
        config_dir = os.path.join(os.environ['XDG_CONFIG_HOME'])
    elif 'HOME' in os.environ:
        config_dir = os.path.join(os.environ['HOME'], '.config')

    if config_dir:
        candidates.append(os.path.join(config_dir, 'shell-craft', 'config.json'))

    filename = None
    for candidate in candidates:
        if os.path.exists(candidate):
            filename = candidate
            break
    else:
        raise ValueError("No GitHub repository found")

    with open(filename) as f:
        config = json.load(f)

    repository = config.get("github_repository")
    if not repository:
        raise ValueError("No GitHub repository found")
    
    return repository

def add_arguments(parser: ArgumentParser):
    """
    Adds '--github' argument to the parser. This argument is used to
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

    try:
        if not parser.parse_known_args()[0].github:
            parser.set_defaults(github=get_github_url())
    except ValueError:
        pass # No GitHub repository found