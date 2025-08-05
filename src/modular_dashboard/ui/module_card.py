"""Module card component for displaying individual modules."""

from nicegui import ui

from ..utils.lazy_module import module_cache


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

        with ui.card().classes(
            "w-full h-full cursor-pointer transition-all duration-300 "
            "hover:shadow-lg hover:scale-[1.02] bg-white/80 backdrop-blur-sm "
            "border border-white/50"
        ):
            self._render_header(lazy_module)
            self._render_content(lazy_module)

    def _render_header(self, lazy_module) -> None:
        """Render the module card header."""
        with ui.row().classes("w-full justify-between items-center p-4 pb-2"):
            # Module title
            title_label = ui.label(lazy_module.name).classes(
                "text-lg font-semibold cursor-pointer text-slate-800"
            )
            title_label.on(
                "click",
                lambda e, mid=self.module_id: ui.navigate.to(f"/module/{mid}"),
            )

            # Module icon
            icon_element = ui.icon(lazy_module.icon).classes(
                "text-xl cursor-pointer text-slate-600 hover:text-indigo-600 "
                "transition-all duration-300 hover:scale-110"
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
