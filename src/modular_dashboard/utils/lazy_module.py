"""Lazy module loading for performance optimization."""

import threading
import time
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..modules.base import Module

from .system_monitor import get_performance_tracker

stats_collector = get_performance_tracker()


class LazyModuleWrapper:
    """Lazy module wrapper that delays module instantiation until needed.

    This wrapper prevents immediate instantiation of all modules during dashboard
    initialization, reducing startup time by only loading modules when they are
    actually accessed.
    """

    def __init__(
        self,
        module_class: type["Module"],
        config: dict[str, Any],
        module_id: str = None,
    ):
        self._module_class = module_class
        self._config = config
        self._instance: Module | None = None
        self._lock = threading.RLock()
        self._module_id = module_id or getattr(module_class, "id", str(module_class))

    def __getattr__(self, name: str) -> Any:
        """Lazy attribute access - instantiate module on first access."""
        if self._instance is None:
            with self._lock:
                if self._instance is None:  # Double-check pattern
                    start_time = time.time()
                    try:
                        self._instance = self._module_class(self._config)
                        init_time = time.time() - start_time
                        stats_collector.record_init(self._module_id, init_time)
                    except Exception as e:
                        init_time = time.time() - start_time
                        stats_collector.record_init(self._module_id, init_time)
                        raise e
        return getattr(self._instance, name)

    def get_instance(self) -> "Module":
        """Get the actual module instance, creating it if necessary."""
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    start_time = time.time()
                    try:
                        self._instance = self._module_class(self._config)
                        init_time = time.time() - start_time
                        stats_collector.record_init(self._module_id, init_time)
                    except Exception as e:
                        init_time = time.time() - start_time
                        stats_collector.record_init(self._module_id, init_time)
                        raise e
        return self._instance

    def is_initialized(self) -> bool:
        """Check if the module has been initialized."""
        return self._instance is not None

    def reset(self) -> None:
        """Reset the module instance (for testing/debugging)."""
        with self._lock:
            if self._instance is not None:
                if hasattr(self._instance, "cleanup"):
                    self._instance.cleanup()
                self._instance = None


class ModuleCache:
    """Thread-safe cache for lazy module instances."""

    def __init__(self):
        self._cache: dict[str, LazyModuleWrapper] = {}
        self._lock = threading.RLock()

    def get_or_create(
        self, module_id: str, module_class: type["Module"], config: dict[str, Any]
    ) -> LazyModuleWrapper:
        """Get or create a lazy module wrapper for the given module."""
        if module_id not in self._cache:
            with self._lock:
                if module_id not in self._cache:
                    self._cache[module_id] = LazyModuleWrapper(module_class, config)
        return self._cache[module_id]

    def get_instance(self, module_id: str) -> Optional["Module"]:
        """Get the actual module instance if it exists."""
        wrapper = self._cache.get(module_id)
        return wrapper.get_instance() if wrapper else None

    def clear(self) -> None:
        """Clear all cached modules."""
        with self._lock:
            for wrapper in self._cache.values():
                wrapper.reset()
            self._cache.clear()


# Global module cache instance
module_cache = ModuleCache()
