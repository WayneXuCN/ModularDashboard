"""Dashboard UI components with optimized design."""

from nicegui import ui

from ..config.schema import AppConfig
from ..modules.registry import MODULE_REGISTRY
from .fab import FloatingActionButton
from .header import HeaderNavigation
from .layout import DashboardLayout


def render_module_detail(module_id: str, config: AppConfig):
    """Render a module's detailed view with elegant design."""
    # Check if module exists
    module_class = MODULE_REGISTRY.get(module_id)
    if not module_class:
        _render_module_not_found(module_id)
        return

    # Get module configuration and create instance
    module_config = next((m for m in config.modules if m.id == module_id), None)
    module = module_class(module_config.config) if module_config else module_class()

    # Main container with refined background
    with (
        ui.column()
        .classes("w-full")
        .style(
            "min-height: 100vh; "
            "background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.7) 100%);"
        )
    ):
        # Header with back button and module title
        _render_detail_header(module)

        # Content area with glass morphism card
        _render_detail_content(module)


def _render_module_not_found(module_id: str) -> None:
    """Render error state for missing module."""
    with (
        ui.column()
        .classes("w-full items-center")
        .style(
            "padding: 4rem 2rem; min-height: 100vh; "
            "background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.7) 100%);"
        )
    ):
        ui.label(f"Module {module_id} not found").classes("text-3xl font-light").style(
            "color: #475569; margin-bottom: 2rem; letter-spacing: -0.02em;"
        )

        ui.button("← Back to Dashboard", on_click=lambda: ui.navigate.to("/")).classes(
            "px-6 py-3 text-sm font-medium transition-all duration-300"
        ).style(
            "background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); "
            "border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; "
            "color: #475569; box-shadow: 0 4px 16px rgba(0,0,0,0.08); "
            "hover:transform: translateY(-2px); hover:box-shadow: 0 8px 24px rgba(0,0,0,0.12);"
        ).props("flat")


def _render_detail_header(module) -> None:
    """Render the detail page header."""
    with (
        ui.row()
        .classes("w-full items-center")
        .style("padding: 2rem 3rem 1rem 3rem; max-width: 1200px; margin: 0 auto;")
    ):
        # Back button
        ui.button("← Back to Dashboard", on_click=lambda: ui.navigate.to("/")).classes(
            "px-5 py-2.5 text-sm font-medium transition-all duration-300"
        ).style(
            "background: rgba(255,255,255,0.9); backdrop-filter: blur(12px); "
            "border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; "
            "color: #475569; box-shadow: 0 2px 12px rgba(0,0,0,0.06); "
            "hover:background: rgba(255,255,255,0.95); "
            "hover:transform: translateY(-1px); hover:box-shadow: 0 4px 16px rgba(0,0,0,0.1);"
        ).props("flat")

        # Module title with icon
        with ui.row().classes("items-center").style("margin-left: 2rem; gap: 1rem;"):
            ui.icon(module.icon).classes("text-3xl").style("color: #6366f1;")
            ui.label(module.name).classes("text-3xl font-light").style(
                "color: #1e293b; letter-spacing: -0.025em; font-weight: 300;"
            )


def _render_detail_content(module) -> None:
    """Render the content area with module details."""
    with (
        ui.column()
        .classes("w-full items-center")
        .style("padding: 2rem 3rem; max-width: 1200px; margin: 0 auto;"),
        ui.card()
        .classes("w-full")
        .style(
            "background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); "
            "border: 1px solid rgba(255,255,255,0.3); border-radius: 24px; "
            "box-shadow: 0 12px 40px rgba(0,0,0,0.08); padding: 3rem;"
        ),
    ):
        module.render_detail()


def render_dashboard(config: AppConfig) -> None:
    """Render the main dashboard UI with proper NiceGUI layout."""
    # Main container with full viewport height and background
    with ui.column().classes(
        "min-h-screen bg-gradient-to-br from-slate-50 to-slate-100"
    ):
        # Header section
        if config.layout.show_nav:
            header = HeaderNavigation(config)
            header.render()

        # Main content area
        layout = DashboardLayout(config)
        layout.render()

        # Floating action button
        fab = FloatingActionButton()
        fab.render()
