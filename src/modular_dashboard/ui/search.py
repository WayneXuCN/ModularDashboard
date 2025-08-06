"""Search module implementation with support for multiple search engines and bangs functionality."""

from dataclasses import dataclass

from nicegui import ui


@dataclass
class BangConfig:
    """Configuration for a single bang."""

    title: str
    shortcut: str
    url: str


@dataclass
class SearchConfig:
    """Configuration for the search module."""

    search_engine: str = "duckduckgo"
    new_tab: bool = False
    autofocus: bool = False
    target: str = "_blank"
    placeholder: str = "Type here to search…"
    bangs: list[BangConfig] = None

    def __post_init__(self):
        if self.bangs is None:
            self.bangs = []


class UISearchModule:
    """Search module with support for multiple search engines and bangs functionality."""

    # Default search engines
    DEFAULT_ENGINES = {
        "duckduckgo": "https://duckduckgo.com/?q={QUERY}",
        "google": "https://www.google.com/search?q={QUERY}",
        "bing": "https://www.bing.com/search?q={QUERY}",
        "perplexity": "https://www.perplexity.ai/search?q={QUERY}",
        "kagi": "https://kagi.com/search?q={QUERY}",
        "startpage": "https://www.startpage.com/sp/search?query={QUERY}",
    }

    def __init__(self, config: SearchConfig | None = None):
        self.config = config or SearchConfig()
        self.search_input = None
        self.bang_title_label = None

    def render(self) -> None:
        """Render the search module UI."""
        with ui.column().classes("w-full max-w-3xl mx-auto mb-8"):
            with ui.row().classes("w-full items-center gap-2"):
                # Search input
                self.search_input = (
                    ui.input(
                        placeholder=self.config.placeholder,
                        on_change=self._on_input_change,
                    )
                    .classes("flex-1")
                    .on("keydown.enter", self._handle_enter)
                )

                # Bang title display
                self.bang_title_label = ui.label("").classes(
                    "text-sm text-gray-500 mr-2"
                )

                # Search button
                ui.button("Search", on_click=self._perform_search).classes("ml-2")

            # Set autofocus if configured
            if self.config.autofocus:
                self.search_input.run_method("focus")

            # Add keyboard shortcuts
            ui.keyboard(self._handle_key)

    def _on_input_change(self, e) -> None:
        """Handle input changes to detect bangs."""
        query = e.value
        if not query:
            self.bang_title_label.set_text("")
            return

        # Check if query starts with a bang
        for bang in self.config.bangs:
            if query.startswith(bang.shortcut):
                self.bang_title_label.set_text(bang.title)
                return

        # Check if query starts with a default engine
        for name, _ in self.DEFAULT_ENGINES.items():
            if query.startswith(f"!{name}"):
                self.bang_title_label.set_text(name.capitalize())
                return

        self.bang_title_label.set_text("")

    def _handle_key(self, e) -> None:
        """Handle keyboard shortcuts."""
        if (
            e.key == "s"
            and not e.modifiers.ctrl
            and not e.modifiers.alt
            and not e.modifiers.shift
        ):
            self.search_input.run_method("focus")
        elif e.key == "Escape":
            self.search_input.run_method("blur")

    def _handle_enter(self, e) -> None:
        """Handle Enter key press."""
        # Ctrl+Enter logic
        if e.args["ctrlKey"]:
            self._perform_search(new_tab=not self.config.new_tab)
        else:
            self._perform_search(new_tab=self.config.new_tab)

    def _perform_search(self, new_tab: bool | None = None) -> None:
        """Perform the search action."""
        query = self.search_input.value
        if not query:
            return

        # Determine target URL
        target_url = self._get_search_url(query)

        # Determine target
        target = self.config.target
        if new_tab is not None:
            target = "_blank" if new_tab else "_self"

        # Open URL
        ui.run_javascript(f"window.open('{target_url}', '{target}')")

    def _get_search_url(self, query: str) -> str:
        """Get the search URL based on query and configuration."""
        # Check for custom bangs
        for bang in self.config.bangs:
            if query.startswith(bang.shortcut):
                search_term = query[len(bang.shortcut) :].strip()
                return bang.url.replace("{QUERY}", search_term)

        # Check for default engine bangs
        for name, url in self.DEFAULT_ENGINES.items():
            if query.startswith(f"!{name}"):
                search_term = query[len(name) + 1 :].strip()
                return url.replace("{QUERY}", search_term)

        # Use default search engine
        engine_url = self.DEFAULT_ENGINES.get(
            self.config.search_engine, self.config.search_engine
        )
        return engine_url.replace("{QUERY}", query)
