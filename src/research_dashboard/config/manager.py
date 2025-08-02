"""Configuration management."""

import json
import os
from pathlib import Path

from .schema import AppConfig, LayoutConfig, ModuleConfig


def get_config_dir():
    """Get the system-specific configuration directory.

    Returns
    -------
    config_dir : pathlib.Path
        The path to the configuration directory based on the operating system.

    Notes
    -----
    The configuration directory is determined as follows:
    - Windows: %APPDATA%\\ResearchDashboard
    - macOS/Linux: ~/.config/ResearchDashboard
    - Other systems: ./config (fallback)
    """
    if os.name == "nt":  # Windows
        config_dir = Path(os.environ.get("APPDATA", "")) / "ResearchDashboard"
    elif os.name == "posix":  # POSIX systems (macOS/Linux/others)
        config_dir = Path.home() / ".config" / "ResearchDashboard"
    else:
        # Fallback to current directory for non-standard systems
        config_dir = Path("config")

    return config_dir


CONFIG_DIR = get_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG_FILE = Path(__file__).parent.parent / "assets" / "default-config.json"


def load_config() -> AppConfig:
    """Load configuration from file or create default config if not exists.

    This function attempts to load the user configuration from the system-specific
    configuration directory. If no configuration file exists, it creates one using
    the default configuration template.

    Returns
    -------
    config : AppConfig
        The application configuration object containing version, theme, layout,
        and module settings.

    Notes
    -----
    The configuration file is stored in JSON format. The default configuration
    is loaded from the assets directory and saved to the user config directory
    on first run.
    """
    # Create config directory if it doesn't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Load config file if exists, otherwise create from default
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r") as f:
            config_data = json.load(f)
    else:
        # Load default config
        with DEFAULT_CONFIG_FILE.open("r") as f:
            config_data = json.load(f)
        # Save default config to user config file
        with CONFIG_FILE.open("w") as f:
            json.dump(config_data, f, indent=2)

    # Convert to AppConfig object
    layout = LayoutConfig(**config_data.get("layout", {}))
    modules = [ModuleConfig(**module) for module in config_data.get("modules", [])]

    return AppConfig(
        version=config_data.get("version", "0.1.0"),
        theme=config_data.get("theme", "light"),
        layout=layout,
        modules=modules,
    )


def save_config(config: AppConfig) -> None:
    """Save configuration to file.

    Parameters
    ----------
    config : AppConfig
        The application configuration object to be saved.

    Notes
    -----
    The configuration is saved in JSON format with indentation for readability.
    Existing configuration files will be overwritten.
    """
    config_data = {
        "version": config.version,
        "theme": config.theme,
        "layout": config.layout.__dict__,
        "modules": [module.__dict__ for module in config.modules],
    }

    with CONFIG_FILE.open("w") as f:
        json.dump(config_data, f, indent=2)
