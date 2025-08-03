"""Header navigation component for the dashboard."""

from nicegui import ui

from ..config.schema import AppConfig


class HeaderNavigation:
    """Header navigation component with theme toggle and refresh button."""

    def __init__(self, config: AppConfig):
        self.config = config

    def render(self) -> None:
        """Render the header navigation."""
        with (
            ui.card().classes(
                "w-full border-0 shadow-sm bg-white/80 backdrop-blur-sm"
            ),
            ui.row().classes(
                "w-full justify-between items-center p-4 max-w-7xl mx-auto"
            )
        ):
                # Title with gradient styling
                ui.label("Research Dashboard").classes(
                    "text-3xl font-light bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent"
                )

                # Controls container
                with ui.row().classes("gap-3"):
                    self._render_refresh_button()
                    self._render_theme_toggle()

    def _render_refresh_button(self) -> None:
        """Render the refresh button."""
        ui.button(
            icon="refresh",
            on_click=lambda: ui.notify("Refreshing all modules...", type="positive"),
        ).classes(
            "bg-white/90 backdrop-blur-sm border border-slate-200/50 rounded-lg "
            "text-slate-600 shadow-sm hover:bg-white hover:shadow-md "
            "transition-all duration-300 hover:scale-105"
        ).props("flat")

    def _render_theme_toggle(self) -> None:
        """Render the theme toggle."""
        options = {"Light": "light", "Dark": "dark"}
        initial_key = "Light" if self.config.theme == "light" else "Dark"
        theme_toggle = ui.toggle(options, value=initial_key).classes(
            "bg-white/80 backdrop-blur-sm border border-slate-200/50 rounded-lg "
            "shadow-sm transition-all duration-300"
        )

        def on_theme_change(e):
            self.config.theme = e.value
            if e.value == "dark":
                ui.dark_mode().enable()
            else:
                ui.dark_mode().disable()

        theme_toggle.on("change", on_theme_change)
