"""Dashboard UI components with optimized design and consistent styling.

This module provides organized and maintainable dashboard components with centralized
styling and improved code structure using modern Python patterns.
"""

from typing import Any

from nicegui import ui

from ..config.schema import AppConfig
from ..modules.registry import MODULE_REGISTRY
from ..utils.lazy_module import module_cache
from .fab import FloatingActionButton
from .header import HeaderNavigation
from .layout import DashboardLayout
from .styles import DashboardStyles


class ModuleDetailRenderer:
    """Handles module detail page rendering with consistent styling."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def render(self, module_id: str) -> None:
        """Render complete module detail view."""
        module = self._get_module_instance(module_id)
        if not module:
            self._render_not_found(module_id)
            return

        self._render_layout(module)

    def _get_module_instance(self, module_id: str) -> Any | None:
        """Get module instance with lazy loading."""
        module_class = MODULE_REGISTRY.get(module_id)
        if not module_class:
            return None

        module_config = next(
            (m for m in self.config.modules if m.id == module_id), None
        )
        return module_cache.get_or_create(
            module_id, module_class, module_config.config if module_config else {}
        )

    def _render_layout(self, module) -> None:
        """Render main detail layout."""
        with ui.column().classes(f"w-full min-h-screen {DashboardStyles.DETAIL_BG}"):
            self._render_header(module)
            self._render_content(module)

    def _render_header(self, module) -> None:
        """Render module detail header."""
        with ui.row().classes("w-full items-center px-12 py-8 max-w-7xl mx-auto"):
            self._render_back_button()
            self._render_module_title(module)

    def _render_back_button(self) -> None:
        """Render back to dashboard button."""
        ui.button("← Back to Dashboard", on_click=lambda: ui.navigate.to("/")).classes(
            DashboardStyles.BUTTON_PRIMARY
        )

    def _render_module_title(self, module) -> None:
        """Render module title with icon."""
        with ui.row().classes("items-center ml-8 gap-4"):
            ui.icon(module.icon).classes("text-3xl text-indigo-500")
            ui.label(module.name).classes(DashboardStyles.TITLE_H2)

    def _render_content(self, module) -> None:
        """Render module content area."""
        with ui.column().classes("w-full items-center px-12 pb-12 max-w-7xl mx-auto"):  # noqa: SIM117
            with ui.card().classes(DashboardStyles.GLASS_CARD + " p-12 w-full"):
                module.render_detail()

    def _render_not_found(self, module_id: str) -> None:
        """Render module not found state."""
        with ui.column().classes(
            f"w-full items-center justify-center min-h-screen {DashboardStyles.DETAIL_BG}"
        ):
            ui.label(f"Module {module_id} not found").classes(
                DashboardStyles.ERROR_TEXT + " mb-8"
            )
            ui.button(
                "← Back to Dashboard", on_click=lambda: ui.navigate.to("/")
            ).classes(DashboardStyles.BUTTON_PRIMARY)


def render_module_detail(module_id: str, config: AppConfig) -> None:
    """Render a module's detailed view with optimized design."""
    renderer = ModuleDetailRenderer(config)
    renderer.render(module_id)


class DashboardRenderer:
    """Main dashboard renderer with consistent styling."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def render(self) -> None:
        """Render the complete dashboard."""
        ui.add_head_html(
            """
            <style>
                .dashboard-body {
                    min-height: 100vh;
                }
                .dashboard-container {
                    min-height: 100vh;
                }
            </style>
            """
        )
        with ui.column().classes(f"dashboard-container {DashboardStyles.MAIN_BG}"):
            self._render_header()
            self._render_content()
            ui.separator()
            self._render_fab()

    def _render_header(self) -> None:
        """Render dashboard header conditionally."""
        if self.config.layout.show_nav:
            HeaderNavigation(self.config).render()

    def _render_content(self) -> None:
        """Render main dashboard content."""
        DashboardLayout(self.config).render()

    def _render_fab(self) -> None:
        """Render floating action button."""
        FloatingActionButton().render()


def render_dashboard(config: AppConfig) -> None:
    """Render the main dashboard UI with optimized layout."""
    DashboardRenderer(config).render()
