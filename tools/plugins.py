from __future__ import annotations

from abc import ABC
from abc import ABCMeta
from typing import Iterable
from typing import Type


class RegistryRepr(type):
    def __repr__(cls) -> str:

        if cls.__name__ != "PluginRegistry":
            raise AttributeError("Trying to represent something other than a PluginRegistry")

        runners = [c.__name__ for c in getattr(cls, "runners")]
        parsers = [c.__name__ for c in getattr(cls, "parsers")]
        return f"PluginRegistry(runners={runners}, parsers={parsers})"


class PluginRegistry(type, metaclass=RegistryRepr):
    runners: list[Type[RunnerPlugin]] = []
    parsers: list[Type[ParserPlugin]] = []

    def __init__(
        cls: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
    ) -> None:

        if name in ("RunnerPlugin", "ParserPlugin"):
            return

        if issubclass(cls, RunnerPlugin):
            PluginRegistry.runners.append(cls)
        elif issubclass(cls, ParserPlugin):
            PluginRegistry.parsers.append(cls)
        else:
            raise ValueError(f"Unknown plugin type: {cls.__base__.__name__}")


class _PluginABCMeta(PluginRegistry, ABCMeta):
    pass


class RunnerPlugin(ABC, metaclass=_PluginABCMeta):
    lang: str


class ParserPlugin(ABC, metaclass=_PluginABCMeta):
    lang: str


def discover_plugins(dirs: str | Iterable[str]) -> None:
    ...
