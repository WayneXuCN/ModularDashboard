"""Module registry."""

from .arxiv.module import ArxivModule
from .base import Module
from .clock.module import ClockModule
from .github.module import GithubModule
from .monitor.module import MonitorModule
from .releases.module import ReleasesModule
from .rss.module import RssModule
from .todo.module import TodoModule
from .weather.module import WeatherModule

# Registry of all available modules
MODULE_REGISTRY = {
    "arxiv": ArxivModule,
    "clock": ClockModule,
    "github": GithubModule,
    "monitor": MonitorModule,
    "releases": ReleasesModule,
    "rss": RssModule,
    "todo": TodoModule,
    "weather": WeatherModule,
}

def get_module_class(module_id: str) -> type[Module] | None:
    """Get module class by ID. Returns None if not found."""
    return MODULE_REGISTRY.get(module_id)
