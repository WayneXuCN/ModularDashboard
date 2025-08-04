"""Update system initialization and configuration."""

from pathlib import Path
from typing import Any

from loguru import logger

from .checker import ModuleUpdateRegistry
from .core import DefaultUpdateNotifier, UpdatePolicy
from .manager import UpdateManager
from .security import SecurityValidator
from .sources import UpdateSourceManager
from .storage import FileUpdateStorage
from .ui import UpdateUI


class UpdateSystem:
    """Main update system coordinator."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.update_manager: UpdateManager | None = None
        self.update_ui: UpdateUI | None = None
        self.update_registry = ModuleUpdateRegistry()
        self.is_initialized = False

        # Paths
        self.base_dir = Path(config.get("base_dir", "."))
        self.modules_dir = self.base_dir / "modules"
        self.backup_dir = self.base_dir / "backups"
        self.storage_dir = self.base_dir / "update_storage"
        self.keys_dir = self.base_dir / "keys"

        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.modules_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.keys_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self) -> None:
        """Initialize the update system."""
        try:
            logger.info("Initializing update system...")

            # Initialize components
            await self._initialize_storage()
            await self._initialize_sources()
            await self._initialize_security()
            await self._initialize_manager()
            await self._initialize_ui()

            self.is_initialized = True
            logger.info("Update system initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing update system: {e}")
            raise

    async def _initialize_storage(self) -> None:
        """Initialize storage components."""
        self.storage = FileUpdateStorage(str(self.storage_dir))
        self.notifier = DefaultUpdateNotifier()

        logger.info("Storage components initialized")

    async def _initialize_sources(self) -> None:
        """Initialize update sources."""
        self.source_manager = UpdateSourceManager()

        # Register default sources based on config
        sources_config = self.config.get("sources", {})

        # GitHub sources
        for name, config in sources_config.get("github", {}).items():
            self.source_manager.create_github_source(
                name=name,
                repo_owner=config["owner"],
                repo_name=config["repo"],
                token=config.get("token"),
            )
            logger.info(f"Registered GitHub source: {name}")

        # PyPI sources
        for name, config in sources_config.get("pypi", {}).items():
            self.source_manager.create_pypi_source(
                name=name, package_name=config["package"]
            )
            logger.info(f"Registered PyPI source: {name}")

    async def _initialize_security(self) -> None:
        """Initialize security components."""
        security_config = self.config.get("security", {})

        self.security_validator = SecurityValidator(
            keys_dir=str(self.keys_dir),
            require_signature=security_config.get("require_signature", True),
            require_checksum=security_config.get("require_checksum", True),
        )

        logger.info("Security components initialized")

    async def _initialize_manager(self) -> None:
        """Initialize update manager."""
        policy_config = self.config.get("policy", {})

        policy = UpdatePolicy(policy_config)

        self.update_manager = UpdateManager(
            modules_dir=str(self.modules_dir),
            backup_dir=str(self.backup_dir),
            storage=self.storage,
            notifier=self.notifier,
            policy=policy,
        )

        # Set validator
        self.update_manager.executor.validator = self.security_validator

        # Set registry
        self.update_manager.set_update_registry(self.update_registry)

        logger.info("Update manager initialized")

    async def _initialize_ui(self) -> None:
        """Initialize UI components."""
        if self.update_manager:
            self.update_ui = UpdateUI(self.update_manager)
            logger.info("UI components initialized")

    def register_module(self, module_id: str, module_info: dict[str, Any]) -> None:
        """Register a module for updates."""
        if not self.is_initialized:
            logger.warning("Update system not initialized, cannot register module")
            return

        self.update_registry.register_module(module_id, module_info)
        logger.info(f"Registered module for updates: {module_id}")

    def unregister_module(self, module_id: str) -> None:
        """Unregister a module from updates."""
        if self.update_registry:
            self.update_registry.unregister_module(module_id)
            logger.info(f"Unregistered module from updates: {module_id}")

    async def start(self) -> None:
        """Start the update system."""
        if not self.is_initialized:
            await self.initialize()

        # Start background checks
        if self.config.get("background_checks", True):
            if self.update_manager:
                await self.update_manager.start_background_checks()

        # Start auto updates if enabled
        if self.config.get("auto_update", False) and self.update_manager is not None:
            await self.update_manager.start_auto_updates()

        logger.info("Update system started")

    async def stop(self) -> None:
        """Stop the update system."""
        if self.update_manager:
            await self.update_manager.shutdown()

        if self.source_manager:
            await self.source_manager.close_all()

        logger.info("Update system stopped")

    def get_update_ui(self) -> UpdateUI | None:
        """Get the update UI component."""
        return self.update_ui

    async def check_updates(self) -> Any:
        """Check for updates."""
        if not self.update_manager:
            raise RuntimeError("Update system not initialized")

        return await self.update_manager.check_all_updates()

    async def install_update(self, module_id: str) -> bool:
        """Install update for a module."""
        if not self.update_manager:
            raise RuntimeError("Update system not initialized")

        return await self.update_manager.install_update(module_id)

    def get_update_history(self) -> list:
        """Get update history."""
        if not self.update_manager:
            return []

        return self.update_manager.get_update_history()

    def get_active_updates(self) -> dict:
        """Get active updates."""
        if not self.update_manager:
            return {}

        return self.update_manager.get_active_updates()

    def generate_key_pair(self, key_id: str, key_size: int = 2048) -> tuple[str, str]:
        """Generate a new key pair for signing updates."""
        if not self.security_validator:
            raise RuntimeError("Security validator not initialized")

        return self.security_validator.generate_key_pair(key_id, key_size)

    def list_available_keys(self) -> list[str]:
        """List available public keys."""
        if not self.security_validator:
            return []

        return self.security_validator.list_available_keys()

    def get_public_key_pem(self, key_id: str) -> str | None:
        """Get public key in PEM format."""
        if not self.security_validator:
            return None

        return self.security_validator.get_public_key_pem(key_id)


# Default configuration
DEFAULT_CONFIG = {
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
}


async def create_update_system(config: dict[str, Any] | None = None) -> UpdateSystem:
    """Create and initialize an update system."""
    if config is None:
        config = DEFAULT_CONFIG.copy()

    update_system = UpdateSystem(config)
    await update_system.initialize()

    return update_system


# Global update system instance
_global_update_system: UpdateSystem | None = None


async def get_global_update_system() -> UpdateSystem:
    """Get the global update system instance."""
    global _global_update_system

    if _global_update_system is None:
        _global_update_system = await create_update_system()

    return _global_update_system


def set_global_update_system(update_system: UpdateSystem) -> None:
    """Set the global update system instance."""
    global _global_update_system
    _global_update_system = update_system


async def initialize_global_update_system(
    config: dict[str, Any] | None = None,
) -> UpdateSystem:
    """Initialize the global update system."""
    update_system = await create_update_system(config)
    set_global_update_system(update_system)
    return update_system
