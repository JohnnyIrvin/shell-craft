import pathlib
import unittest.mock
from argparse import Namespace
from typing import Optional

import pytest

from shell_craft.cli.main import (AggregateConfiguration, _generate_service,
                                  _get_configuration, _get_sub_prompt_name)
from shell_craft.prompts.languages import BASH_PROMPT


@pytest.fixture
def namespace() -> Namespace:
    """
    Namespace to replicate command line arguments.
    
    Includes the following arguments:
    - api_key
    - model
    - count
    - temperature
    - prompt

    :return: Namespace with the above arguments.
    :rtype: Namespace
    """    
    return Namespace(
        api_key="test",
        model="test",
        count=1,
        temperature=1,
        prompt="bash"
    )

@pytest.mark.parametrize(
    'path',
    ['~/.shell-craft/config.json']
)
def test_get_configuration(path: str):
    """
    Tests that the configuration is loaded correctly.
    """
    expand = lambda path: pathlib.Path(path).expanduser().absolute().as_posix()
    with unittest.mock.patch.object(
        AggregateConfiguration,
        'from_files',
        return_value={'test': 'test'}
    ) as mock:
        _get_configuration()
        assert expand(path) in mock.call_args.args[0]
        
def test_configuration_expands_shell_craft_env_var():
    """
    Tests that the configuration is loaded correctly.
    """
    expand = lambda path: pathlib.Path(path).expanduser().absolute().as_posix()
    with unittest.mock.patch.object(
        AggregateConfiguration,
        'from_files',
        return_value={'test': 'test'}
    ) as mock:
        with unittest.mock.patch.dict(
            'os.environ',
            {'SHELLCRAFT_CONFIG': '~/.shell-craft/config.json'}
        ):
            _get_configuration()
            assert expand('~/.shell-craft/config.json') in mock.call_args.args[0]

@pytest.mark.parametrize(
    "args, expected",
    [
        ({"refactor": True}, "refactor"),
        ({"document": True}, "document"),
        ({"test": True}, "test"),
        ({}, None),
        (Namespace(refactor=True), "refactor"),
        (Namespace(document=True), "document"),
        (Namespace(test=True), "test"),
        (Namespace(), None),
    ],
)
def test_given_args_when_calling_get_sub_prompt_name_then_returns_expected(
    args: dict, expected: Optional[str]
):
    # Act
    result = _get_sub_prompt_name(args)

    # Assert
    assert result == expected

@pytest.mark.parametrize(
    "setting, expected",
    [
        ("api_key", "test"),
        ("model", "test"),
        ("count", 1),
        ("temperature", 1),
        ("messages", BASH_PROMPT.messages),
    ]
)
def test_generate_service(namespace: Namespace, setting: str, expected: str):
    """
    Tests that the service is generated correctly.
    """
    # Act
    service = _generate_service(namespace)
    
    # Assert
    assert getattr(service._settings, setting) == expected