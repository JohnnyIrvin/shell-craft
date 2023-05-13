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
from typing import Optional

from .prompt import Prompt


@dataclass(frozen=True)
class LanguagePrompt(Prompt):
    refactoring: Optional[Prompt] = None
    documentation: Optional[Prompt] = None
    testing: Optional[Prompt] = None


def _generate_prompt(language: str) -> LanguagePrompt:
    return LanguagePrompt(
        content=" ".join(f"""
            You are {language}.
            You reply with valid {language}, nothing else.
            No explanations.
            You receive descriptions and return {language}.
        """.split()),
        refactoring=Prompt(
            content=" ".join(f"""
                You receive {language} and return {language}.
                You shorten the code.
                You remove bugs.
                You make the code more efficient.
            """.split())
        ),
        documentation=Prompt(
            content=" ".join(f"""
                You receive {language} and return {language} with document strings.
                You add documentation to each function.
                You add documentation to each class.
                You explain parameters and return values.
                You run the code with the documentation in place.
            """.split())
        ),
        testing=Prompt(
            content=" ".join(f"""
                You receive {language} and return {language} with tests.
                You write tests for each function.
                Tests are written in AAA (Arrange, Act, Assert) format.
                You do not repeat yourself.
                You do not return the original code.
            """.split())
        )
    )

def get_prompts() -> list[LanguagePrompt]:
    """
    Returns all of the language prompts. This is used to generate the
    language prompt choices. This is also used to define the exports.

    Returns:
        list[LanguagePrompt]: All of the language prompts.
    """    
    return [
        prompt for prompt
        in globals().values()
        if isinstance(prompt, LanguagePrompt)
    ]

BASH_PROMPT = _generate_prompt("Bash")
C_PROMPT = _generate_prompt("C")
C_SHARP_PROMPT = _generate_prompt("C#")
GO_PROMPT = _generate_prompt("GoLang")
POWERSHELL_PROMPT = _generate_prompt("PowerShell")
PYTHON_PROMPT = _generate_prompt("Python")
JAVA_PROMPT = _generate_prompt("Java")
JAVASCRIPT_PROMPT = _generate_prompt("JavaScript")


__all__ = get_prompts()
