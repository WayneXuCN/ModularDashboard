"""Module registry."""

from .arxiv.module import ArxivModule
from .base import Module
from .github.module import GithubModule
from .rss.module import RssModule

# Registry of all available modules
MODULE_REGISTRY = {
    "arxiv": ArxivModule,
    "github": GithubModule,
    "rss": RssModule,
}

def get_module_class(module_id: str) -> type[Module] | None:
    """Get module class by ID. Returns None if not found."""
    return MODULE_REGISTRY.get(module_id)
