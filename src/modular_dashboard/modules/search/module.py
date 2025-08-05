"""Search module implementation as a standalone module."""

from typing import Any

from ...ui.search import BangConfig, SearchConfig, UISearchModule
from ..base import Module


class SearchModule(Module):
    """Search module with support for multiple search engines and bangs functionality."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the search module with configuration."""
        # Convert config dict to SearchConfig dataclass
        bangs = [BangConfig(**bang) for bang in config.get("bangs", [])]
        self.search_config = SearchConfig(
            search_engine=config.get("search_engine", "duckduckgo"),
            new_tab=config.get("new_tab", False),
            autofocus=config.get("autofocus", False),
            target=config.get("target", "_blank"),
            placeholder=config.get("placeholder", "Type here to search…"),
            bangs=bangs,
        )
        self.ui_module = UISearchModule(self.search_config)

    @property
    def id(self) -> str:
        """Get module ID."""
        return "search"

    @property
    def name(self) -> str:
        """Get module name."""
        return "Search"

    @property
    def icon(self) -> str:
        """Get module icon."""
        return "search"

    @property
    def description(self) -> str:
        """Get module description."""
        return "Universal search module with support for multiple search engines and custom bangs"

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch method for search module (not used for search functionality)."""
        # Search module doesn't fetch data in the traditional sense
        # It's a UI module that allows users to search
        return []

    def render(self) -> None:
        """Render the search module UI."""
        self.ui_module.render()

    def render_detail(self) -> None:
        """Render the search module detail view."""
        self.ui_module.render()
