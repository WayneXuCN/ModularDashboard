"""Dashboard UI components with optimized design."""

from nicegui import ui

from ..config.schema import AppConfig
from ..modules.registry import MODULE_REGISTRY


def render_module_detail(module_id: str, config: AppConfig):
    """Render a module's detailed view with elegant design."""
    module_class = MODULE_REGISTRY.get(module_id)
    if not module_class:
        with (
            ui.column()
            .classes("w-full items-center")
            .style(
                "padding: 4rem 2rem; min-height: 100vh; "
                "background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.7) 100%);"
            )
        ):
            # Error state
            ui.label(f"Module {module_id} not found").classes(
                "text-3xl font-light"
            ).style("color: #475569; margin-bottom: 2rem; letter-spacing: -0.02em;")
            ui.button(
                "← Back to Dashboard", on_click=lambda: ui.navigate.to("/")
            ).classes(
                "px-6 py-3 text-sm font-medium transition-all duration-300"
            ).style(
                "background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); "
                "border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; "
                "color: #475569; box-shadow: 0 4px 16px rgba(0,0,0,0.08); "
                "hover:transform: translateY(-2px); hover:box-shadow: 0 8px 24px rgba(0,0,0,0.12);"
            ).props("flat")
        return

    module = module_class()

    # Main container with refined background
    with (
        ui.column()
        .classes("w-full")
        .style(
            "min-height: 100vh; "
            "background: linear-gradient(135deg, rgba(248,250,252,0.9) 0%, rgba(241,245,249,0.7) 100%);"
        )
    ):
        # Header
        with (
            ui.row()
            .classes("w-full items-center")
            .style("padding: 2rem 3rem 1rem 3rem; max-width: 1200px; margin: 0 auto;")
        ):
            ui.button(
                "← Back to Dashboard", on_click=lambda: ui.navigate.to("/")
            ).classes(
                "px-5 py-2.5 text-sm font-medium transition-all duration-300"
            ).style(
                "background: rgba(255,255,255,0.9); backdrop-filter: blur(12px); "
                "border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; "
                "color: #475569; box-shadow: 0 2px 12px rgba(0,0,0,0.06); "
                "hover:background: rgba(255,255,255,0.95); "
                "hover:transform: translateY(-1px); hover:box-shadow: 0 4px 16px rgba(0,0,0,0.1);"
            ).props("flat")

            # Module title with icon
            with (
                ui.row().classes("items-center").style("margin-left: 2rem; gap: 1rem;")
            ):
                ui.icon(module.icon).classes("text-3xl").style("color: #6366f1;")
                ui.label(module.name).classes("text-3xl font-light").style(
                    "color: #1e293b; letter-spacing: -0.025em; font-weight: 300;"
                )

        # Content area with glass morphism card
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
            # Render module details
            module.render_detail()


def render_dashboard(config: AppConfig) -> None:
    """Render the main dashboard UI."""
    with (
        ui.column()
        .classes("w-full items-center")
        .style(
            "padding: 3rem 2rem; "
            "background: linear-gradient(135deg, rgba(248,250,252,0.8) 0%, rgba(241,245,249,0.6) 100%); "
            "min-height: 100vh;"
        )
    ):
        # Header with title and controls
        with (
            ui.row()
            .classes("w-full max-w-7xl justify-between items-center")
            .style("margin-bottom: 3.5rem; padding: 0 1rem;")
        ):
            ####################
            ### Main Title
            ####################
            ui.label("Research Dashboard").classes(
                "text-4xl font-light tracking-wide"
            ).style(
                "background: linear-gradient(135deg, #1e293b 0%, #475569 100%); "
                "-webkit-background-clip: text; -webkit-text-fill-color: transparent; "
                "letter-spacing: -0.025em; font-weight: 300;"
            )

            with ui.row().classes("items-center").style("gap: 1.5rem;"):
                ####################
                ### Refresh button
                ####################
                ui.button(
                    "Refresh All",
                    on_click=lambda: ui.notify(
                        "Refreshing all modules...", type="positive"
                    ),
                ).classes(
                    "px-6 py-2.5 text-sm font-medium transition-all duration-300"
                ).style(
                    "background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); "
                    "border: 1px solid rgba(148,163,184,0.2); border-radius: 12px; "
                    "color: #475569; box-shadow: 0 2px 8px rgba(0,0,0,0.04); "
                    "hover:background: rgba(255,255,255,0.95); hover:transform: translateY(-1px); "
                    "hover:box-shadow: 0 4px 16px rgba(0,0,0,0.08);"
                ).props("flat")

                ####################
                ### Theme toggle
                ####################
                options = {"Light": "light", "Dark": "dark"}
                initial_key = "Light" if config.theme == "light" else "Dark"
                theme_toggle = (
                    ui.toggle(options, value=initial_key)
                    .classes("transition-all duration-300")
                    .style(
                        "background: rgba(255,255,255,0.8); backdrop-filter: blur(12px); "
                        "border: 1px solid rgba(148,163,184,0.15); border-radius: 14px; "
                        "padding: 0.25rem; box-shadow: 0 2px 12px rgba(0,0,0,0.05);"
                    )
                )

                def on_theme_change(e):
                    config.theme = e.value
                    if e.value == "dark":
                        ui.dark_mode().enable()
                    else:
                        ui.dark_mode().disable()

                theme_toggle.on("change", on_theme_change)

        # Module cards grid
        with ui.element("div").classes(
            "grid w-full max-w-7xl transition-all duration-500 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 px-4"
        ):
            for module_config in sorted(config.modules, key=lambda m: m.position):
                if module_config.enabled and module_config.id in MODULE_REGISTRY:
                    module_class = MODULE_REGISTRY[module_config.id]
                    module = module_class()

                    with (
                        ui.card()
                        .classes(
                            "w-full sm:w-auto cursor-pointer group transition-all duration-300 flex flex-col"
                        )
                        .style(
                            "background: rgba(255,255,255,0.85); backdrop-filter: blur(16px); "
                            "border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; "
                            "box-shadow: 0 8px 32px rgba(0,0,0,0.06); padding: 1.75rem; "
                            "hover:background: rgba(255,255,255,0.92); "
                            "hover:transform: translateY(-4px) scale(1.02); "
                            "hover:box-shadow: 0 16px 48px rgba(0,0,0,0.12); "
                            "hover:border-color: rgba(99,102,241,0.2);"
                        )
                    ):
                        # Header with module name and icon
                        with (
                            ui.row()
                            .classes("w-full justify-between items-start")
                            .style("margin-bottom: 1.25rem;")
                        ):
                            label = (
                                ui.label(module.name)
                                .classes(
                                    "text-xl font-medium leading-tight cursor-pointer"
                                )
                                .style(
                                    "color: #1e293b; letter-spacing: -0.015em; "
                                    "transition: color 0.3s ease;"
                                )
                            )
                            label.on(
                                "click",
                                lambda e, mid=module_config.id: ui.navigate.to(
                                    f"/module/{mid}"
                                ),
                            )
                            icon = (
                                ui.icon(module.icon)
                                .classes(
                                    "text-2xl transition-all duration-300 cursor-pointer"
                                )
                                .style(
                                    "color: #64748b; group-hover:color: #6366f1; "
                                    "group-hover:transform: scale(1.1);"
                                )
                            )
                            icon.on(
                                "click",
                                lambda e, mid=module_config.id: ui.navigate.to(
                                    f"/module/{mid}"
                                ),
                            )

                        # Subtle separator with gradient
                        ui.element("div").style(
                            "width: 100%; height: 1px; margin: 1rem 0; "
                            "background: linear-gradient(90deg, "
                            "rgba(148,163,184,0.3) 0%, rgba(148,163,184,0.1) 50%, rgba(148,163,184,0.3) 100%);"
                        )

                        # Module content container
                        with ui.element("div").style("margin: 1.25rem 0;"):
                            module.render()

        # Add floating action button for global actions (with menu)
        with ui.element("div").classes("fixed bottom-8 right-8 z-50"):

            def show_fab_menu():
                with ui.dialog() as dialog, ui.column().classes("gap-4 p-4"):
                    ui.label("请选择操作").classes("text-lg font-medium mb-2")
                    ui.button(
                        "新建便笺",
                        on_click=lambda: ui.notify(
                            "新建便笺功能暂未实现", type="info"
                        ),
                    ).classes("w-full")
                    ui.button(
                        "导入新模块",
                        on_click=lambda: ui.notify(
                            "导入新模块功能暂未实现", type="info"
                        ),
                    ).classes("w-full")
                dialog.open()

            ui.button(
                icon="add",
                on_click=show_fab_menu,
            ).classes("w-14 h-14 transition-all duration-300").style(
                "background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); "
                "border-radius: 50%; border: none; color: white; "
                "box-shadow: 0 8px 24px rgba(99,102,241,0.3); "
                "hover:transform: scale(1.05) translateY(-2px); "
                "hover:box-shadow: 0 12px 32px rgba(99,102,241,0.4);"
            ).props("fab")
