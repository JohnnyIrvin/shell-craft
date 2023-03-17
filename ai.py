# Copyright (c) 2023 Johnathan P. Irvin

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#!/usr/bin/env python3

from sys import argv
import json

import openai

if len(argv) < 2:
    print("Usage: <program_name> <win:optional> <command>")
    exit(1)

with open("config.json") as f:
    config = json.load(f)

openai.api_key = config.get("openai_api_key")

is_windows = True if argv[1] == "win" else False

prompt = "You are a Linux terminal. You only reply with valid bash, and nothing else. Do not write explanations. You are bash. You will receive a description and return a bash command."
if is_windows:
    # Remove first argument
    argv.pop(1)
    prompt = "You are a Windows terminal. You only reply with valid cmd, and nothing else. Do not write explanations. You are powershell. You will receive a description and return a powershell command."

if len(argv) < 2:
    print("Usage: <program_name> <command>")
    exit(1)

print(
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": "pwd"
            },
            {
                "role": "assistant",
                "content": "/home/username"
            },
            {
                "role": "user",
                "content": " ".join(argv[1:])
            }
        ]
    )['choices'][0]['message']['content']
)