# Configuration API

Configuration系统管理 Research Dashboard Configuration的加载、验证和保存。

## Overview

Configuration系统由以下部分组成：

1. `src/research_dashboard/config/schema.py` 中的Configuration模式定义
2. `src/research_dashboard/config/manager.py` 中的Configuration管理
3. `src/research_dashboard/assets/default-config.json` 中的默认Configuration

## 模式定义

### AppConfig

主应用程序Configuration对象。

```python
@dataclass
class AppConfig:
    version: str
    theme: str
    layout: LayoutConfig
    modules: List[ModuleConfig]
```

### LayoutConfig

仪表盘布局的Configuration。

```python
@dataclass
class LayoutConfig:
    columns: int = 1  # 列数 (1-3)
    width: str = "default"  # "default", "narrow", "wide"
    show_nav: bool = True  # 是否显示导航栏
    center_content: bool = False  # 是否垂直居中内容
    column_config: List[ColumnConfig] = None  # 每列的Configuration
```

### ColumnConfig

单列布局的Configuration。

```python
@dataclass
class ColumnConfig:
    width: str = "normal"  # "narrow" 或 "normal"
    modules: List[str] = None  # 要在此列中显示的Modules ID 列表
```

### ModuleConfig

单个Modules的Configuration。

```python
@dataclass
class ModuleConfig:
    id: str
    enabled: bool = True
    collapsed: bool = False
    config: dict = None
```

## Configuration管理

### load_config

从文件加载Configuration或在不存在时创建默认Configuration。

```python
def load_config() -> AppConfig:
    """
    从文件加载Configuration或在不存在时创建默认Configuration。

    此函数尝试从系统特定的ConfigurationTable of Contents加载用户Configuration。
    如果不存在Configuration文件，它会使用默认Configuration模板创建一个。

    返回
    -------
    config : AppConfig
        包含版本、主题、布局和Modules设置的应用程序Configuration对象。
    """
```

### save_config

将Configuration保存到文件。

```python
def save_config(config: AppConfig) -> None:
    """
    将Configuration保存到文件。

    参数
    ----------
    config : AppConfig
        要保存的应用程序Configuration对象。
    """
```

### get_config_dir

获取系统特定的ConfigurationTable of Contents。

```python
def get_config_dir():
    """
    获取系统特定的ConfigurationTable of Contents。

    返回
    -------
    config_dir : pathlib.Path
        基于操作系统的ConfigurationTable of Contents路径。

    说明
    -----
    ConfigurationTable of Contents按以下方式确定：
    - Windows: %APPDATA%\\ResearchDashboard
    - macOS/Linux: ~/.config/ResearchDashboard
    - 其他系统: ./config (备用)
    """
```

## Configuration文件

### 默认Configuration

默认Configuration存储在 `src/research_dashboard/assets/default-config.json` 中。在创建新用户Configuration时，此文件用作模板。

### 用户Configuration

用户Configuration存储在系统特定的ConfigurationTable of Contents中：

- **Windows**: `%APPDATA%\\ResearchDashboard\\config.json`
- **macOS/Linux**: `~/.config/ResearchDashboard/config.json`

此文件在首次运行时创建，用户可以修改它来自定义应用程序。

## Configuration验证

Configuration系统在加载Configuration文件时执行基本验证：

1. 确保存在必需字段
2. 验证数据类型
3. 为缺少的可选字段提供默认值

对于更复杂的验证，Modules可以在其构造函数中实现自己的验证。

## 扩展Configuration系统

要添加新Configuration选项：

1. 在 `schema.py` 中向适当的数据类添加新字段
2. 在 `default-config.json` 中更新默认Configuration
3. 在 `docs/user-guide/configuration.md` 中更新文档
4. 在Modules构造函数中实现任何必要的验证

添加新Configuration选项时，请考虑它们应该是全局的、布局特定的还是Modules特定的。