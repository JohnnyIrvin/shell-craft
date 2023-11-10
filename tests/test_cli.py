import pathlib
import unittest.mock
from argparse import Namespace
from typing import Optional

import pytest

from shell_craft.cli.main import (AggregateConfiguration, _generate_service,
                                  _get_configuration, _get_prompt,
                                  _get_sub_prompt_name, _interactive,
                                  _single_request)
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
        prompt="bash",
        request="test",
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

def test_configuration_expands_xdg_home_env_var():
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
            {'XDG_CONFIG_HOME': '~/.config'}
        ):
            _get_configuration()
            assert expand('~/.config/shell-craft/config.json') in mock.call_args.args[0]

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
    
@pytest.mark.parametrize(
    "subprompt, expected",
    [
        ("refactor", BASH_PROMPT.refactoring),
        ("document", BASH_PROMPT.documentation),
        ("test", BASH_PROMPT.testing),
        ("notimplemented", BASH_PROMPT),
        (None, BASH_PROMPT),
    ]
)
def test_get_prompt(namespace: Namespace, subprompt: str, expected: str):
    """
    Tests that the prompt is generated correctly.
    """
    # Act
    prompt = _get_prompt("bash", subprompt)
    
    # Assert
    assert prompt == expected.messages

def test_single_request_prints_response(namespace: Namespace):
    """
    Tests that the single request prints the response.
    """
    # Arrange
    service = _generate_service(namespace)
    with unittest.mock.patch.object(service, 'query') as service_mock:
        service_mock.return_value = ['test']
        with unittest.mock.patch('builtins.print') as print_mock:
            # Act
            _single_request(service, namespace)
            
            # Assert
            print_mock.assert_called_once_with('test')

def test_interactive_mode_prints_results(namespace: Namespace):
    """
    Tests that the interactive mode prints the results.
    """
    # Arrange
    service = _generate_service(namespace)
    with unittest.mock.patch.object(service, 'query') as service_mock:
        service_mock.return_value = ['ls']
        with unittest.mock.patch('builtins.input') as input_mock:
            input_mock.side_effect = ['ls', 'n', 'exit']
            with unittest.mock.patch('builtins.print') as print_mock:
                # Act
                _interactive(service)
                
                # Assert
                print_mock.assert_has_calls(
                    [
                        unittest.mock.call("Welcome to Shell Craft interactive mode."),
                        unittest.mock.call("Type 'exit' or Ctrl+C to exit the program."),
                        unittest.mock.call(),
                        unittest.mock.call("ls"),
                        unittest.mock.call(),
                    ]
                )
