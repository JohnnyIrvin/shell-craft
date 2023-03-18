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
import json
from sys import argv

from shell_craft import Service
from shell_craft.factories import PromptFactory


def main():
    if len(argv) < 3:
        print("Usage: <program_name> <prompt type> <human request>")
        return
    
    prompt_type, human_request = argv[1], " ".join(argv[2:])

    with open("config.json") as f:
        config = json.load(f)

    try:
        prompt = PromptFactory.get_prompt(prompt_type)
    except ValueError:
        print("Invalid prompt type")
        return

    api_key = config.get("openai_api_key")
    print(Service(api_key, prompt).query(human_request))
