<div align="center">

# Modular Dashboard

<!-- Project Status & Release -->
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/WayneXuCN/ModularDashboard?label=latest%20release)](https://github.com/WayneXuCN/ModularDashboard/releases)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/WayneXuCN/ModularDashboard?label=latest%20tag)](https://github.com/WayneXuCN/ModularDashboard/tags)
[![Documentation Status](https://img.shields.io/badge/docs-available-brightgreen)](https://waynexucn.github.io/ModularDashboard/)
[![GitHub last commit](https://img.shields.io/github/last-commit/WayneXuCN/ModularDashboard)](https://github.com/WayneXuCN/ModularDashboard/commits/main)

<!-- Community & Activity -->
[![GitHub stars](https://img.shields.io/github/stars/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/watchers)

</div>

<div align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a>
</div>

A modern, modular, and extensible dashboard application for aggregating information from multiple sources into a single, customizable interface.

## 🌟 Overview

Modular Dashboard is a local, modular, and extensible information aggregation dashboard designed to provide users with a unified entry point for daily information. With its highly customizable card-based layout, it aggregates dynamic information from multiple data sources, allowing users to have a comprehensive view of their important information at a glance.

## 🚀 Key Features

- **Modular Architecture**: Plugin-based system with dynamic loading and extensibility
- **Modern UI**: Responsive user interface with light/dark theme support powered by [NiceGUI](https://nicegui.io)
- **Flexible Layout**: Configurable single, double, or triple-column layouts
- **Rich Module Ecosystem**: Built-in modules for various data sources
- **Smart Storage**: Multi-backend storage system with caching and data persistence
- **Cross-Platform**: Runs as both web application and native desktop application
- **Highly Configurable**: JSON-based configuration files for real-time updates

## 🧩 Available Modules

<div align="center">

| Module | Icon | Description | Data Source | Update Frequency | Customizable |
|--------|------|-------------|-------------|------------------|--------------|
| **Clock** | 🕐 | Real-time clock with customizable time formats | System Time | Real-time | ✅ Format, Timezone |
| **Weather** | ☁️ | Weather information for your location | Weather API | Hourly | ✅ Location, Units |
| **Todo** | 📝 | Simple task management with persistence | Local Storage | Manual | ✅ Categories, Priority |
| **Arxiv** | 📚 | Latest research papers based on your interests | ArXiv API | Daily | ✅ Keywords, Categories |
| **Animals** | 🐱 | Cute animal images to brighten your day | Random APIs | On Refresh | ✅ Animal Types |
| **RSS** | 📡 | RSS feed reader for your favorite sources | RSS Feeds | Configurable | ✅ Feeds, Refresh Rate |
| **GitHub** | 🐙 | GitHub activity tracking for users and repositories | GitHub API | Hourly | ✅ Users, Repos, Events |
| **Releases** | 📦 | Latest software releases tracking | GitHub Releases | Daily | ✅ Repository Selection |

</div>

### Module Features

- **🔄 Auto-refresh**: All modules support configurable automatic updates
- **💾 Caching**: Smart caching system reduces API calls and improves performance  
- **🎨 Theming**: Consistent visual design that adapts to light/dark themes
- **⚙️ Configuration**: JSON-based configuration for easy customization
- **🔧 Extensible**: Plugin architecture allows easy addition of new modules

### Key Dependencies

```python
# Core Framework
nicegui>=2.0.0                 # Modern web UI framework
pywebview>=5.0                 # Desktop application wrapper

# Data Fetching & Processing  
httpx>=0.25.0                  # Async HTTP client
requests>=2.25.0               # HTTP library
beautifulsoup4>=4.9.0          # HTML/XML parser
feedparser>=6.0.0              # RSS/Atom feed parser
arxiv>=2.0.0                   # ArXiv API client

# Task Management & Logging
APScheduler>=3.0.0             # Background task scheduler
loguru>=0.7.0                  # Structured logging
structlog>=25.0.0              # Structured logging framework

# Development & Documentation
mkdocs-material>=9.0.0         # Documentation theme
pytest>=6.0.0                  # Testing framework
black                          # Code formatter
mypy                           # Type checking
```

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- [uv package manager](https://docs.astral.sh/uv/) (recommended)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/WayneXuCN/ModularDashboard.git
   cd ModularDashboard
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Run the application**

   ```bash
   # Run as web application
   uv run -m modular_dashboard.app
   
   # Run as native desktop application
   uv run -m modular_dashboard.app --native
   ```

## ⚙️ Configuration

Modular Dashboard uses JSON configuration files for customization. On first run, the application creates a default configuration in your system's config directory:

- **Windows**: `%APPDATA%\ModularDashboard\config.json`
- **macOS/Linux**: `~/.config/ModularDashboard/config.json`

You can customize:

- Layout (1-3 columns with different module arrangements)
- Theme (light/dark)
- Module-specific settings
- Enabled/disabled modules

## 🧪 Development

### Setting up the Development Environment

```bash
# Clone and enter the project directory
git clone https://github.com/WayneXuCN/ModularDashboard.git
cd ModularDashboard

# Install dependencies with development tools
uv sync --extra dev

# Run tests
uv run pytest
```

### Project Structure

```
ModularDashboard/
├── src/modular_dashboard/          # Main application code
│   ├── app.py                      # Application entry point
│   ├── config/                     # Configuration management
│   ├── modules/                    # Module system
│   ├── ui/                         # UI components
│   ├── storage.py                  # Storage system
│   └── utils/                      # Utility functions
├── config/                         # Example configurations
├── docs/                           # Documentation
├── scripts/                        # Helper scripts
└── pyproject.toml                  # Project configuration
```

### Creating Custom Modules

To create a custom module, extend the [Module](src/modular_dashboard/modules/base.py) base class:

```python
from modular_dashboard.modules.base import Module

class MyCustomModule(Module):
    @property
    def id(self) -> str:
        return "my_module"
    
    @property
    def name(self) -> str:
        return "My Custom Module"
    
    @property
    def icon(self) -> str:
        return "custom_icon"
    
    @property
    def description(self) -> str:
        return "Description of what my module does"
    
    def fetch(self) -> list[dict[str, Any]]:
        # Fetch data from your source
        return [
            {
                "title": "Item Title",
                "summary": "Brief description",
                "link": "https://example.com",
                "published": "2023-01-01T00:00:00Z",
                "tags": ["tag1", "tag2"]
            }
        ]
    
    def render(self) -> None:
        # Render the module UI using NiceGUI components
        ui.label("Hello from My Custom Module!")
```

Register your module in [registry.py](src/modular_dashboard/modules/registry.py):

```python
from .my_module.module import MyCustomModule

MODULE_REGISTRY = {
    # ... existing modules
    "my_module": MyCustomModule,
}
```

## 📚 Documentation

For detailed documentation, check the [docs](docs/) directory or run:

```bash
uv run mkdocs serve
```

Then visit <http://localhost:8000> in your browser.

## 🗺️ Roadmap

### Current Version (v0.1.x)

- [x] Core modular architecture
- [x] Basic module ecosystem (Clock, Weather, Todo, etc.)
- [x] JSON-based configuration system
- [x] Light/Dark theme support
- [x] Desktop and web deployment options

### Next Release (v0.2.x)

- [ ] **Enhanced Module System**
  - [ ] Module marketplace/store
  - [ ] Hot module reloading
  - [ ] Module dependency management
- [ ] **User Experience**
  - [ ] Drag & drop layout editor
  - [ ] Module search and filtering
  - [ ] Keyboard shortcuts
- [ ] **Data & Security**
  - [ ] Encrypted data storage options
  - [ ] Multi-user support
  - [ ] Cloud synchronization

### Future Releases (v0.3.x+)

- [ ] **Advanced Features**
  - [ ] AI-powered content recommendations
  - [ ] Integration with popular services (Notion, Slack, etc.)
  - [ ] Mobile companion app
- [ ] **Enterprise Features**
  - [ ] Team/organization dashboards
  - [ ] Role-based access control
  - [ ] Analytics and reporting
- [ ] **Platform Expansion**
  - [ ] Browser extension
  - [ ] Docker container deployment
  - [ ] Cloud hosting options

> 📢 **Want to contribute to these goals?** Check out our [contribution guide](docs/development/contributing.md) and join our community!

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](docs/development/contributing.md) for details on how to submit pull requests, report issues, or request features.

Areas where we especially welcome contributions:

- New modules for different data sources
- UI/UX improvements
- Performance optimizations
- Documentation enhancements
- Bug fixes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
