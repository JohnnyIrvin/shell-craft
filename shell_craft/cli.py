# Copyright (c) 2023 Johnathan P. Irvin
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
import argparse
import json
import os

import shell_craft.prompts as prompts
from shell_craft import Service
from shell_craft.factories import PromptFactory

parser = argparse.ArgumentParser(
    prog="shell_craft",
    description="Prompt the OpenAI API for a response."
)
parser.add_argument(
    "prompt_type",
    type=str,
    choices=[
        prompt.removesuffix('_PROMPT').lower()
        for prompt in dir(prompts)
        if prompt.endswith("PROMPT")
    ],
    help="The type of prompt to use."
)
parser.add_argument(
    "human_request",
    type=str,
    nargs="+",
    help="The input to prompt the API with."
)
parser.add_argument(
    "--api-key",
    type=str,
    help="The OpenAI API key to use."
)

args = parser.parse_args()


def get_api_key() -> str:
    """
    Get the OpenAI API key from the environment, config file, or command line.

    Priority is given to the command line argument, then the environment variable,
    then the config file.

    Raises:
        ValueError: If no API key is found.

    Returns:
        str: The API key.
    """
    api_key = args.api_key
    if api_key:
        return api_key
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    if not os.path.exists("config.json"):
        raise ValueError("No API key found")
    
    with open("config.json") as f:
        config = json.load(f)

    api_key = config.get("openai_api_key")
    if api_key:
        return api_key
    
    raise ValueError("No API key found")

def main():    
    try:
        prompt = PromptFactory.get_prompt(args.prompt_type)
    except ValueError:
        print("Invalid prompt type")
        return
    
    print(
        Service(
            api_key=get_api_key(),
            prompt=prompt
        ).query(
            message=' '.join(args.human_request)
        )
    )
