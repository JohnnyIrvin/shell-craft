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


def get_api_key() -> str:
    """
    Gets the API key from the environment variable OPENAI_API_KEY, or from the
    config.json file. If neither are found, a ValueError is raised. The config.json
    file should be in the following format:

    {
        "openai_api_key": "YOUR_API_KEY"
    }

    Raises:
        ValueError: If no API key is found.

    Returns:
        str: The API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
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
        raise ValueError("No API key found")

    with open(filename) as f:
        config = json.load(f)

    api_key = config.get("openai_api_key")
    if api_key:
        return api_key

    raise ValueError("No API key found")

def add_arguments(parser: ArgumentParser):
    """
    Adds '--api-key' to the parser as an argument. If the argument is not
    provided, the API key is retrieved from the environment variable OPENAI_API_KEY,
    or from the config.json file. If neither are found, a ValueError is raised. The
    config.json file is the preferred method of providing the API key as it is a
    secret and should not be shared.

    Args:
        parser (ArgumentParser): The parser to add the argument to.
    """
    parser.add_argument(
        "--api-key",
        type=str,
        help="The OpenAI API key to use.",
    )

    try:
        if not parser.parse_known_args()[0].api_key:
            parser.set_defaults(api_key=get_api_key())
    except ValueError:
        print("No API key found. Please provide one with the --api-key argument.")
        parser.print_help()
        exit(1)
