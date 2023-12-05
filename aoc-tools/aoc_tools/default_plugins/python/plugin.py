from aoc_tools import plugins


def register() -> None:

    conf = plugins.PluginConfig.load("aoc_tools/default_plugins/python/config.toml")
    plugins.register(conf)


if __name__ == "__main__":
    register()
