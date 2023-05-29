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
import json
from typing import Any, Protocol
import pathlib


class Configuration(Protocol):
    def get(self, key: Any, default=None) -> Any:
        ...

class JSONConfiguration(dict):
    def __init__(self, text: str) -> None:
        """
        Initialize the JSON configuration with the given text.

        Args:
            text (str): The text to parse as JSON.
        """        
        super().__init__(json.loads(text))

    @classmethod
    def from_file(cls, path: str) -> "JSONConfiguration":
        """
        Initialize the JSON configuration from the given file.

        Args:
            path (str): The path to the JSON file.

        Returns:
            JSONConfiguration: The JSON configuration.
        """        
        with open(path, "r") as file:
            return cls(file.read())

class AggregateConfiguration(dict):
    def __init__(self, configurations: list) -> None:
        """
        Aggregate the given configurations into a single configuration.

        Args:
            configurations (list): The configurations to aggregate.
        """        
        super().__init__({
            key: config.get(key)
            for config in configurations[::-1]
            for key in config.keys()
        })

    @classmethod
    def from_files(cls, paths: list[str]) -> "AggregateConfiguration":
        """
        Initialize the aggregate configuration from the given files.

        If a file does not exist, it will be ignored.

        Args:
            paths (list[str]): The paths to the JSON files.

        Returns:
            AggregateConfiguration: The aggregate configuration.
        """
        return cls([
            JSONConfiguration.from_file(path)
            for path in paths
            if path and pathlib.Path(path).exists()
        ])
