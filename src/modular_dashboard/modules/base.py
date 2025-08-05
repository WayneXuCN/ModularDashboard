"""Module base class."""

from abc import ABC, abstractmethod
from typing import Any

from ..utils.storage import CachedStorage, StorageBackend, get_storage_manager


class Module(ABC):
    """Base class for all dashboard modules.

    This abstract base class defines the common interface that all modules
    in the ModularDashboard system must implement. It provides standardized
    methods for data fetching, UI rendering, storage management, and update handling.

    Parameters
    ----------
    config : dict[str, Any] | None, default=None
        Optional dictionary containing module-specific configuration.
        Configuration keys are module-specific but can include common
        options like update settings, display preferences, etc.

    Attributes
    ----------
    config : dict[str, Any]
        Configuration dictionary for the module. Contains module-specific
        settings that affect behavior and presentation.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._storage: StorageBackend | None = None
        self._cache: CachedStorage | None = None
        self._storage_manager = get_storage_manager()

    def get_storage(self) -> StorageBackend:
        """Get module-specific storage backend.

        Returns a storage backend instance specific to this module,
        allowing for isolated data persistence. Storage is lazily
        initialized on first access.

        Returns
        -------
        StorageBackend
            Module-specific storage backend instance.
        """
        if self._storage is None:
            self._storage = self._storage_manager.get_module_storage(self.id)
        return self._storage

    def get_cache(self, default_ttl: int = 3600) -> CachedStorage:
        """Get module-specific cache with TTL support.

        Returns a cached storage instance specific to this module with
        time-to-live (TTL) support. Cache is lazily initialized on first access.

        Parameters
        ----------
        default_ttl : int, default=3600
            Default time-to-live in seconds for cached items.

        Returns
        -------
        CachedStorage
            Module-specific cached storage backend instance.
        """
        if self._cache is None:
            self._cache = self._storage_manager.get_module_cache(self.id, default_ttl)

            # Apply module-specific cache limits from config
            max_entries = self.config.get("max_cache_entries")
            if max_entries and hasattr(self._cache, "max_entries"):
                self._cache.max_entries = max_entries

        return self._cache

    def has_persistence(self) -> bool:
        """Check if module requires persistent storage.

        Override this method to indicate whether the module requires
        persistent data storage. Defaults to False.

        Returns
        -------
        bool
            True if module requires persistent storage, False otherwise.
        """
        return False

    def has_cache(self) -> bool:
        """Check if module uses caching.

        Override this method to indicate whether the module uses
        caching functionality. Defaults to False.

        Returns
        -------
        bool
            True if module uses caching, False otherwise.
        """
        return False

    def cleanup(self) -> None:
        """Clean up module resources.

        Perform any necessary cleanup operations such as removing
        expired cache entries. This method is called automatically
        during update operations and module shutdown.
        """
        if self._cache:
            self._cache.cleanup_expired()

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the module.

        This abstract property must be implemented by all subclasses.
        The ID should be a unique string that identifies the module type.

        Returns
        -------
        str
            Unique identifier for the module.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the module.

        This abstract property must be implemented by all subclasses.
        Should return a user-friendly name for display purposes.

        Returns
        -------
        str
            Human-readable name of the module.
        """
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon for the module.

        This abstract property must be implemented by all subclasses.
        Can be an emoji, SVG path, or other icon representation.

        Returns
        -------
        str
            Icon representation for the module.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the module does.

        This abstract property must be implemented by all subclasses.
        Should provide a concise description of the module's functionality.

        Returns
        -------
        str
            Description of the module's purpose and functionality.
        """
        pass

    @property
    def version(self) -> str:
        """Module version.

        Returns the current version of the module. Defaults to "1.0.0"
        but can be overridden by subclasses.

        Returns
        -------
        str
            Semantic version string (e.g., "1.0.0").
        """
        return "1.0.0"

    @property
    def update_source(self) -> str | None:
        """Update source for the module.

        Returns the configured update source for the module, if any.
        Common values might include "github", "pypi", etc.

        Returns
        -------
        str | None
            Update source identifier or None if not configured.
        """
        return self.config.get("update_source")

    @property
    def update_info(self) -> dict[str, Any]:
        """Update information for the module.

        Returns a dictionary containing information about module updates
        including version, source, channel, and auto-update settings.

        Returns
        -------
        dict[str, Any]
            Dictionary containing update-related information:
            - version: Current module version
            - update_source: Configured update source
            - update_channel: Update channel (default: "stable")
            - auto_update: Auto-update setting (default: False)
            - last_update_check: Timestamp of last update check
        """
        return {
            "version": self.version,
            "update_source": self.update_source,
            "update_channel": self.config.get("update_channel", "stable"),
            "auto_update": self.config.get("auto_update", False),
            "last_update_check": self.config.get("last_update_check"),
        }

    def supports_updates(self) -> bool:
        """Check if the module supports updates.

        Returns whether the module has been configured with an update
        source and can be automatically updated.

        Returns
        -------
        bool
            True if module supports updates, False otherwise.
        """
        return self.update_source is not None

    def prepare_for_update(self) -> bool:
        """Prepare the module for update.

        Perform necessary operations before updating the module,
        such as backing up data and cleaning up resources.

        Returns
        -------
        bool
            True if preparation was successful, False otherwise.
        """
        try:
            # Backup data if needed
            if self.has_persistence():
                # storage = self.get_storage()
                # This could be extended to create a backup
                pass

            # Clean up resources
            self.cleanup()
            return True
        except Exception:
            return False

    def post_update_cleanup(self) -> None:
        """Clean up after update.

        Perform cleanup operations after a module update has been
        completed. By default, this just calls the standard cleanup method.
        """
        self.cleanup()

    def handle_update_error(self, error: Exception) -> None:  # noqa: B027
        """Handle update errors.

        Handle any errors that occur during the module update process.
        This default implementation does nothing but can be overridden
        by subclasses to provide custom error handling.

        Parameters
        ----------
        error : Exception
            The exception that occurred during the update process.
        """
        # Default implementation - can be overridden by modules
        pass

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """Fetch data from the source and return standardized items.

        This abstract method must be implemented by all subclasses.
        It should retrieve data from the module's data source and
        return it in a standardized format.

        Returns
        -------
        list[dict[str, Any]]
            List of items with standardized keys:
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
        """Render the module's UI using NiceGUI components.

        This abstract method must be implemented by all subclasses.
        It should create the UI components for displaying the module's
        data using NiceGUI elements.
        """
        pass

    def render_detail(self) -> None:
        """Render the module's detailed view page.

        Render a detailed view of the module's data. By default,
        this shows the same content as the main view, but modules
        can override this for a more detailed presentation.

        This method is typically used when a user clicks on a
        module to see more detailed information.
        """
        self.render()
