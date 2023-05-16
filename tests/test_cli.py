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
from typing import Union

from pytest import mark

from shell_craft.cli.github import GitHubArguments
from shell_craft.cli.github import add_arguments as add_github_arguments
from shell_craft.cli.models import add_arguments as add_model_arguments


@mark.parametrize('model', [
    'gpt-4',
    'gpt-4-0314',
    'gpt-4-32k',
    'gpt-4-32k-0314',
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-0301',
])
def test_ai_model_arguments(model: str):
    parser = ArgumentParser()
    add_model_arguments(parser)
    args = parser.parse_args(['--model', model])
    assert args.model == model

def test_github_arguments():
    parser = ArgumentParser()
    add_github_arguments(parser)
    args = parser.parse_args(['--github', 'https://github.com/JohnnyIrvin/shell-craft/'])
    assert args.github == 'https://github.com/JohnnyIrvin/shell-craft/'

@mark.parametrize('field, value', [
    ('title', 'test'),
    ('labels', ['one', 'two', 'three']),
    ('body', 'about me\n\nbody'),
])
def test_github_arguments_from_prompt(field: str, value: Union[list[str], str]):
    args = GitHubArguments.from_prompt("""
---
name: test
about: about me
labels: one,two,three
---
body
    """)
    assert getattr(args, field) == value

def test_github_arguments_as_url():
    from urllib.parse import urlencode

    args = GitHubArguments.from_prompt("""
---
name: test
about: about me
labels: one,two,three
---
body
    """)

    assert args.as_url('https://github.com/JohnnyIrvin/shell-craft/') == (
        'https://github.com/JohnnyIrvin/shell-craft/issues/new?'
        + urlencode({
            'title': 'test',
            'labels': 'one,two,three',
            'body': 'about me\n\nbody'
        })
    )
