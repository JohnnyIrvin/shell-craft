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
from shell_craft.prompts import Prompt


class PromptFactory:
    @staticmethod
    def get_prompt(prompt: str) -> Prompt:
        """
        Generates a new prompt object based on the prompt type.

        Args:
            prompt (str): A string representing the prompt type.

        Raises:
            ValueError: If the prompt type is not supported.

        Returns:
            Prompt: A new prompt object.
        """        
        import shell_craft.prompts as prompts

        available_prompts = [
            prompt.removesuffix('_PROMPT').casefold()
            for prompt in dir(prompts)
            if prompt.endswith("_PROMPT")
        ]

        if prompt.casefold() in available_prompts:
            return getattr(prompts, f"{prompt.upper()}_PROMPT")


        raise ValueError(f"Unknown prompt type: {prompt}")
