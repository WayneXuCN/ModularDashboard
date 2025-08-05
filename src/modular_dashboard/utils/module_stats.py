"""Module initialization statistics and debugging utilities."""

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class ModuleInitStats:
    """Statistics for module initialization."""

    module_id: str
    init_time: float
    memory_usage: int = 0
    init_count: int = 0
    last_init_time: float = 0


class ModuleStatsCollector:
    """Collect and manage module initialization statistics."""

    def __init__(self):
        self._stats: dict[str, ModuleInitStats] = {}
        self._total_init_time = 0.0
        self._total_init_count = 0

    def record_init(
        self, module_id: str, init_time: float, memory_usage: int = 0
    ) -> None:
        """Record module initialization statistics."""
        if module_id not in self._stats:
            self._stats[module_id] = ModuleInitStats(
                module_id=module_id,
                init_time=init_time,
                memory_usage=memory_usage,
                init_count=1,
                last_init_time=time.time(),
            )
        else:
            self._stats[module_id].init_time = init_time
            self._stats[module_id].memory_usage = memory_usage
            self._stats[module_id].init_count += 1
            self._stats[module_id].last_init_time = time.time()

        self._total_init_time += init_time
        self._total_init_count += 1

    def get_stats(self, module_id: str = None) -> dict[str, Any]:
        """Get module statistics."""
        if module_id:
            return (
                self._stats.get(module_id).__dict__ if module_id in self._stats else {}
            )

        return {
            "total_modules": len(self._stats),
            "total_init_time": self._total_init_time,
            "total_init_count": self._total_init_count,
            "average_init_time": self._total_init_time / max(self._total_init_count, 1),
            "modules": {mid: stat.__dict__ for mid, stat in self._stats.items()},
        }

    def get_performance_summary(self) -> str:
        """Get a human-readable performance summary."""
        if not self._stats:
            return "No modules initialized yet."

        slowest_module = max(self._stats.values(), key=lambda x: x.init_time)
        fastest_module = min(self._stats.values(), key=lambda x: x.init_time)

        return (
            f"Module Performance Summary:\n"
            f"- Total modules: {len(self._stats)}\n"
            f"- Total init time: {self._total_init_time:.2f}s\n"
            f"- Average init time: {self._total_init_time / max(self._total_init_count, 1):.3f}s\n"
            f"- Slowest: {slowest_module.module_id} ({slowest_module.init_time:.3f}s)\n"
            f"- Fastest: {fastest_module.module_id} ({fastest_module.init_time:.3f}s)"
        )


# Global stats collector
stats_collector = ModuleStatsCollector()
