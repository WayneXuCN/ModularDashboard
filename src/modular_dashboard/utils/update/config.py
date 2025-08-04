"""Configuration management for update system."""

import json
import os
from pathlib import Path
from typing import Any

from loguru import logger


class UpdateConfig:
    """Configuration manager for update system."""

    def __init__(self, config_path: str | Path | None = None):
        self.config_path = (
            Path(config_path) if config_path else Path("update_config.json")
        )
        self.config: dict[str, Any] = {}

        # Load existing config
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, encoding="utf-8") as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                self.config = self.get_default_config()
                logger.info("Using default configuration")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = self.get_default_config()

    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def update(self, updates: dict[str, Any]) -> None:
        """Update configuration with multiple values."""
        self._deep_update(self.config, updates)

    def _deep_update(
        self, base_dict: dict[str, Any], update_dict: dict[str, Any]
    ) -> None:
        """Deep update dictionary."""
        for key, value in update_dict.items():
            if (
                isinstance(value, dict)
                and key in base_dict
                and isinstance(base_dict[key], dict)
            ):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration."""
        return {
            "base_dir": "./update_system",
            "background_checks": True,
            "auto_update": False,
            "policy": {
                "auto_update": False,
                "update_types": ["patch", "security"],
                "check_interval": 3600,
                "backup_before_update": True,
                "prerelease_updates": False,
            },
            "security": {"require_signature": True, "require_checksum": True},
            "sources": {"github": {}, "pypi": {}},
            "ui": {
                "show_update_badge": True,
                "notification_sound": True,
                "auto_refresh": True,
            },
        }

    def get_module_config(self, module_id: str) -> dict[str, Any]:
        """Get configuration for a specific module."""
        return self.get(f"modules.{module_id}", {})

    def set_module_config(self, module_id: str, config: dict[str, Any]) -> None:
        """Set configuration for a specific module."""
        self.set(f"modules.{module_id}", config)

    def add_github_source(
        self, name: str, owner: str, repo: str, token: str | None = None
    ) -> None:
        """Add a GitHub update source."""
        source_config = {"owner": owner, "repo": repo}
        if token:
            source_config["token"] = token

        self.set(f"sources.github.{name}", source_config)

    def add_pypi_source(self, name: str, package: str) -> None:
        """Add a PyPI update source."""
        self.set(f"sources.pypi.{name}", {"package": package})

    def remove_source(self, source_type: str, name: str) -> None:
        """Remove an update source."""
        self.set(f"sources.{source_type}.{name}", None)

    def get_source_config(self, source_type: str, name: str) -> dict[str, Any] | None:
        """Get configuration for an update source."""
        return self.get(f"sources.{source_type}.{name}")

    def list_sources(self, source_type: str | None = None) -> dict[str, Any]:
        """List update sources."""
        if source_type:
            return self.get(f"sources.{source_type}", {})
        return self.get("sources", {})

    def validate_config(self) -> bool:
        """Validate configuration."""
        try:
            # Check required fields
            required_fields = ["base_dir", "policy"]
            for field in required_fields:
                if field not in self.config:
                    logger.error(f"Missing required field: {field}")
                    return False

            # Validate policy
            policy = self.config.get("policy", {})
            if "check_interval" in policy and (
                not isinstance(policy["check_interval"], int)
                or policy["check_interval"] <= 0
            ):
                logger.error("Invalid check_interval value")
                return False

            # Validate update types
            if "update_types" in policy:
                valid_types = ["major", "minor", "patch", "security"]
                for update_type in policy["update_types"]:
                    if update_type not in valid_types:
                        logger.error(f"Invalid update type: {update_type}")
                        return False

            # Validate sources
            sources = self.config.get("sources", {})
            for source_type, source_configs in sources.items():
                if source_type == "github":
                    for name, config in source_configs.items():
                        if not all(k in config for k in ["owner", "repo"]):
                            logger.error(f"Invalid GitHub source config: {name}")
                            return False
                elif source_type == "pypi":
                    for name, config in source_configs.items():
                        if "package" not in config:
                            logger.error(f"Invalid PyPI source config: {name}")
                            return False

            return True

        except Exception as e:
            logger.error(f"Error validating configuration: {e}")
            return False

    def export_config(self, export_path: str | Path) -> None:
        """Export configuration to file."""
        export_path = Path(export_path)
        try:
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration exported to {export_path}")
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            raise

    def import_config(self, import_path: str | Path) -> None:
        """Import configuration from file."""
        import_path = Path(import_path)
        try:
            with open(import_path, encoding="utf-8") as f:
                imported_config = json.load(f)

            # Validate imported config
            temp_config = self.config
            self.config = imported_config
            if not self.validate_config():
                self.config = temp_config
                raise ValueError("Invalid configuration file")

            logger.info(f"Configuration imported from {import_path}")
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            raise

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.get_default_config()
        logger.info("Configuration reset to defaults")

    def get_env_override(self, key: str, env_var: str) -> Any:
        """Get configuration value with environment variable override."""
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Try to parse as JSON first, then as string
            try:
                return json.loads(env_value)
            except json.JSONDecodeError:
                return env_value

        return self.get(key)

    def apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Common environment variables
        env_mappings = {
            "UPDATE_BASE_DIR": "base_dir",
            "UPDATE_AUTO_UPDATE": "policy.auto_update",
            "UPDATE_CHECK_INTERVAL": "policy.check_interval",
            "UPDATE_REQUIRE_SIGNATURE": "security.require_signature",
            "UPDATE_REQUIRE_CHECKSUM": "security.require_checksum",
            "UPDATE_BACKGROUND_CHECKS": "background_checks",
        }

        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string values to appropriate types
                if env_value.lower() in ["true", "false"]:
                    env_value = env_value.lower() == "true"
                elif env_value.isdigit():
                    env_value = int(env_value)

                self.set(config_key, env_value)
                logger.info(f"Applied env override: {config_key} = {env_value}")


def create_config_from_env() -> UpdateConfig:
    """Create configuration from environment variables."""
    config = UpdateConfig()
    config.apply_env_overrides()
    return config


def load_config(config_path: str | Path) -> UpdateConfig:
    """Load configuration from file."""
    return UpdateConfig(config_path)
