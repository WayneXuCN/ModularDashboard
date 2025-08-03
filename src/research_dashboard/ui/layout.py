"""Layout component for rendering dashboard columns and modules."""

from nicegui import ui

from ..config.schema import AppConfig
from ..modules.registry import MODULE_REGISTRY
from .module_card import ModuleCard


class DashboardLayout:
    """Dashboard layout component for rendering columns and modules."""

    def __init__(self, config: AppConfig):
        self.config = config

    def render(self) -> None:
        """Render the main dashboard layout."""
        with ui.column().classes("flex-1 p-4 md:p-6"):
            column_configs = self._get_column_configs()

            # Render layout based on width setting
            if self.config.layout.width == "slim":
                self._render_slim_layout(column_configs)
            else:
                self._render_default_layout(column_configs)

    def _get_column_configs(self):
        """Get column configurations."""
        column_configs = (
            self.config.layout.column_config[: self.config.layout.columns]
            if self.config.layout.column_config
            else []
        )

        # Fill in any missing columns with default configuration
        while len(column_configs) < self.config.layout.columns:
            column_configs.append({"width": "normal", "modules": []})

        return column_configs

    def _render_slim_layout(self, column_configs) -> None:
        """Render slim layout (centered with limited width)."""
        with (
            ui.column().classes("w-full items-center"),
            ui.column().classes("max-w-6xl w-full")
        ):
                if self.config.layout.columns == 3:
                    self._render_three_column_layout(column_configs)
                else:
                    self._render_one_or_two_column_layout(column_configs)

    def _render_default_layout(self, column_configs) -> None:
        """Render default/wide layout (full width)."""
        width_class = (
            "w-full px-6" if self.config.layout.width == "default" else "w-full px-8"
        )
        with ui.column().classes(f"{width_class}"):
            if self.config.layout.columns == 3:
                self._render_three_column_layout(column_configs)
            else:
                self._render_one_or_two_column_layout(column_configs)

    def _render_three_column_layout(self, column_configs) -> None:
        """Render three column layout."""
        with ui.row().classes("w-full gap-4 md:gap-6 flex-wrap"):
            for column_config in column_configs:
                with ui.column().classes(
                    "w-full sm:w-1/2 md:w-1/3 lg:w-1/3 mb-4"
                ):
                    self._render_column_content(column_config)

    def _render_one_or_two_column_layout(self, column_configs) -> None:
        """Render one or two column layout."""
        with ui.row().classes("w-full gap-4 md:gap-6 flex-wrap"):
            for column_config in column_configs:
                col_class = (
                    "w-full"
                    if self.config.layout.columns == 1
                    else "w-full sm:w-1/2"
                )
                with ui.column().classes(f"{col_class} mb-4"):
                    self._render_column_content(column_config)

    def _render_column_content(self, column_config) -> None:
        """Render content for a single column."""
        # Handle both dict and object representations of column_config
        if isinstance(column_config, dict):
            module_ids = column_config.get("modules", [])
        else:
            module_ids = getattr(column_config, "modules", [])

        # Render modules in this column based on their order in module_ids
        for module_id in module_ids:
            # Find the module configuration
            module_config = next((m for m in self.config.modules if m.id == module_id), None)

            # Skip if module is not found or not enabled
            if (
                not module_config
                or not module_config.enabled
                or module_id not in MODULE_REGISTRY
            ):
                continue

            module_class = MODULE_REGISTRY[module_id]
            module_card = ModuleCard(module_id, module_config, module_class)
            module_card.render()
