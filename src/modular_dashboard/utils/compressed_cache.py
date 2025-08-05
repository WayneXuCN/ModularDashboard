"""Compressed cache utilities for memory optimization."""

import gzip
import json
import pickle
import sys
from typing import Any


class CompressedCacheEntry:
    """Represents a compressed cache entry."""

    def __init__(self, original_data: Any, compressed_data: bytes, original_size: int):
        self.original_data = original_data
        self.compressed_data = compressed_data
        self.original_size = original_size
        self.compressed_size = len(compressed_data)
        self.compression_ratio = (
            len(compressed_data) / original_size if original_size > 0 else 1.0
        )


class CompressedCache:
    """Cache with compression support for large objects."""

    def __init__(
        self,
        compression_threshold: int = 1024,  # 1KB
        compression_level: int = 6,
        max_entry_size: int = 5 * 1024 * 1024,
    ):  # 5MB
        self.compression_threshold = compression_threshold
        self.compression_level = compression_level
        self.max_entry_size = max_entry_size

    def should_compress(self, obj: Any) -> bool:
        """Check if object should be compressed based on size."""
        try:
            size = sys.getsizeof(obj)
            return size >= self.compression_threshold and size <= self.max_entry_size
        except (TypeError, ValueError):
            return False

    def compress(self, obj: Any) -> CompressedCacheEntry:
        """Compress object using pickle and gzip."""
        serialized = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        original_size = len(serialized)

        compressed = gzip.compress(serialized, compresslevel=self.compression_level)

        return CompressedCacheEntry(obj, compressed, original_size)

    def decompress(self, compressed_entry: CompressedCacheEntry) -> Any:
        """Decompress object."""
        decompressed = gzip.decompress(compressed_entry.compressed_data)
        return pickle.loads(decompressed)

    def estimate_size(self, obj: Any) -> int:
        """Estimate serialized size of object."""
        try:
            return sys.getsizeof(obj)
        except (TypeError, ValueError):
            return 0


class JsonCompressedCache(CompressedCache):
    """Compressed cache optimized for JSON-serializable objects."""

    def compress(self, obj: Any) -> CompressedCacheEntry:
        """Compress JSON-serializable object."""
        serialized = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        original_size = len(serialized)

        compressed = gzip.compress(serialized, compresslevel=self.compression_level)

        return CompressedCacheEntry(obj, compressed, original_size)

    def decompress(self, compressed_entry: CompressedCacheEntry) -> Any:
        """Decompress JSON object."""
        decompressed = gzip.decompress(compressed_entry.compressed_data)
        return json.loads(decompressed.decode("utf-8"))


class MemoryEfficientCache:
    """Memory-efficient cache with compression and size limits."""

    def __init__(self, max_size_mb: int = 50, compression_threshold: int = 1024):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.compression_threshold = compression_threshold
        self._cache: dict[str, Any] = {}
        self._sizes: dict[str, int] = {}
        self._total_size = 0
        self.compressor = CompressedCache(compression_threshold)

    def get(self, key: str) -> Any | None:
        """Get value from cache."""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if isinstance(entry, CompressedCacheEntry):
            return self.compressor.decompress(entry)
        return entry

    def set(self, key: str, value: Any) -> bool:
        """Set value in cache with size management."""
        # Remove existing entry
        if key in self._cache:
            self._total_size -= self._sizes[key]
            del self._cache[key]
            del self._sizes[key]

        # Estimate size
        estimated_size = self.compressor.estimate_size(value)

        # Check if we need to compress
        if estimated_size >= self.compression_threshold:
            try:
                compressed = self.compressor.compress(value)
                entry = compressed
                actual_size = compressed.compressed_size
            except Exception:
                entry = value
                actual_size = estimated_size
        else:
            entry = value
            actual_size = estimated_size

        # Ensure we have space
        while self._total_size + actual_size > self.max_size_bytes and self._cache:
            # Remove oldest entry
            oldest_key = next(iter(self._cache))
            self._total_size -= self._sizes[oldest_key]
            del self._cache[oldest_key]
            del self._sizes[oldest_key]

        # Add new entry
        self._cache[key] = entry
        self._sizes[key] = actual_size
        self._total_size += actual_size

        return True

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            self._total_size -= self._sizes[key]
            del self._cache[key]
            del self._sizes[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._sizes.clear()
        self._total_size = 0

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        compressed_count = sum(
            1 for v in self._cache.values() if isinstance(v, CompressedCacheEntry)
        )
        return {
            "size": len(self._cache),
            "total_size_mb": self._total_size / (1024 * 1024),
            "max_size_mb": self.max_size_bytes / (1024 * 1024),
            "compression_ratio": compressed_count / len(self._cache)
            if self._cache
            else 0.0,
            "compressed_entries": compressed_count,
        }
