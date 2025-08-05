"""Floating action button component for dashboard."""

from nicegui import ui

from .styles import DashboardStyles


class FloatingActionButton:
    """Floating action button component with menu."""

    def render(self) -> None:
        """Render the floating action button."""
        with ui.column().classes("fixed bottom-4 right-4 z-50"):
            self._render_fab_button()

    def _render_fab_button(self) -> None:
        """Render the FAB button with menu."""

        def show_fab_menu():
            with (
                ui.dialog() as dialog,
                ui.column().classes("gap-4 p-4 bg-white rounded-lg shadow-xl"),
            ):
                ui.label("请选择操作").classes(
                    "text-lg font-medium mb-2 text-slate-800"
                )
                ui.button(
                    "新建便笺",
                    on_click=lambda: ui.notify("新建便笺功能暂未实现", type="info"),
                ).classes(f"w-full justify-start {DashboardStyles.BUTTON_SECONDARY}")
                ui.button(
                    "导入新模块",
                    on_click=lambda: ui.notify("导入新模块功能暂未实现", type="info"),
                ).classes(f"w-full justify-start {DashboardStyles.BUTTON_SECONDARY}")
            dialog.open()

        ui.button(
            icon="add",
            on_click=show_fab_menu,
        ).classes(f"{DashboardStyles.FAB} {DashboardStyles.HOVER_SCALE}").props("fab")
