from __future__ import annotations

import importlib
import os
from pydantic import BaseModel
import tomllib

plugins = []

class PluginConfig(BaseModel):
    """Represents a plugin configuration."""
    title: str
    name: str
    lang: str

    @staticmethod
    def load(filepath: str) -> "PluginConfig":
        """Load a plugin configuration."""

        with open(filepath, "rb") as file:
            data = tomllib.load(file)
            
        return PluginConfig.model_validate(data)
        
        
class RegisteredPlugin(BaseModel):
    config: PluginConfig
    
class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    @staticmethod
    def register() -> None:
        """Register the plugin"""

        
def discover(plugin_dir = "aoc_tools/default_plugins/python") -> None:
    """Discover available plugins."""
    for filename in os.listdir(plugin_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            plugin_path = os.path.join(plugin_dir, filename)
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'register'):
                module.register()

    
def register(conf: PluginConfig) -> None:
    """Register a plugin."""
    global plugins
    plugins.append(RegisteredPlugin(config=conf))