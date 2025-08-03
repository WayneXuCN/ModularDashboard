"""Module base class."""

from abc import ABC, abstractmethod
from typing import Any

from ..storage import CachedStorage, StorageBackend, get_storage_manager


class Module(ABC):
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the module with optional configuration.

        Args:
            config: Optional dictionary containing module-specific configuration
        """
        self.config = config or {}
        self._storage: StorageBackend | None = None
        self._cache: CachedStorage | None = None
        self._storage_manager = get_storage_manager()

    def get_storage(self) -> StorageBackend:
        """Get module-specific storage backend."""
        if self._storage is None:
            self._storage = self._storage_manager.get_module_storage(self.id)
        return self._storage

    def get_cache(self, default_ttl: int = 3600) -> CachedStorage:
        """Get module-specific cache with TTL support."""
        if self._cache is None:
            self._cache = self._storage_manager.get_module_cache(self.id, default_ttl)
        return self._cache

    def has_persistence(self) -> bool:
        """Check if module requires persistent storage."""
        return False

    def has_cache(self) -> bool:
        """Check if module uses caching."""
        return False

    def cleanup(self) -> None:
        """Clean up module resources."""
        if self._cache:
            self._cache.cleanup_expired()

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the module."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the module."""
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon for the module (e.g., emoji or SVG path)."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the module does."""
        pass

    @property
    def version(self) -> str:
        """Module version."""
        return "1.0.0"

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """
        Fetch data from the source and return standardized items.

        Returns:
            List of items with keys:
            - title (str): Item title
            - summary (str): Brief description
            - link (str): URL to the full item
            - published (str): ISO8601 formatted date
            - tags (List[str]): Optional tags
            - extra (Dict): Optional extra fields
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        Render the module's UI using NiceGUI components.
        """
        pass

    def render_detail(self) -> None:
        """
        Render the module's detailed view page.
        By default, it shows the same content as the main view,
        but modules can override this for a more detailed presentation.
        """
        self.render()
