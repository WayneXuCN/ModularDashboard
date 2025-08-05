"""Lightweight data storage manager for modules."""

import contextlib
import json
import pickle
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config.memory_config import MemoryConfig
from .utils.system_monitor import get_memory_monitor


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def DateTimeDecoder(dct: dict[str, Any]) -> dict[str, Any]:
    """JSON decoder that converts ISO datetime strings back to datetime objects."""
    for key, value in dct.items():
        if isinstance(value, str) and key.endswith("_at"):
            with contextlib.suppress(ValueError, TypeError):
                dct[key] = datetime.fromisoformat(value)
    return dct


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value by key."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all data."""
        pass

    @abstractmethod
    def keys(self) -> list[str]:
        """Return all keys in storage."""
        pass


class JSONFileBackend(StorageBackend):
    """JSON file storage backend."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load data from file."""
        if self.file_path.exists():
            try:
                with open(self.file_path, encoding="utf-8") as f:
                    self._data = json.load(f, object_hook=DateTimeDecoder)
            except (OSError, json.JSONDecodeError):
                self._data = {}

    def _save(self) -> None:
        """Save data to file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(
                    self._data, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder
                )
        except OSError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        """Delete value by key."""
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()
        self._save()

    def keys(self) -> list[str]:
        """Return all keys in storage."""
        return list(self._data.keys())


class PickleFileBackend(StorageBackend):
    """Pickle file storage backend for complex objects."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load data from file."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "rb") as f:
                    self._data = pickle.load(f)
            except (OSError, pickle.PickleError):
                self._data = {}

    def _save(self) -> None:
        """Save data to file."""
        try:
            with open(self.file_path, "wb") as f:
                pickle.dump(self._data, f)
        except OSError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        """Delete value by key."""
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()

    def keys(self) -> list[str]:
        """Return all keys in storage."""
        return list(self._data.keys())
        self._save()


class MemoryBackend(StorageBackend):
    """In-memory storage backend."""

    def __init__(self):
        self._data: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value by key."""
        self._data[key] = value

    def delete(self, key: str) -> bool:
        """Delete value by key."""
        if key in self._data:
            del self._data[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()

    def keys(self) -> list[str]:
        """Return all keys in storage."""
        return list(self._data.keys())


class CachedStorage:
    """Cached storage wrapper with TTL support and memory management."""

    def __init__(
        self, backend: StorageBackend, default_ttl: int = 3600, max_entries: int = 1000
    ):
        self.backend = backend
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self._cache: dict[str, dict[str, Any]] = {}
        self._access_order: list[str] = []  # LRU tracking
        self._stats = {"hits": 0, "misses": 0, "evictions": 0, "memory_usage": 0}

    def _is_expired(self, cache_entry: dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        if "expires_at" not in cache_entry:
            return True
        return datetime.now() > cache_entry["expires_at"]

    def _get_cache_key(self, key: str) -> str:
        """Get cache key with module prefix."""
        return f"cache_{key}"

    def get(self, key: str, default: Any = None) -> Any:
        """Get cached value if not expired."""
        cache_key = self._get_cache_key(key)

        # Check memory cache first
        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if not self._is_expired(cache_entry):
                return cache_entry["value"]
            else:
                del self._cache[cache_key]

        # Check persistent cache
        cache_data = self.backend.get(cache_key)
        if cache_data and not self._is_expired(cache_data):
            # Restore to memory cache
            self._cache[cache_key] = cache_data
            return cache_data["value"]

        return default

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set cached value with TTL and memory management."""
        cache_key = self._get_cache_key(key)
        ttl = ttl or self.default_ttl

        cache_entry = {
            "value": value,
            "expires_at": datetime.now() + timedelta(seconds=ttl),
            "created_at": datetime.now(),
        }

        # Ensure we have space for new entry
        self._ensure_cache_space()

        # Store in memory cache
        self._cache[cache_key] = cache_entry
        self._update_access_order(cache_key)

        # Store in persistent cache
        self.backend.set(cache_key, cache_entry)

    def delete(self, key: str) -> bool:
        """Delete cached value."""
        cache_key = self._get_cache_key(key)

        # Delete from memory cache
        if cache_key in self._cache:
            del self._cache[cache_key]

        # Delete from persistent cache
        return self.backend.delete(cache_key)

    def exists(self, key: str) -> bool:
        """Check if cached value exists."""
        return self.get(key) is not None

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._access_order.clear()
        self._reset_stats()
        # Clear only cache entries from backend
        for key in self.backend.keys():  # noqa: SIM118
            if key.startswith("cache_"):
                self.backend.delete(key)

    def cleanup_expired(self) -> None:
        """Clean up expired cache entries."""
        expired_keys = []
        for cache_key, cache_entry in self._cache.items():
            if self._is_expired(cache_entry):
                expired_keys.append(cache_key)

        for key in expired_keys:
            self._remove_from_cache(key)

    def cleanup_lru(self, count: int = None) -> None:
        """Clean up least recently used entries."""
        if count is None:
            count = max(1, len(self._cache) // 10)  # Remove 10% or at least 1

        keys_to_remove = self._access_order[:count]
        for key in keys_to_remove:
            self._remove_from_cache(key)
            self._stats["evictions"] += 1

    def get_stats(self) -> dict:
        """Get cache statistics."""
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "evictions": self._stats["evictions"],
            "size": len(self._cache),
            "max_size": self.max_entries,
            "hit_rate": self._stats["hits"]
            / (self._stats["hits"] + self._stats["misses"])
            if (self._stats["hits"] + self._stats["misses"]) > 0
            else 0.0,
        }

    def _ensure_cache_space(self) -> None:
        """Ensure we have space for new cache entry."""
        if len(self._cache) >= self.max_entries:
            # Remove oldest entries based on LRU
            remove_count = min(10, len(self._cache) - self.max_entries + 1)
            self.cleanup_lru(remove_count)

    def _update_access_order(self, key: str) -> None:
        """Update LRU access order."""
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def _remove_from_cache(self, key: str) -> None:
        """Remove key from cache and access order."""
        if key in self._cache:
            del self._cache[key]
        if key in self._access_order:
            self._access_order.remove(key)

    def _reset_stats(self) -> None:
        """Reset cache statistics."""
        self._stats.update({"hits": 0, "misses": 0, "evictions": 0, "memory_usage": 0})


class StorageManager:
    """Centralized storage manager for modules."""

    def __init__(
        self, base_path: str | Path | None = None, memory_config: MemoryConfig = None
    ):
        if base_path is None:
            base_path = Path.home() / ".modular_dashboard"

        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Initialize memory configuration
        self.memory_config = memory_config or MemoryConfig()
        self.memory_monitor = get_memory_monitor(self.memory_config)
        if self.memory_monitor:
            self.memory_monitor.start_monitoring()

        # Initialize storage backends
        self._backends: dict[str, StorageBackend] = {}
        self._cached_storages: dict[str, CachedStorage] = {}

    def get_backend(self, name: str, backend_type: str = "json") -> StorageBackend:
        """Get or create storage backend."""
        if name not in self._backends:
            file_path = (
                self.base_path / f"{name}.{'json' if backend_type == 'json' else 'pkl'}"
            )

            if backend_type == "json":
                self._backends[name] = JSONFileBackend(file_path)
            elif backend_type == "pickle":
                self._backends[name] = PickleFileBackend(file_path)
            elif backend_type == "memory":
                self._backends[name] = MemoryBackend()
            else:
                raise ValueError(f"Unsupported backend type: {backend_type}")

        return self._backends[name]

    def get_cached_storage(
        self, name: str, default_ttl: int = 3600, max_entries: int = None
    ) -> CachedStorage:
        """Get or create cached storage with memory management."""
        if name not in self._cached_storages:
            backend = self.get_backend(name)
            max_entries = max_entries or self.memory_config.max_cache_size
            self._cached_storages[name] = CachedStorage(
                backend,
                default_ttl or self.memory_config.cache_ttl_seconds,
                max_entries=max_entries,
            )

            # Register cleanup callback with memory monitor
            if self.memory_monitor:
                self.memory_monitor.register_cleanup_callback(
                    self._cached_storages[name].cleanup_expired
                )

        return self._cached_storages[name]

    def get_module_storage(self, module_id: str) -> StorageBackend:
        """Get storage for a specific module."""
        return self.get_backend(f"module_{module_id}")

    def get_module_cache(
        self, module_id: str, default_ttl: int = 3600
    ) -> CachedStorage:
        """Get cache for a specific module."""
        return self.get_cached_storage(f"module_{module_id}", default_ttl)

    def cleanup_expired_caches(self) -> None:
        """Clean up expired cache entries in all cached storages."""
        for cached_storage in self._cached_storages.values():
            cached_storage.cleanup_expired()

    def clear_all(self) -> None:
        """Clear all storage and caches."""
        for backend in self._backends.values():
            backend.clear()
        for cached_storage in self._cached_storages.values():
            cached_storage.clear()


# Global storage manager instance
_storage_manager: StorageManager | None = None


def get_storage_manager() -> StorageManager:
    """Get the global storage manager instance."""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = StorageManager()
    return _storage_manager


def set_storage_manager(manager: StorageManager) -> None:
    """Set the global storage manager instance."""
    global _storage_manager
    _storage_manager = manager
