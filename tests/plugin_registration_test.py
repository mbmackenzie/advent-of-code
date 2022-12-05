import importlib
import sys
from itertools import product

import pytest


MAX_PLUGINS_TO_ADD = 5


@pytest.fixture
def plugins():
    yield importlib.import_module("tools.plugins")
    del sys.modules["tools.plugins"]


def test_plugin_registry_starts_empty(plugins):
    assert plugins.PluginRegistry.runners == []
    assert plugins.PluginRegistry.parsers == []


@pytest.mark.parametrize(
    "plugins, num_runners, num_parsers",
    [("plugins", *x) for x in product(range(MAX_PLUGINS_TO_ADD), repeat=2)],
    indirect=["plugins"],
)
def test_register_things(plugins, num_runners, num_parsers):

    for i in range(num_runners):

        class Runner(plugins.RunnerPlugin):
            lang = f"mylang{i}"

        Runner.__name__ = f = f"Runner{i}"

    for i in range(num_parsers):

        class Parser(plugins.ParserPlugin):
            lang = f"mylang{i}"

        Parser.__name__ = f = f"Parser{i}"

    print("\n", plugins.PluginRegistry)
    assert len(set(plugins.PluginRegistry.runners)) == num_runners
    assert len(set(plugins.PluginRegistry.parsers)) == num_parsers
