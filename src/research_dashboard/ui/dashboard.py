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

    # Find the module configuration
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


def _get_max_width_class(width_setting: str) -> str:
    """Get the max-width class based on width setting."""
    width_map = {
        "narrow": "max-w-4xl",  # ~1000px
        "default": "max-w-6xl",  # ~1100px
        "wide": "max-w-7xl"     # ~1600px
    }
    return width_map.get(width_setting, "max-w-6xl")


def _get_column_width_class(column_width: str) -> str:
    """Get the column width class based on column width setting."""
    if column_width == "narrow":
        return "md:w-1/4 lg:w-1/5"
    return "md:w-2/4 lg:w-3/5"


def render_dashboard(config: AppConfig) -> None:
    """Render the main dashboard UI with column-based layout."""
    # Determine max width class based on config
    max_width_class = _get_max_width_class(config.layout.width)
    
    # Determine if we should center content vertically
    center_class = "items-center justify-center" if config.layout.center_content else "items-center"
    
    # Determine padding based on navigation visibility
    padding_style = "padding: 1rem 2rem;" if config.layout.show_nav else "padding: 3rem 2rem;"
    
    with (
        ui.column()
        .classes(f"w-full {center_class}")
        .style(
            f"{padding_style} "
            "background: linear-gradient(135deg, rgba(248,250,252,0.8) 0%, rgba(241,245,249,0.6) 100%); "
            "min-height: 100vh;"
        )
    ):
        # Header with title and controls (only if show_nav is True)
        if config.layout.show_nav:
            with (
                ui.row()
                .classes(f"w-full {max_width_class} justify-between items-center")
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
                        icon="refresh",
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

        # Main content area with multi-column layout
        with ui.row().classes(f"w-full {max_width_class}"):
            # Create columns based on config
            column_classes = "flex flex-col gap-6 h-full"
            if config.layout.center_content:
                column_classes += " items-center"
                
            # Render each column based on configuration
            # Ensure we have the right number of columns
            column_configs = config.layout.column_config[:config.layout.columns] if config.layout.column_config else []
            
            # Fill in any missing columns with default configuration
            while len(column_configs) < config.layout.columns:
                column_configs.append({"width": "normal", "modules": []})
            
            for i, column_config in enumerate(column_configs):
                # Handle both dict and object representations of column_config
                if isinstance(column_config, dict):
                    column_width = column_config.get("width", "normal")
                    module_ids = column_config.get("modules", [])
                else:
                    column_width = getattr(column_config, "width", "normal")
                    module_ids = getattr(column_config, "modules", [])
                
                column_width_class = _get_column_width_class(column_width)
                
                with ui.column().classes(f"w-full {column_width_class} gap-6"):
                    # Render modules in this column based on their order in module_ids
                    for position, module_id in enumerate(module_ids):
                        # Find the module configuration
                        module_config = next((m for m in config.modules if m.id == module_id), None)
                        
                        # Skip if module is not found or not enabled
                        if not module_config or not module_config.enabled or module_id not in MODULE_REGISTRY:
                            continue
                            
                        module_class = MODULE_REGISTRY[module_id]
                        # Pass the module-specific configuration to the module instance
                        module = module_class(module_config.config)

                        with (
                            ui.card()
                            .classes(
                                "w-full cursor-pointer group transition-all duration-300 flex flex-col"
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
                                    lambda e, mid=module_id: ui.navigate.to(
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
                                    lambda e, mid=module_id: ui.navigate.to(
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
                        on_click=lambda: ui.notify("新建便笺功能暂未实现", type="info"),
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
