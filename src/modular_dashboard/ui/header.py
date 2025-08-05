"""Header navigation component for the dashboard."""

from nicegui import ui

from ..config.manager import save_config
from ..config.schema import AppConfig
from .styles import DashboardStyles, DesignSystem


class HeaderNavigation:
    """Header navigation component with theme toggle and refresh button."""

    def __init__(self, config: AppConfig):
        self.config = config

    def render(self) -> None:
        """Render the header navigation."""
        with (
            ui.card().classes(f"w-full {DashboardStyles.HEADER}"),
            ui.row().classes(
                f"w-full justify-between items-center {DashboardStyles.PADDING_MD} {DashboardStyles.CONTAINER_CENTER}"
            ),
        ):
            # Title with unified styling
            ui.label("Modular Dashboard").classes(DashboardStyles.TITLE_H1)

            # Controls container
            with ui.row().classes(DashboardStyles.GAP_MD):
                self._render_stats_button()
                self._render_refresh_button()
                self._render_theme_toggle()

    def _render_refresh_button(self) -> None:
        """Render the refresh button."""
        ui.button(
            icon="refresh",
            on_click=lambda: ui.notify("Refreshing all modules...", type="positive"),
        ).classes(DashboardStyles.BUTTON_SECONDARY).props("flat")

    def _render_stats_button(self) -> None:
        """Render the statistics page button."""
        ui.button(
            icon="analytics",
            on_click=lambda: ui.navigate.to("/stats"),
        ).classes(DashboardStyles.BUTTON_SECONDARY).props("flat")

    def _render_theme_toggle(self) -> None:
        """Render the theme toggle."""
        options = {"Light": "light", "Dark": "dark"}
        initial_key = "Light" if self.config.theme == "light" else "Dark"
        theme_toggle = ui.toggle(options, value=initial_key).classes(
            f"{DashboardStyles.GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_MD} "
            f"{DesignSystem.SHADOW_SM} transition-all duration-300"
        )

        def on_theme_change(e):
            self.config.theme = e.value
            save_config(self.config)  # Save the configuration to file
            if e.value == "dark":
                ui.dark_mode().enable()
            else:
                ui.dark_mode().disable()

        theme_toggle.on("change", on_theme_change)
