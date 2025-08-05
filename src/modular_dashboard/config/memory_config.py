"""Memory management configuration."""

from dataclasses import dataclass


@dataclass
class MemoryConfig:
    """Configuration for memory management and caching."""

    max_cache_size: int = 1000  # Maximum number of cache entries
    max_memory_mb: int = 100  # Maximum memory usage in MB
    cache_ttl_seconds: int = 3600  # Default TTL for cache entries
    enable_compression: bool = True  # Enable cache compression
    cleanup_interval_seconds: int = 300  # Automatic cleanup interval
    memory_threshold_percent: int = 80  # Memory usage threshold for cleanup
    enable_lru_eviction: bool = True  # Enable LRU eviction policy
    max_entry_size_mb: float = 5.0  # Maximum size per cache entry in MB
    enable_weak_refs: bool = False  # Use weak references for large objects
    debug_memory_usage: bool = False  # Enable memory usage debugging


@dataclass
class CacheStats:
    """Cache usage statistics."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    memory_usage_bytes: int = 0
    last_cleanup: float | None = None

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    @property
    def memory_usage_mb(self) -> float:
        """Get memory usage in MB."""
        return self.memory_usage_bytes / (1024 * 1024)
