# 配置 API

配置系统管理 Research Dashboard 配置的加载、验证和保存。

## 概述

配置系统由以下部分组成：

1. `src/modular_dashboard/config/schema.py` 中的配置模式定义
2. `src/modular_dashboard/config/manager.py` 中的配置管理
3. `src/modular_dashboard/assets/default-config.json` 中的默认配置

## 模式定义

### AppConfig

主应用程序配置对象。

```python
@dataclass
class AppConfig:
    version: str
    theme: str
    layout: LayoutConfig
    modules: List[ModuleConfig]
```

### LayoutConfig

仪表盘布局的配置。

```python
@dataclass
class LayoutConfig:
    columns: int = 1  # 列数 (1-3)
    width: str = "default"  # "default", "narrow", "wide"
    show_nav: bool = True  # 是否显示导航栏
    column_config: List[ColumnConfig] = None  # 每列的配置
```

### ColumnConfig

单列布局的配置。

```python
@dataclass
class ColumnConfig:
    width: str = "normal"  # "narrow" 或 "normal"
    modules: List[str] = None  # 要在此列中显示的模块 ID 列表
```

### ModuleConfig

单个模块的配置。

```python
@dataclass
class ModuleConfig:
    id: str
    enabled: bool = True
    collapsed: bool = False
    config: dict = None
```

## 配置管理

### load_config

从文件加载配置或在不存在时创建默认配置。

```python
def load_config() -> AppConfig:
    """
    从文件加载配置或在不存在时创建默认配置。

    此函数尝试从系统特定的配置目录加载用户配置。
    如果不存在配置文件，它会使用默认配置模板创建一个。

    返回
    -------
    config : AppConfig
        包含版本、主题、布局和模块设置的应用程序配置对象。
    """
```

### save_config

将配置保存到文件。

```python
def save_config(config: AppConfig) -> None:
    """
    将配置保存到文件。

    参数
    ----------
    config : AppConfig
        要保存的应用程序配置对象。
    """
```

### get_config_dir

获取系统特定的配置目录。

```python
def get_config_dir():
    """
    获取系统特定的配置目录。

    返回
    -------
    config_dir : pathlib.Path
        基于操作系统的配置目录路径。

    说明
    -----
    配置目录按以下方式确定：
    - Windows: %APPDATA%\\ModularDashboard
    - macOS/Linux: ~/.config/ModularDashboard
    - 其他系统: ./config (备用)
    """
```

## 配置文件

### 默认配置

默认配置存储在 `src/modular_dashboard/assets/default-config.json` 中。在创建新用户配置时，此文件用作模板。

### 用户配置

用户配置存储在系统特定的配置目录中：

- **Windows**: `%APPDATA%\\ModularDashboard\\config.json`
- **macOS/Linux**: `~/.config/ModularDashboard/config.json`

此文件在首次运行时创建，用户可以修改它来自定义应用程序。

## 配置验证

配置系统在加载配置文件时执行基本验证：

1. 确保存在必需字段
2. 验证数据类型
3. 为缺少的可选字段提供默认值

对于更复杂的验证，模块可以在其构造函数中实现自己的验证。

## 扩展配置系统

要添加新配置选项：

1. 在 `schema.py` 中向适当的数据类添加新字段
2. 在 `default-config.json` 中更新默认配置
3. 在 `docs/user-guide/configuration.md` 中更新文档
4. 在模块构造函数中实现任何必要的验证

添加新配置选项时，请考虑它们应该是全局的、布局特定的还是模块特定的。
