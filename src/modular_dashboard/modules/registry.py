"""Module registry."""

from .animals.module import AnimalsModule
from .arxiv.module import ArxivModule
from .base import Module
from .clock.module import ClockModule
from .github.module import GithubModule
from .github_trending.module import GithubTrendingModule
from .progress.module import ProgressModule
from .random_fact.module import RandomFactModule
from .releases.module import ReleasesModule
from .rss.module import RssModule
from .search.module import SearchModule
from .site_monitor.module import SiteMonitorModule
from .system_monitor.module import SystemMonitorModule
from .todo.module import TodoModule
from .weather.module import WeatherModule

# Registry of all available modules
MODULE_REGISTRY = {
    "animals": AnimalsModule,
    "arxiv": ArxivModule,
    "clock": ClockModule,
    "github": GithubModule,
    "github_trending": GithubTrendingModule,
    "random_fact": RandomFactModule,
    "site_monitor": SiteMonitorModule,
    "progress": ProgressModule,
    "releases": ReleasesModule,
    "rss": RssModule,
    "search": SearchModule,
    "system_monitor": SystemMonitorModule,
    "todo": TodoModule,
    "weather": WeatherModule,
}


def get_module_class(module_id: str) -> type[Module] | None:
    """Get module class by ID. Returns None if not found."""
    return MODULE_REGISTRY.get(module_id)
