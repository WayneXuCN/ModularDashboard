"""Module base class."""

from abc import ABC, abstractmethod
from typing import Any


class Module(ABC):
    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the module with optional configuration.

        Args:
            config: Optional dictionary containing module-specific configuration
        """
        self.config = config or {}

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the module."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the module."""
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icon for the module (e.g., emoji or SVG path)."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the module does."""
        pass

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """
        Fetch data from the source and return standardized items.

        Returns:
            List of items with keys:
            - title (str): Item title
            - summary (str): Brief description
            - link (str): URL to the full item
            - published (str): ISO8601 formatted date
            - tags (List[str]): Optional tags
            - extra (Dict): Optional extra fields
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        Render the module's UI using NiceGUI components.
        """
        pass

    def render_detail(self) -> None:
        """
        Render the module's detailed view page.
        By default, it shows the same content as the main view,
        but modules can override this for a more detailed presentation.
        """
        self.render()
