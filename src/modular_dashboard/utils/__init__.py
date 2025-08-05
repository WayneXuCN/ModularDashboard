"""Utility modules for the modular dashboard."""

from .lazy_module import LazyModuleWrapper, ModuleCache, module_cache
from .module_stats import ModuleStatsCollector, stats_collector

__all__ = [
    "LazyModuleWrapper",
    "ModuleCache",
    "module_cache",
    "ModuleStatsCollector",
    "stats_collector",
]
