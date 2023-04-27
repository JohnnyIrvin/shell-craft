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
from typing import Union
from warnings import warn

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

    def query(self, message: str, count: int = 1, temperature: float = 1.0) -> Union[str, list[str]]:
        """
        Query the model with a message.

        Args:
            message (str): The message to query the model with.
            count (int, optional): The number of responses to return. Defaults to 1.
            temperature (float, optional): The sampling temperature to use. Defaults to 1.

        Returns:
            str | list[str]: The response from the model as a string or a list of strings.
        """
        warn(
            "In the future, the return type of Service.query will be a list of strings.",
            DeprecationWarning,
            source="shell_craft.services.Service.query"
        )
        warn(
            "In the future, configuring the number of results and sampling temperature will be done through a configuration interface.",
            DeprecationWarning,
            source="shell_craft.services.Service.query"
        )

        choices = openai.ChatCompletion.create(
            api_key=self._api_key,
            model=self._model,
            messages=self._prompt.messages + [
                {
                    "role": "user",
                    "content": message
                }
            ],
            n=count,
            temperature=temperature,
        )['choices']

        if count == 1:
            return choices[0]['message']['content']
        
        return [choice['message']['content'] for choice in choices]
