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
from dataclasses import dataclass, field

MODEL_MESSAGE = list[dict[str, str]]

@dataclass(frozen=True)
class Prompt:
    """
    A prompt is a guide for OpenAI models to generate text. It is a
    string that is used to seed the model's text generation. It is
    typically a question or a statement that the model is asked to
    respond to.

    Examples refer to "user" messages that are sent to the model, and
    "assistant" messages that are sent from the model. We use this
    as additional context for the model to generate text.
    """    
    content: str
    examples: list[MODEL_MESSAGE] = field(default_factory=list)

    @property
    def messages(self) -> list[MODEL_MESSAGE]:
        """
        Get the messages to send to the model. This includes the prompt
        and any examples. The prompt is sent as a "system" message, and
        the examples are sent as "user" and "assistant" messages.

        The dictionary is formatted as follows:
        {
            "role": <"system" | "user" | "assistant">,
            "content": <str>
        }

        Returns:
            list[MODEL_MESSAGE]: The messages to send to the model.
        """        
        return [
            {
                "role": "user",
                "content": self.content
            }
        ] + self.examples
