"""Unified statistics and memory monitoring dashboard UI."""

from typing import Any

from nicegui import ui

from ..utils.storage import get_storage_manager
from ..utils.system_monitor import get_memory_monitor, get_performance_tracker

memory_monitor = get_memory_monitor()
stats_collector = get_performance_tracker()


class StatsDashboardUI:
    """Unified dashboard for performance and memory statistics."""

    def __init__(self):
        self.storage_manager = get_storage_manager()
        self.memory_monitor = get_memory_monitor()

    def render_dashboard(self) -> None:
        """Render complete unified dashboard."""
        with ui.column().classes("w-full p-6 max-w-6xl mx-auto"):
            self._render_header()
            self._render_summary_cards()
            self._render_performance_section()
            self._render_memory_section()
            self._render_actions_section()

    def _render_header(self) -> None:
        """Render dashboard header."""
        with ui.row().classes("w-full items-center mb-6"):
            ui.button(
                "← 返回",
                on_click=lambda: ui.navigate.to("/"),
            ).classes(
                "px-4 py-2 bg-blue-600 text-white rounded-lg "
                "hover:bg-blue-700 transition-colors"
            )
            ui.label("系统统计与监控").classes("text-3xl font-bold text-center flex-1")

    def _render_summary_cards(self) -> None:
        """Render summary statistics cards."""
        with ui.row().classes("w-full gap-4 mb-6"):
            # Performance summary
            stats_collector.get_performance_summary()

            # Module count
            stats = stats_collector.get_stats()
            total_modules = stats.get("total_modules", 0)

            # Cache statistics
            total_entries = 0
            total_hits = 0
            total_misses = 0

            for _name, cache in self.storage_manager._cached_storages.items():
                if hasattr(cache, "get_stats"):
                    cache_stats = cache.get_stats()
                    total_entries += cache_stats.get("size", 0)
                    total_hits += cache_stats.get("hits", 0)
                    total_misses += cache_stats.get("misses", 0)

            hit_rate = (
                total_hits / (total_hits + total_misses)
                if (total_hits + total_misses) > 0
                else 0
            )

            # Create cards
            cards = [
                ("总模块数", str(total_modules), "text-blue-600"),
                ("缓存条目", str(total_entries), "text-green-600"),
                ("缓存命中率", f"{hit_rate:.1%}", "text-purple-600"),
                (
                    "总初始化时间",
                    f"{stats.get('total_init_time', 0):.3f}s",
                    "text-orange-600",
                ),
            ]

            for label, value, color in cards:
                with ui.card().classes("p-4 flex-1 text-center"):
                    ui.label(value).classes(f"text-2xl font-bold {color}")
                    ui.label(label).classes("text-sm text-gray-600")

    def _render_performance_section(self) -> None:
        """Render performance statistics section."""
        with ui.card().classes("w-full p-4 mb-6"):
            ui.label("模块性能统计").classes("text-xl font-semibold mb-4")

            stats = stats_collector.get_stats()
            if stats.get("modules"):
                self._render_module_performance_table(stats)
            else:
                ui.label("暂无模块加载数据").classes("text-gray-500 text-center py-8")

    def _render_module_performance_table(self, stats: dict[str, Any]) -> None:
        """Render module performance table."""
        columns = [
            {
                "name": "module_id",
                "label": "模块ID",
                "field": "module_id",
                "align": "left",
            },
            {
                "name": "init_time",
                "label": "初始化时间",
                "field": "init_time",
                "align": "center",
            },
            {
                "name": "init_count",
                "label": "初始化次数",
                "field": "init_count",
                "align": "center",
            },
            {
                "name": "last_init",
                "label": "最后初始化",
                "field": "last_init_time",
                "align": "center",
            },
            {
                "name": "cache_entries",
                "label": "缓存条目",
                "field": "cache_entries",
                "align": "center",
            },
            {
                "name": "cache_hit_rate",
                "label": "缓存命中率",
                "field": "cache_hit_rate",
                "align": "center",
            },
        ]

        rows = []
        for module_id, module_stats in stats["modules"].items():
            # Cache info for this module
            cache_key = f"module_{module_id}"
            cache_entries = 0
            cache_hit_rate = "0%"

            if cache_key in self.storage_manager._cached_storages:
                cache = self.storage_manager._cached_storages[cache_key]
                if hasattr(cache, "get_stats"):
                    cache_stats = cache.get_stats()
                    cache_entries = cache_stats.get("size", 0)
                    hits = cache_stats.get("hits", 0)
                    misses = cache_stats.get("misses", 0)
                    total = hits + misses
                    if total > 0:
                        cache_hit_rate = f"{(hits / total) * 100:.1f}%"

            rows.append(
                {
                    "module_id": str(module_id),
                    "init_time": f"{float(module_stats.get('init_time', 0)):.3f}s",
                    "init_count": str(int(module_stats.get("init_count", 0))),
                    "last_init_time": str(int(module_stats.get("last_init_time", 0))),
                    "cache_entries": str(cache_entries),
                    "cache_hit_rate": cache_hit_rate,
                }
            )

        ui.table(columns=columns, rows=rows, row_key="module_id").classes("w-full")

    def _render_memory_section(self) -> None:
        """Render memory usage section."""
        with ui.card().classes("w-full p-4 mb-6"):
            ui.label("内存使用情况").classes("text-xl font-semibold mb-4")

            with ui.row().classes("w-full"):
                # System memory
                self._render_system_memory_stats()

                # Cache details
                self._render_module_cache_details()

    def _render_system_memory_stats(self) -> None:
        """Render system memory statistics."""
        with ui.column().classes("flex-1"):
            ui.label("系统内存").classes("text-subtitle1 mb-2")

            try:
                import psutil

                memory = psutil.virtual_memory()

                ui.linear_progress(value=memory.percent / 100, show_value=True).classes(
                    "w-full mb-2"
                )

                with ui.column().classes("text-sm space-y-1"):
                    ui.label(f"总计: {memory.total // (1024**3):.1f} GB")
                    ui.label(f"已用: {memory.used // (1024**3):.1f} GB")
                    ui.label(f"可用: {memory.available // (1024**3):.1f} GB")

            except ImportError:
                ui.label("psutil 不可用").classes("text-warning text-sm")

    def _render_module_cache_details(self) -> None:
        """Render module cache details."""
        with ui.column().classes("flex-1"):
            ui.label("模块缓存详情").classes("text-subtitle1 mb-2")

            cache_data = []
            for name, cache in self.storage_manager._cached_storages.items():
                if hasattr(cache, "get_stats"):
                    stats = cache.get_stats()
                    hit_rate = stats.get("hit_rate", 0)

                    cache_data.append(
                        {
                            "module": name.replace("module_", "", 1),
                            "entries": stats.get("size", 0),
                            "hits": stats.get("hits", 0),
                            "misses": stats.get("misses", 0),
                            "hit_rate": f"{hit_rate:.1%}",
                        }
                    )

            if cache_data:
                for item in cache_data:
                    with ui.card().classes("p-2 mb-2"):
                        ui.label(f"模块: {item['module']}").classes("font-semibold")
                        with ui.row().classes("text-sm space-x-4"):
                            ui.label(f"条目: {item['entries']}")
                            ui.label(f"命中: {item['hits']}")
                            ui.label(f"未命中: {item['misses']}")
                            ui.label(f"命中率: {item['hit_rate']}")
            else:
                ui.label("暂无缓存数据").classes("text-grey text-sm")

    def _render_actions_section(self) -> None:
        """Render memory management actions."""
        with ui.card().classes("w-full p-4"):
            ui.label("内存管理").classes("text-xl font-semibold mb-4")

            with ui.row().classes("gap-4"):
                ui.button("清空所有缓存", on_click=self._clear_all_caches)
                ui.button("强制垃圾回收", on_click=self._force_gc)
                ui.button(
                    "刷新统计", on_click=lambda: ui.run_javascript("location.reload()")
                )

    def _clear_all_caches(self) -> None:
        """Clear all caches."""
        self.storage_manager.clear_all()
        ui.notify("所有缓存已清空")

    def _force_gc(self) -> None:
        """Force garbage collection."""
        import gc

        gc.collect()
        ui.notify("垃圾回收完成")


def render_stats_dashboard() -> None:
    """Render unified statistics dashboard."""
    dashboard = StatsDashboardUI()
    dashboard.render_dashboard()


class AutoRefreshStatsDashboard:
    """Auto-refreshing unified dashboard component."""

    def __init__(self, refresh_interval: int = 30):
        self.refresh_interval = refresh_interval
        self.dashboard = StatsDashboardUI()

    def render(self) -> None:
        """Render auto-refreshing dashboard."""
        with ui.card().classes("w-full"):
            ui.label("实时统计监控").classes("text-h6")

            content_container = ui.column()

            def update_dashboard():
                content_container.clear()
                with content_container:
                    self.dashboard._render_summary_cards()

            # Initial render
            update_dashboard()

            # Set up auto-refresh
            ui.timer(self.refresh_interval, update_dashboard)

            ui.label(f"每 {self.refresh_interval} 秒自动刷新").classes(
                "text-caption text-grey"
            )
