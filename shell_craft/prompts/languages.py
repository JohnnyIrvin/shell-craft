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
from .prompt import Prompt


def _generate_prompt(language: str) -> Prompt:
    return Prompt(
        content=" ".join(f"""
            You are {language}.
            You reply with valid {language}, nothing else.
            No explanations.
            You receive descriptions and return {language}.
        """.split()),
    )


BASH_PROMPT = _generate_prompt("Bash")
C_PROMPT = _generate_prompt("C")
C_SHARP_PROMPT = _generate_prompt("C#")
GO_PROMPT = _generate_prompt("Go")
POWERSHELL_PROMPT = _generate_prompt("PowerShell")
PYTHON_PROMPT = _generate_prompt("Python")
JAVA_PROMPT = _generate_prompt("Java")
JAVASCRIPT_PROMPT = _generate_prompt("JavaScript")
