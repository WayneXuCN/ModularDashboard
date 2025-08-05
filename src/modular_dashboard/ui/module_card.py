"""Module card component for displaying individual modules."""

from nicegui import ui

from ..utils.lazy_module import module_cache
from .styles import DashboardStyles


class ModuleCard:
    """Individual module card component with lazy loading."""

    def __init__(self, module_id: str, module_config, module_class):
        self.module_id = module_id
        self.module_config = module_config
        self.module_class = module_class

    def render(self) -> None:
        """Render the module card with lazy loading."""
        # Use lazy module wrapper to delay instantiation
        lazy_module = module_cache.get_or_create(
            self.module_id, self.module_class, self.module_config.config
        )

        with ui.card().classes(f"w-full h-full {DashboardStyles.MODULE_CARD}"):
            self._render_header(lazy_module)
            self._render_content(lazy_module)

    def _render_header(self, lazy_module) -> None:
        """Render the module card header."""
        with ui.row().classes(
            f"w-full justify-between items-center {DashboardStyles.PADDING_MD} {DashboardStyles.PADDING_SM}"
        ):
            # Module title
            title_label = ui.label(lazy_module.name).classes(
                f"{DashboardStyles.TITLE_H3} cursor-pointer {DashboardStyles.HOVER_SCALE}"
            )
            title_label.on(
                "click",
                lambda e, mid=self.module_id: ui.navigate.to(f"/module/{mid}"),
            )

            # Module icon
            icon_element = ui.icon(lazy_module.icon).classes(
                f"text-xl cursor-pointer text-indigo-500 {DashboardStyles.HOVER_SCALE}"
            )
            icon_element.on(
                "click",
                lambda e, mid=self.module_id: ui.navigate.to(f"/module/{mid}"),
            )

    def _render_content(self, lazy_module) -> None:
        """Render the module card content with lazy initialization."""
        # NiceGUI separator
        ui.separator().classes("my-2")

        # Module content container
        with ui.column().classes("p-2"):
            lazy_module.render()
