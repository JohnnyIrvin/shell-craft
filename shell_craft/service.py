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
import openai

from shell_craft.prompts import Prompt


class Service:
    def __init__(self, api_key: str, prompt: Prompt, model: str = "gpt-3.5-turbo"):
        """
        Initialize a new Service instance.

        Args:
            api_key (str): The OpenAI API key to use.
            prompt (Prompt): Informs the model how to act when generating a response.
            model (str, optional):
                The model to use when generating a response. Defaults to "gpt-3.5-turbo".
                Check out the OpenAI docs for more information on models and their
                pricing.
        """
        self._api_key: str = api_key
        self._prompt: Prompt = prompt
        self._model: str = model

    def query(self, message: str) -> str:
        """
        Query the model with a message.

        Args:
            message (str): The message to query the model with.

        Returns:
            str: The response from the model.
        """
        return openai.ChatCompletion.create(
            api_key=self._api_key,
            model=self._model,
            messages=self._prompt.messages + [
                {
                    "role": "user",
                    "content": message
                }
            ]
        )['choices'][0]['message']['content']
