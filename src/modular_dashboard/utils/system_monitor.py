"""System monitoring and performance tracking utilities.

This module provides unified system monitoring capabilities including:
- Memory usage monitoring and management
- Module initialization performance tracking
- System resource statistics collection
- Automated cleanup and optimization
"""

import gc
import logging
import threading
import time
import weakref
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from ..config.memory_config import CacheStats, MemoryConfig


@dataclass
class ModuleInitStats:
    """Statistics for module initialization."""

    module_id: str
    init_time: float
    memory_usage: int = 0
    init_count: int = 0
    last_init_time: float = 0


class PerformanceTracker:
    """Track module initialization performance."""

    def __init__(self):
        self._stats: dict[str, ModuleInitStats] = {}
        self._total_init_time = 0.0
        self._total_init_count = 0
        self._lock = threading.RLock()

    def record_init(
        self, module_id: str, init_time: float, memory_usage: int = 0
    ) -> None:
        """Record module initialization statistics."""
        module_id_str = str(module_id)

        with self._lock:
            if module_id_str not in self._stats:
                self._stats[module_id_str] = ModuleInitStats(
                    module_id=module_id_str,
                    init_time=init_time,
                    memory_usage=memory_usage,
                    init_count=1,
                    last_init_time=time.time(),
                )
            else:
                self._stats[module_id_str].init_time = init_time
                self._stats[module_id_str].memory_usage = memory_usage
                self._stats[module_id_str].init_count += 1
                self._stats[module_id_str].last_init_time = time.time()

            self._total_init_time += init_time
            self._total_init_count += 1

    def get_stats(self, module_id: str | None = None) -> dict[str, Any]:
        """Get module statistics."""
        with self._lock:
            if module_id:
                stat = self._stats.get(module_id)
                return stat.__dict__ if stat else {}

            return {
                "total_modules": len(self._stats),
                "total_init_time": self._total_init_time,
                "total_init_count": self._total_init_count,
                "average_init_time": self._total_init_time
                / max(self._total_init_count, 1),
                "modules": {mid: stat.__dict__ for mid, stat in self._stats.items()},
            }

    def get_performance_summary(self) -> str:
        """Get human-readable performance summary."""
        with self._lock:
            if not self._stats:
                return "No modules initialized yet."

            slowest_module = max(self._stats.values(), key=lambda x: x.init_time)
            fastest_module = min(self._stats.values(), key=lambda x: x.init_time)

            slowest_id = str(slowest_module.module_id)
            fastest_id = str(fastest_module.module_id)

            return (
                f"Module Performance Summary:\n"
                f"- Total modules: {len(self._stats)}\n"
                f"- Total init time: {self._total_init_time:.2f}s\n"
                f"- Average init time: {self._total_init_time / max(self._total_init_count, 1):.3f}s\n"
                f"- Slowest: {slowest_id} ({slowest_module.init_time:.3f}s)\n"
                f"- Fastest: {fastest_id} ({fastest_module.init_time:.3f}s)"
            )


class MemoryMonitor:
    """Monitor memory usage and trigger cleanup when needed."""

    def __init__(self, config: MemoryConfig):
        self.config = config
        self.stats = CacheStats()
        self.running = False
        self._monitor_thread: threading.Thread | None = None
        self._lock = threading.RLock()
        self._cleanup_callbacks: list[Callable[[], None]] = []

    def start_monitoring(self) -> None:
        """Start memory monitoring in background thread."""
        if self.running:
            return

        self.running = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True, name="MemoryMonitor"
        )
        self._monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop memory monitoring."""
        self.running = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)

    def register_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """Register a cleanup callback to be called when memory is low."""
        with self._lock:
            self._cleanup_callbacks.append(callback)

    def unregister_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """Unregister a cleanup callback."""
        with self._lock:
            if callback in self._cleanup_callbacks:
                self._cleanup_callbacks.remove(callback)

    def get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        if not HAS_PSUTIL:
            return 0

        try:
            process = psutil.Process()
            return process.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0

    def get_memory_usage_percent(self) -> float:
        """Get memory usage percentage."""
        if not HAS_PSUTIL:
            return 0.0

        try:
            memory = psutil.virtual_memory()
            return memory.percent
        except Exception:
            return 0.0

    def get_system_memory_info(self) -> dict[str, Any]:
        """Get comprehensive system memory information."""
        if not HAS_PSUTIL:
            return {"error": "psutil not available"}

        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()

            return {
                "virtual": {
                    "total": virtual_memory.total,
                    "available": virtual_memory.available,
                    "used": virtual_memory.used,
                    "free": virtual_memory.free,
                    "percent": virtual_memory.percent,
                    "active": getattr(virtual_memory, "active", None),
                    "inactive": getattr(virtual_memory, "inactive", None),
                    "buffers": getattr(virtual_memory, "buffers", None),
                    "cached": getattr(virtual_memory, "cached", None),
                },
                "swap": {
                    "total": swap_memory.total,
                    "used": swap_memory.used,
                    "free": swap_memory.free,
                    "percent": swap_memory.percent,
                    "sin": swap_memory.sin,
                    "sout": swap_memory.sout,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def should_cleanup(self) -> bool:
        """Check if cleanup should be triggered."""
        if not HAS_PSUTIL:
            return False

        memory_percent = self.get_memory_usage_percent()
        return memory_percent >= self.config.memory_threshold_percent

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.running:
            try:
                if self.should_cleanup():
                    self._trigger_cleanup()
                time.sleep(self.config.cleanup_interval_seconds)
            except Exception as e:
                logging.getLogger(__name__).error(f"Memory monitor error: {e}")
                time.sleep(5)

    def _trigger_cleanup(self) -> None:
        """Trigger cleanup callbacks."""
        with self._lock:
            callbacks = self._cleanup_callbacks.copy()

        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                logging.getLogger(__name__).error(f"Cleanup callback error: {e}")

        gc.collect()
        self.stats.last_cleanup = time.time()


class SystemMonitor:
    """Unified system monitoring combining memory and performance tracking."""

    def __init__(self, config: MemoryConfig):
        self.config = config
        self.memory_monitor = MemoryMonitor(config)
        self.performance_tracker = PerformanceTracker()

    def start_monitoring(self) -> None:
        """Start all monitoring systems."""
        self.memory_monitor.start_monitoring()

    def stop_monitoring(self) -> None:
        """Stop all monitoring systems."""
        self.memory_monitor.stop_monitoring()

    def record_module_init(
        self, module_id: str, init_time: float, memory_usage: int = 0
    ) -> None:
        """Record module initialization with both performance and memory data."""
        self.performance_tracker.record_init(module_id, init_time, memory_usage)

    def get_comprehensive_stats(self) -> dict[str, Any]:
        """Get comprehensive system statistics."""
        return {
            "performance": self.performance_tracker.get_stats(),
            "memory": self.memory_monitor.get_system_memory_info(),
            "memory_usage_percent": self.memory_monitor.get_memory_usage_percent(),
            "memory_usage_bytes": self.memory_monitor.get_memory_usage(),
        }

    def register_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """Register cleanup callback with memory monitor."""
        self.memory_monitor.register_cleanup_callback(callback)


class WeakValueCache:
    """Cache that uses weak references for automatic cleanup."""

    def __init__(self):
        self._cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()

    def get(self, key: str) -> Any | None:
        """Get value from cache."""
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = value

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

    def keys(self) -> list[str]:
        """Get all cache keys."""
        return list(self._cache.keys())


class CompressedCache:
    """Cache with compression support for large objects."""

    def __init__(self, max_size_mb: float = 5.0):
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def should_compress(self, obj: Any) -> bool:
        """Check if object should be compressed."""
        try:
            import sys

            size = sys.getsizeof(obj)
            return size > 1024 and size < self.max_size_bytes
        except Exception:
            return False

    def compress(self, obj: Any) -> bytes:
        """Compress object using pickle and gzip."""
        import gzip
        import pickle

        return gzip.compress(pickle.dumps(obj))

    def decompress(self, data: bytes) -> Any:
        """Decompress object."""
        import gzip
        import pickle

        return pickle.loads(gzip.decompress(data))


# Global instances
_system_monitor: SystemMonitor | None = None
_performance_tracker: PerformanceTracker | None = None


def get_system_monitor(config: MemoryConfig | None = None) -> SystemMonitor:
    """Get global system monitor instance."""
    global _system_monitor
    if _system_monitor is None and config is not None:
        _system_monitor = SystemMonitor(config)
    return _system_monitor


def get_performance_tracker() -> PerformanceTracker:
    """Get global performance tracker instance."""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker


# Backward compatibility aliases
def get_memory_monitor(config: MemoryConfig | None = None) -> MemoryMonitor:
    """Backward compatibility - get memory monitor from system monitor."""
    system_monitor = get_system_monitor(config)
    return system_monitor.memory_monitor if system_monitor else None


def get_module_stats() -> PerformanceTracker:
    """Backward compatibility - get module stats collector."""
    return get_performance_tracker()
