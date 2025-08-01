# Module Base Class

All modules in Research Dashboard inherit from the base `Module` class, which defines the common interface.

## Class Definition

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Module(ABC):
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
    def fetch(self) -> List[Dict[str, Any]]:
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
```

## Required Properties

Each module must implement the following properties:

- `id`: A unique string identifier for the module
- `name`: A human-readable name for the module
- `icon`: An icon to represent the module (emoji or SVG path)
- `description`: A brief description of the module's purpose

## Required Methods

Each module must implement the following methods:

- `fetch()`: Returns a list of standardized items from the module's data source
- `render()`: Renders the module's UI in the main dashboard view

## Optional Methods

- `render_detail()`: Renders the module's UI in the detailed view (defaults to calling `render()`)

## Data Format

The `fetch()` method should return data in the following standardized format:

```json
[
  {
    "title": "string",
    "summary": "string",
    "link": "string (URL)",
    "published": "string (ISO8601)",
    "tags": "List[string]",
    "extra": "Dict (optional additional fields)"
  }
]
```