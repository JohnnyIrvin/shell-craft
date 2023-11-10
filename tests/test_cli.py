import pathlib
import unittest.mock

import pytest

from shell_craft.cli.main import AggregateConfiguration, _get_configuration


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
