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
from shell_craft.configuration import (AggregateConfiguration, Configuration,
                                       DictionaryConfiguration,
                                       JSONConfiguration)


def json_configuration() -> JSONConfiguration:
    return JSONConfiguration(
        text="""{
            "key": "json"
        }"""
    )

def dictionary_configuration() -> DictionaryConfiguration:
    return DictionaryConfiguration(
        variables={
            "KEY": "dictionary"
        }
    )

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
def test_get_value(configuration: Configuration, key: str, value: str) -> None:
    assert configuration.get_value(key) == value

@pytest.mark.parametrize(
    "configuration, key, value", [
    (json_configuration(), "key", "new_value"),
    (dictionary_configuration(), "key", "new_value"),
    (aggregate_configuration(), "key", "new_value"),
])
def test_set_value(configuration: Configuration, key: str, value: str) -> None:
    configuration.set_value(key, value)
    assert configuration.get_value(key) == value

@pytest.mark.parametrize(
    "configuration, keys", [
    (json_configuration(), ["key"]),
    (dictionary_configuration(), ["key"]),
    (aggregate_configuration(), ["key"]),
])
def test_get_keys(configuration: Configuration, keys: list[str]) -> None:
    assert configuration.keys == keys
