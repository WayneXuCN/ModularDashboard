"""Configuration management."""

import json
import os
from typing import Optional
from .schema import AppConfig, LayoutConfig, ModuleConfig

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "user-config.json")
DEFAULT_CONFIG_FILE = os.path.join("src", "research_dashboard", "assets", "default-config.json")

def load_config() -> AppConfig:
    """Load configuration from file or create default config if not exists."""
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Load config file if exists, otherwise create from default
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
    else:
        # Load default config
        with open(DEFAULT_CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        # Save default config to user config file
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=2)
    
    # Convert to AppConfig object
    layout = LayoutConfig(**config_data.get("layout", {}))
    modules = [ModuleConfig(**module) for module in config_data.get("modules", [])]
    
    return AppConfig(
        version=config_data.get("version", "0.1.0"),
        theme=config_data.get("theme", "light"),
        layout=layout,
        modules=modules
    )

def save_config(config: AppConfig) -> None:
    """Save configuration to file."""
    config_data = {
        "version": config.version,
        "theme": config.theme,
        "layout": config.layout.__dict__,
        "modules": [module.__dict__ for module in config.modules]
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)