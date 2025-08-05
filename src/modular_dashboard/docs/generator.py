"""Documentation generation system for Modular Dashboard."""

import json
from pathlib import Path
from typing import Any

from ..config.manager import load_config
from ..modules.registry import MODULE_REGISTRY


def generate_module_docs() -> None:
    """Generate documentation for all modules."""
    docs_dir = Path("docs/modules")
    docs_dir.mkdir(exist_ok=True)

    # Load configuration
    config = load_config()

    # Generate index page
    with open(docs_dir / "index.md", "w") as f:
        f.write("# Modules Documentation\n\n")
        f.write(
            "This section contains documentation for all modules in the Modular Dashboard.\n\n"
        )
        f.write("## Available Modules\n\n")

        for module_config in config.modules:
            if module_config.enabled and module_config.id in MODULE_REGISTRY:
                module_class = MODULE_REGISTRY[module_config.id]
                module = module_class()

                f.write(f"- [{module.name}](./{module.id}.md) - {module.description}\n")

                # Generate individual module documentation
                generate_module_detail_docs(module, docs_dir)


def generate_module_detail_docs(module: Any, docs_dir: Path) -> None:
    """Generate detailed documentation for a specific module."""
    with open(docs_dir / f"{module.id}.md", "w") as f:
        f.write(f"# {module.name}\n\n")
        f.write(f"**ID**: `{module.id}`\n\n")
        f.write(f"**Icon**: {module.icon}\n\n")
        f.write(f"**Description**: {module.description}\n\n")

        # Add section for data format
        f.write("## Data Format\n\n")
        f.write("This module provides data in the following standardized format:\n\n")
        f.write("```json\n")
        f.write("{\n")
        f.write('  "title": "string",\n')
        f.write('  "summary": "string",\n')
        f.write('  "link": "string (URL)",\n')
        f.write('  "published": "string (ISO8601)",\n')
        f.write('  "tags": "List[string]",\n')
        f.write('  "extra": "Dict (optional additional fields)"\n')
        f.write("}\n")
        f.write("```\n\n")

        # Add example data
        f.write("## Example Data\n\n")
        f.write("Here's an example of the data provided by this module:\n\n")
        f.write("```json\n")
        example_data = module.fetch()
        if example_data:
            f.write(json.dumps(example_data[0], indent=2))
        f.write("\n```\n")


def generate_api_docs() -> None:
    """Generate API documentation."""
    docs_dir = Path("docs/api")
    docs_dir.mkdir(exist_ok=True)

    with open(docs_dir / "index.md", "w") as f:
        f.write("# API Documentation\n\n")
        f.write(
            "This section documents the internal APIs of the Modular Dashboard.\n\n"
        )

        # Configuration API
        f.write("## Configuration API\n\n")
        f.write(
            "The configuration system is managed through the following components:\n\n"
        )
        f.write("- `config.manager` - Functions for loading and saving configuration\n")
        f.write(
            "- `config.schema` - Data classes defining the configuration structure\n\n"
        )

        # Module API
        f.write("## Module API\n\n")
        f.write(
            "Modules implement a standardized interface defined in `modules.base.Module`:\n\n"
        )
        f.write("```python\n")
        f.write("class Module(ABC):\n")
        f.write("    @property\n")
        f.write("    @abstractmethod\n")
        f.write("    def id(self) -> str: ...\n\n")
        f.write("    @property\n")
        f.write("    @abstractmethod\n")
        f.write("    def name(self) -> str: ...\n\n")
        f.write("    @property\n")
        f.write("    @abstractmethod\n")
        f.write("    def icon(self) -> str: ...\n\n")
        f.write("    @property\n")
        f.write("    @abstractmethod\n")
        f.write("    def description(self) -> str: ...\n\n")
        f.write("    @abstractmethod\n")
        f.write("    def fetch(self) -> List[Dict[str, Any]]: ...\n\n")
        f.write("    @abstractmethod\n")
        f.write("    def render(self) -> None: ...\n\n")
        f.write("    def render_detail(self) -> None: ...\n")
        f.write("```\n")


def generate_development_docs() -> None:
    """Generate development documentation."""
    docs_dir = Path("docs/development")
    docs_dir.mkdir(exist_ok=True)

    with open(docs_dir / "index.md", "w") as f:
        f.write("# Development Guide\n\n")
        f.write(
            "This guide provides information for developers working on the Modular Dashboard.\n\n"
        )

        # Project structure
        f.write("## Project Structure\n\n")
        f.write("```\n")
        f.write("modular-dashboard/\n")
        f.write("│\n")
        f.write("├── pyproject.toml             # Project configuration\n")
        f.write("├── README.md                  # Project overview\n")
        f.write("├── LICENSE                    # License information\n")
        f.write("├── .gitignore                 # Git ignore patterns\n")
        f.write("│\n")
        f.write("├── src/\n")
        f.write("│   └── modular_dashboard/    # Main source code\n")
        f.write("│       ├── __init__.py\n")
        f.write("│       ├── __main__.py        # Entry point\n")
        f.write("│       ├── app.py             # Main application logic\n")
        f.write("│       │\n")
        f.write("│       ├── config/            # Configuration system\n")
        f.write("│       ├── modules/           # Module system\n")
        f.write("│       ├── ui/                # User interface components\n")
        f.write("│       ├── static/            # Static assets\n")
        f.write("│       ├── utils/             # Utility functions\n")
        f.write("│       └── assets/            # Application assets\n")
        f.write("│\n")
        f.write("├── config/                    # User configuration\n")
        f.write("├── scripts/                   # Utility scripts\n")
        f.write("├── tests/                     # Test suite\n")
        f.write("└── docs/                      # Documentation\n")
        f.write("```\n\n")

        # Getting started
        f.write("## Getting Started\n\n")
        f.write("1. Install dependencies:\n")
        f.write("   ```bash\n")
        f.write("   uv pip install -e .\n")
        f.write("   ```\n\n")
        f.write("2. Run the application:\n")
        f.write("   ```bash\n")
        f.write("   uv run -m modular_dashboard\n")
        f.write("   ```\n\n")
        f.write("3. Run as native desktop app:\n")
        f.write("   ```bash\n")
        f.write("   uv run -m modular_dashboard --native\n")
        f.write("   ```\n")


def generate_documentation() -> None:
    """Generate all documentation."""
    print("Generating documentation...")

    # Create main docs directory if it doesn't exist
    Path("docs").mkdir(exist_ok=True)

    # Generate main documentation index
    with open("docs/index.md", "w") as f:
        f.write("# Modular Dashboard Documentation\n\n")
        f.write("Welcome to the Modular Dashboard documentation.\n\n")
        f.write("## Table of Contents\n\n")
        f.write("- [Modules](./modules/index.md)\n")
        f.write("- [API Reference](./api/index.md)\n")
        f.write("- [Development Guide](./development/index.md)\n")
        f.write("- [README](./README.md)\n\n")

    # Generate module documentation
    generate_module_docs()

    # Generate API documentation
    generate_api_docs()

    # Generate development documentation
    generate_development_docs()

    # Copy README to docs
    with open("README.md") as src, open("docs/README.md", "w") as dst:
        dst.write(src.read())

    print("Documentation generated successfully!")


if __name__ == "__main__":
    generate_documentation()
