# Configuration API

The configuration system in Research Dashboard manages all user preferences and module settings.

## Configuration Schema

The configuration is defined by several data classes:

### AppConfig

```python
@dataclass
class AppConfig:
    version: str
    theme: str
    layout: LayoutConfig
    modules: List[ModuleConfig]
```

### LayoutConfig

```python
@dataclass
class LayoutConfig:
    columns: int = 3
    view: str = "grid"  # "grid" | "list"
    card_size: str = "medium"
```

### ModuleConfig

```python
@dataclass
class ModuleConfig:
    id: str
    enabled: bool
    position: int
    collapsed: bool
    refresh_interval: int
    config: Dict
```

## Configuration Manager

The configuration manager provides functions for loading and saving configurations:

### load_config()

```python
def load_config() -> AppConfig:
    """Load configuration from file or create default config if not exists."""
    pass
```

### save_config()

```python
def save_config(config: AppConfig) -> None:
    """Save configuration to file."""
    pass
```

## Configuration Files

- **Default Configuration**: `src/research_dashboard/assets/default-config.json`
- **User Configuration**: `config/user-config.json` (created on first run)

The user configuration file is created from the default configuration on first run and can be modified to customize the dashboard.