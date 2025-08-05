"""Utility modules for the modular dashboard."""

from .lazy_module import LazyModuleWrapper, ModuleCache, module_cache
from .system_monitor import PerformanceTracker, get_performance_tracker

stats_collector = get_performance_tracker()
ModuleStatsCollector = PerformanceTracker

__all__ = [
    "LazyModuleWrapper",
    "ModuleCache",
    "module_cache",
    "ModuleStatsCollector",
    "stats_collector",
]
