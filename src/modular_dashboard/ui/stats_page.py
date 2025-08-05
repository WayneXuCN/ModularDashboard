"""Statistics page UI components for displaying module performance metrics."""

from nicegui import ui


def render_stats_page(stats_collector) -> None:
    """Render the module performance statistics page.

    Args:
        stats_collector: ModuleStatsCollector instance for retrieving statistics
    """
    with ui.column().classes("w-full p-6 max-w-4xl mx-auto"):
        # Header with back button
        with ui.row().classes("w-full items-center mb-6"):
            ui.button(
                "← 返回",
                on_click=lambda: ui.navigate.to("/"),
            ).classes(
                "px-4 py-2 bg-blue-600 text-white rounded-lg "
                "hover:bg-blue-700 transition-colors"
            )
            ui.label("模块性能统计").classes("text-3xl font-bold text-center flex-1")

        # Performance summary
        summary = stats_collector.get_performance_summary()
        with ui.card().classes("w-full p-4 mb-6"):
            ui.label("性能摘要").classes("text-xl font-semibold mb-3")
            ui.label(summary).classes("font-mono text-sm whitespace-pre-line")

        # Detailed statistics
        stats = stats_collector.get_stats()
        if stats.get("modules"):
            with ui.card().classes("w-full p-4 mb-6"):
                ui.label("详细统计").classes("text-xl font-semibold mb-3")

                # Summary cards
                with ui.row().classes("w-full gap-4 mb-4"):
                    with ui.card().classes("p-4 flex-1 text-center"):
                        ui.label(str(stats["total_modules"])).classes(
                            "text-2xl font-bold text-blue-600"
                        )
                        ui.label("总模块数").classes("text-sm text-gray-600")

                    with ui.card().classes("p-4 flex-1 text-center"):
                        ui.label(f"{stats['total_init_time']:.3f}s").classes(
                            "text-2xl font-bold text-green-600"
                        )
                        ui.label("总初始化时间").classes("text-sm text-gray-600")

                    with ui.card().classes("p-4 flex-1 text-center"):
                        ui.label(f"{stats['average_init_time']:.3f}s").classes(
                            "text-2xl font-bold text-purple-600"
                        )
                        ui.label("平均初始化时间").classes("text-sm text-gray-600")

                # Module details table
                ui.label("各模块详情").classes("text-lg font-semibold mb-3")

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
                ]

                rows = []
                for module_id, module_stats in stats["modules"].items():
                    # 确保所有值都是基本类型，避免JSON序列化问题
                    last_init_str = str(int(module_stats.get("last_init_time", 0)))
                    rows.append(
                        {
                            "module_id": str(module_id),
                            "init_time": f"{float(module_stats.get('init_time', 0)):.3f}s",
                            "init_count": str(int(module_stats.get("init_count", 0))),
                            "last_init_time": last_init_str,
                        }
                    )

                ui.table(columns=columns, rows=rows, row_key="module_id").classes(
                    "w-full"
                )

        else:
            with ui.card().classes("w-full p-8 text-center"):
                ui.label("暂无模块加载数据").classes("text-xl text-gray-500")
                ui.label("模块将在首次访问时加载").classes("text-sm text-gray-400 mt-2")
