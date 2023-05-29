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
from unittest.mock import mock_open, patch

import pytest
from shell_craft.configuration import (AggregateConfiguration, Configuration,
                                       JSONConfiguration)


def json_configuration() -> JSONConfiguration:
    return JSONConfiguration(
        text="""{
            "key": "json"
        }"""
    )

def dictionary_configuration() -> dict:
    return {
        "key": "dictionary"
    }

def aggregate_configuration() -> AggregateConfiguration:
    return AggregateConfiguration(
        configurations=[
            json_configuration(),
            dictionary_configuration(),
        ]
    )

@pytest.mark.parametrize(
    "configuration, key, value", [
    (json_configuration(), "key", "json"),
    (dictionary_configuration(), "key", "dictionary"),
    (aggregate_configuration(), "key", "json"),
])
def test_get(configuration: Configuration, key: str, value: str) -> None:
    assert configuration.get(key) == value

@pytest.mark.parametrize(
    "configuration, keys", [
    (json_configuration(), ["key"]),
    (dictionary_configuration(), ["key"]),
    (aggregate_configuration(), ["key"]),
])
def test_get_keys(configuration: Configuration, keys: list[str]) -> None:
    assert list(configuration.keys()) == keys

def test_json_from_file() -> None:
    with patch("builtins.open", mock_open(read_data="""{
        "key": "json"
    }""")):
        assert JSONConfiguration.from_file("file.json").get("key") == "json"

def test_aggregate_from_files() -> None:
    with patch("builtins.open", mock_open(read_data="""{
        "key": "json"
    }""")):
        with patch("pathlib.Path.exists", return_value=True):
            assert AggregateConfiguration.from_files(["file.json"]).get("key") == "json"
