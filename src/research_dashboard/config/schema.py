"""Configuration schema definitions."""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ModuleConfig:
    id: str
    enabled: bool
    position: int
    collapsed: bool
    refresh_interval: int
    config: Dict

@dataclass
class LayoutConfig:
    columns: int = 3
    view: str = "grid"  # "grid" | "list"
    card_size: str = "medium"

@dataclass
class AppConfig:
    version: str
    theme: str
    layout: LayoutConfig
    modules: List[ModuleConfig]