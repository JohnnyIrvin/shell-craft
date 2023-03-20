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
import pytest

import shell_craft.prompts as prompts
from shell_craft.factories import PromptFactory

PROMPTS = [
    prompt
    for prompt in dir(prompts)
    if prompt.endswith("_PROMPT")
    and not prompt.startswith("_")
]

@pytest.mark.parametrize("prompt", PROMPTS)
def test_prompt_factory(prompt: str):
    """
    Test that the prompt factory returns the correct prompt.

    Args:
        prompt (str): The prompt to test.
    """    
    assert PromptFactory.get_prompt(prompt.removesuffix("_PROMPT")) == getattr(prompts, prompt)
