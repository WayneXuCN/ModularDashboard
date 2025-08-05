"""Configuration schema definitions."""

from dataclasses import dataclass

from .memory_config import MemoryConfig


@dataclass
class ModuleConfig:
    id: str
    enabled: bool = True
    position: int = 0
    collapsed: bool = False
    config: dict = None

    def __post_init__(self):
        if self.config is None:
            self.config = {}


@dataclass
class ColumnConfig:
    width: str = "normal"  # "narrow" or "normal"
    modules: list[str] = None  # List of module IDs to display in this column

    def __post_init__(self):
        if self.modules is None:
            self.modules = []


@dataclass
class LayoutConfig:
    columns: int = 1  # Number of columns (1-3)
    width: str = "default"  # "slim", "default", "wide"
    show_nav: bool = True  # Whether to show navigation bar
    column_config: list[ColumnConfig] = None  # Configuration for each column

    def __post_init__(self):
        if self.column_config is None:
            # Default to 1 column with normal width
            self.column_config = [ColumnConfig() for _ in range(self.columns)]


@dataclass
class AppConfig:
    version: str
    theme: str
    layout: LayoutConfig
    modules: list[ModuleConfig]
    memory: MemoryConfig = None

    def __post_init__(self):
        if self.memory is None:
            self.memory = MemoryConfig()
