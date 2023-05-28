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

class DictionaryConfiguration:
    def __init__(self, variables: dict[str, str]) -> None:
        self._variables = {
            key.lower(): value
            for key, value in variables.items()
            if key.isupper()
        }

    @property
    def keys(self) -> list[str]:
        return list(self._variables.keys())
    
    def get_value(self, key: str) -> str:
        """
        Gets a value from the json text.

        Args:
            key (str): Looks up the JSON key using this value.

        Raises:
            KeyError: If the key does not exist in the JSON text.

        Returns:
            str: The value for the key.
        """        
        return self._variables[key.lower()]
    
    def set_value(self, key: str, value: str) -> None:
        """
        Sets a value in the json text. Does not save the text to a file.

        Args:
            key (str): The key to set.
            value (str): The value to set.
        """        
        self._variables[key.lower()] = value
