"""Dashboard UI components."""

from nicegui import app, ui

from ..config.schema import AppConfig
from ..modules.registry import MODULE_REGISTRY


def render_module_detail(module_id: str, config: AppConfig):
    """Render a module's detailed view."""
    module_class = MODULE_REGISTRY.get(module_id)
    if not module_class:
        with ui.column().classes("w-full items-center p-4"):
            ui.label(f"Module {module_id} not found").classes("text-2xl")
            ui.button("← Back to Dashboard", on_click=lambda: ui.open("/")).props(
                "outline"
            )
        return

    module = module_class()

    # Header with back button
    with ui.row().classes("w-full items-center mb-4 p-4"):
        ui.button("← Back to Dashboard", on_click=lambda: ui.open("/")).props("outline")
        ui.label(module.name).classes("text-2xl font-bold ml-4")

    # Render module details
    module.render_detail()


def render_dashboard(config: AppConfig) -> None:
    """Render the main dashboard UI."""
    # Set dark mode based on config
    app.add_media_files("/static", "src/research_dashboard/static")

    with ui.column().classes("w-full items-center p-4"):
        # Header with title and controls
        with ui.row().classes("w-full justify-between items-center mb-6"):
            ui.label("Research Dashboard").classes("text-3xl font-bold")

            with ui.row().classes("items-center gap-4"):
                # Refresh button
                ui.button(
                    "Refresh All",
                    on_click=lambda: ui.notify("Refreshing all modules..."),
                ).props("outline")

                # Theme toggle
                options = {"Light": "light", "Dark": "dark"}
                initial_key = "Light" if config.theme == "light" else "Dark"
                theme_toggle = ui.toggle(options, value=initial_key).classes("mr-2")

                def on_theme_change(e):
                    config.theme = e.value
                    if e.value == "dark":
                        ui.dark_mode().enable()
                    else:
                        ui.dark_mode().disable()

                theme_toggle.on("change", on_theme_change)

                # Column count selector
                column_options = {str(i): i for i in range(1, 5)}
                # Ensure the value is a string key, not the integer value
                initial_column_key = str(config.layout.columns)
                column_selector = ui.select(
                    column_options, value=initial_column_key, label="Columns"
                )
                column_selector.on(
                    "update:model-value",
                    lambda e: setattr(config.layout, "columns", int(e.value)),
                )

        # Module cards grid
        with ui.grid(columns=config.layout.columns).classes("w-full gap-4") as grid:
            grid.bind_visibility_from(column_selector, "value")

            for module_config in sorted(config.modules, key=lambda m: m.position):
                if module_config.enabled and module_config.id in MODULE_REGISTRY:
                    module_class = MODULE_REGISTRY[module_config.id]
                    module = module_class()

                    # Create a card with separate click areas
                    with ui.card().classes("w-full card-hover"):
                        # Make the whole card clickable for navigation to detail page
                        ui.on(
                            "click",
                            lambda module_id=module_config.id: ui.open(
                                f"/module/{module_id}"
                            ),
                        )

                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label(module.name).classes("text-lg font-bold")
                            ui.icon(module.icon).classes("text-2xl")

                        # Add a separator
                        ui.separator()

                        # Render module content
                        module.render()

                        # Add module footer with refresh button
                        with ui.row().classes("w-full justify-end mt-2"):
                            ui.button(
                                "Refresh",
                                on_click=lambda m=module: ui.notify(
                                    f"Refreshing {m.name}"
                                ),
                            ).props("flat small")


# Register the detail pages for each module
@app.get("/module/{module_id}")
def module_detail_page(module_id: str):
    """Create a page for the module detail view."""
    with ui.column().classes("w-full p-4"):
        # Load config for this page
        from ..config.manager import load_config

        config = load_config()
        render_module_detail(module_id, config)
