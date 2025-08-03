# API 参考

Modular Dashboard 提供了完整的 API 接口，支持模块开发、配置管理、存储系统等功能。本章节详细介绍各个 API 的使用方法。

## 📚 API 文档导航

### 核心接口
- **[模块基类](module-base.md)** - Module 和 ExtendedModule 基类接口
- **[配置 API](configuration.md)** - 配置管理和验证接口
- **[存储 API](storage.md)** - 存储系统和缓存接口

### 工具函数
- **日志工具** - 结构化日志记录
- **网络工具** - HTTP 客户端和网络请求
- **配置工具** - 配置验证和转换
- **事件系统** - 模块间事件通信

## 架构概览

Modular Dashboard 采用分层模块化架构：

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层 (Application)                      │
├─────────────────────────────────────────────────────────────┤
│                    模块层 (Module System)                     │
├─────────────────────────────────────────────────────────────┤
│                    配置层 (Configuration)                     │
├─────────────────────────────────────────────────────────────┤
│                    存储层 (Storage System)                     │
├─────────────────────────────────────────────────────────────┤
│                    UI 层 (User Interface)                      │
└─────────────────────────────────────────────────────────────┘
```

## 核心应用 API

### 主应用类

**位置**: `src/modular_dashboard/app.py`

#### `initialize_app(config: dict[str, Any]) -> None`
初始化 NiceGUI 应用程序，设置静态文件和 CSS 样式。

**参数**:
- `config`: 应用配置字典

**示例**:
```python
from modular_dashboard.app import initialize_app
initialize_app({"theme": "light"})
```

#### `run_app(native: bool = False) -> None`
运行 Modular Dashboard 应用程序。

**参数**:
- `native`: 是否以原生桌面应用模式运行

**示例**:
```python
from modular_dashboard.app import run_app

# Web 模式
run_app(native=False)

# 桌面模式
run_app(native=True)
```

### 路由系统

应用提供以下路由：

- `/` - 主仪表盘页面
- `/module/{module_id}` - 模块详情页面

## 模块系统 API

### Module 基类

**位置**: `src/modular_dashboard/modules/base.py`

#### 抽象属性

所有模块必须实现以下抽象属性：

```python
@property
@abstractmethod
def id(self) -> str: pass

@property
@abstractmethod
def name(self) -> str: pass

@property
@abstractmethod
def icon(self) -> str: pass

@property
@abstractmethod
def description(self) -> str: pass
```

#### 抽象方法

```python
@abstractmethod
def fetch(self) -> list[dict[str, Any]]: pass

@abstractmethod
def render(self) -> None: pass
```

#### 存储和缓存方法

```python
def get_storage(self) -> StorageBackend:
    """获取模块专用的存储后端"""
    pass

def get_cache(self, default_ttl: int = 3600) -> CachedStorage:
    """获取模块专用的缓存"""
    pass

def has_persistence(self) -> bool:
    """检查模块是否需要持久化存储"""
    return False

def has_cache(self) -> bool:
    """检查模块是否使用缓存"""
    return False

def cleanup(self) -> None:
    """清理模块资源"""
    pass
```

### ExtendedModule 扩展基类

**位置**: `src/modular_dashboard/modules/extended.py`

#### 统计信息方法

```python
def get_stats(self) -> dict[str, Any]:
    """获取模块统计信息"""
    return {
        "fetch_count": 0,
        "error_count": 0,
        "last_fetch": None,
        "last_error": None,
    }

def reset_stats(self) -> None:
    """重置模块统计信息"""
    pass
```

#### 异步支持方法

```python
async def async_fetch(self) -> list[dict[str, Any]]:
    """异步版本的数据获取方法"""
    return self.fetch()

def fetch_with_retry(
    self, max_retries: int = 3, retry_delay: float = 1.0
) -> list[dict[str, Any]]:
    """带重试机制的数据获取"""
    pass
```

#### 生命周期方法

```python
def initialize(self) -> None:
    """初始化模块"""
    pass

def shutdown(self) -> None:
    """关闭模块"""
    pass
```

#### 数据导入导出方法

```python
def export_data(self, format: str = "json") -> Any:
    """导出模块数据"""
    pass

def import_data(self, data: Any, format: str = "json") -> bool:
    """导入模块数据"""
    pass
```

#### 配置管理方法

```python
def get_default_config(self) -> dict[str, Any]:
    """获取默认配置"""
    return {}

def validate_config(self, config: dict[str, Any]) -> bool:
    """验证配置"""
    return True

def get_config_schema(self) -> dict[str, Any]:
    """获取配置模式"""
    return {}
```

### 模块注册表

**位置**: `src/modular_dashboard/modules/registry.py`

#### `MODULE_REGISTRY: dict[str, type[Module]]`
所有可用模块的注册表。

**示例**:
```python
from modular_dashboard.modules.registry import MODULE_REGISTRY, get_module_class

# 获取所有可用模块
available_modules = list(MODULE_REGISTRY.keys())

# 获取特定模块类
arxiv_module_class = get_module_class("arxiv")
if arxiv_module_class:
    module = arxiv_module_class(config)
```

#### `get_module_class(module_id: str) -> type[Module] | None`
根据模块 ID 获取模块类。

**参数**:
- `module_id`: 模块唯一标识符

**返回**:
- 模块类或 None（如果未找到）

## 配置管理 API

### 配置管理器

**位置**: `src/modular_dashboard/config/manager.py`

#### `load_config() -> AppConfig`
加载配置文件或创建默认配置。

**返回**:
- `AppConfig`: 应用配置对象

**示例**:
```python
from modular_dashboard.config.manager import load_config

config = load_config()
print(f"主题: {config.theme}")
print(f"列数: {config.layout.columns}")
```

#### `save_config(config: AppConfig) -> None`
保存配置到文件。

**参数**:
- `config`: 要保存的配置对象

**示例**:
```python
from modular_dashboard.config.manager import save_config, load_config

config = load_config()
config.theme = "dark"
save_config(config)
```

#### `get_config_dir() -> pathlib.Path`
获取系统特定的配置目录路径。

**返回**:
- 配置目录的 Path 对象

### 配置数据模型

**位置**: `src/modular_dashboard/config/schema.py`

#### `AppConfig`
应用配置数据类。

**属性**:
- `version`: str - 配置版本
- `theme`: str - 主题模式
- `layout`: LayoutConfig - 布局配置
- `modules`: list[ModuleConfig] - 模块配置列表

#### `LayoutConfig`
布局配置数据类。

**属性**:
- `columns`: int - 列数 (1-3)
- `width`: str - 页面宽度
- `show_nav`: bool - 显示导航栏
- `column_config`: list[ColumnConfig] - 列配置数组

#### `ModuleConfig`
模块配置数据类。

**属性**:
- `id`: str - 模块标识符
- `enabled`: bool - 是否启用
- `position`: int - 显示位置
- `collapsed`: bool - 初始折叠状态
- `config`: dict - 模块特定配置

## 存储系统 API

### 存储管理器

**位置**: `src/modular_dashboard/storage.py`

#### `get_storage_manager() -> StorageManager`
获取全局存储管理器实例。

**返回**:
- `StorageManager`: 存储管理器实例

**示例**:
```python
from modular_dashboard.storage import get_storage_manager

storage_manager = get_storage_manager()
backend = storage_manager.get_backend("my_module")
```

#### `set_storage_manager(manager: StorageManager) -> None`
设置全局存储管理器实例。

### StorageBackend 抽象基类

#### 基本操作方法

```python
@abstractmethod
def get(self, key: str, default: Any = None) -> Any:
    """获取值"""
    pass

@abstractmethod
def set(self, key: str, value: Any) -> None:
    """设置值"""
    pass

@abstractmethod
def delete(self, key: str) -> bool:
    """删除值"""
    pass

@abstractmethod
def exists(self, key: str) -> bool:
    """检查键是否存在"""
    pass

@abstractmethod
def clear(self) -> None:
    """清空所有数据"""
    pass

@abstractmethod
def keys(self) -> list[str]:
    """返回所有键"""
    pass
```

### 具体存储后端

#### JSONFileBackend
JSON 文件存储后端。

**构造函数**:
```python
def __init__(self, file_path: str | Path):
    """初始化 JSON 文件存储后端"""
    pass
```

**示例**:
```python
from modular_dashboard.storage import JSONFileBackend

backend = JSONFileBackend("data.json")
backend.set("user_data", {"name": "John"})
data = backend.get("user_data")
```

#### PickleFileBackend
Pickle 文件存储后端，用于存储复杂对象。

**构造函数**:
```python
def __init__(self, file_path: str | Path):
    """初始化 Pickle 文件存储后端"""
    pass
```

#### MemoryBackend
内存存储后端，用于临时数据存储。

**构造函数**:
```python
def __init__(self):
    """初始化内存存储后端"""
    pass
```

### CachedStorage 缓存存储

#### 带缓存的存储操作

```python
def __init__(self, backend: StorageBackend, default_ttl: int = 3600):
    """初始化缓存存储"""
    pass

def get(self, key: str, default: Any = None) -> Any:
    """获取缓存值（如果未过期）"""
    pass

def set(self, key: str, value: Any, ttl: int | None = None) -> None:
    """设置缓存值"""
    pass

def delete(self, key: str) -> bool:
    """删除缓存值"""
    pass

def cleanup_expired(self) -> None:
    """清理过期缓存"""
    pass
```

**示例**:
```python
from modular_dashboard.storage import JSONFileBackend, CachedStorage

# 创建存储后端
backend = JSONFileBackend("data.json")

# 创建缓存存储（1小时TTL）
cache = CachedStorage(backend, default_ttl=3600)

# 使用缓存
cache.set("api_data", data)
cached_data = cache.get("api_data")
```

### StorageManager 存储管理器

#### 存储管理方法

```python
def get_backend(self, name: str, backend_type: str = "json") -> StorageBackend:
    """获取或创建存储后端"""
    pass

def get_cached_storage(self, name: str, default_ttl: int = 3600) -> CachedStorage:
    """获取或创建缓存存储"""
    pass

def get_module_storage(self, module_id: str) -> StorageBackend:
    """获取模块专用存储"""
    pass

def get_module_cache(self, module_id: str, default_ttl: int = 3600) -> CachedStorage:
    """获取模块专用缓存"""
    pass

def cleanup_expired_caches(self) -> None:
    """清理所有过期缓存"""
    pass

def clear_all(self) -> None:
    """清空所有存储和缓存"""
    pass
```

## UI 组件 API

### 仪表盘 UI

**位置**: `src/modular_dashboard/ui/dashboard.py`

#### `render_dashboard(config: AppConfig) -> None`
渲染主仪表盘界面。

**参数**:
- `config`: 应用配置对象

#### `render_module_detail(module_id: str, config: AppConfig) -> None`
渲染模块详情页面。

**参数**:
- `module_id`: 模块 ID
- `config`: 应用配置对象

### 布局管理

**位置**: `src/modular_dashboard/ui/layout.py`

#### `DashboardLayout`
仪表盘布局管理器。

**构造函数**:
```python
def __init__(self, config: AppConfig):
    """初始化布局管理器"""
    pass

def render(self) -> None:
    """渲染布局"""
    pass
```

### 模块卡片

**位置**: `src/modular_dashboard/ui/module_card.py`

#### `ModuleCard`
模块卡片组件。

**构造函数**:
```python
def __init__(self, module: Module):
    """初始化模块卡片"""
    pass

def render(self) -> None:
    """渲染模块卡片"""
    pass
```

## 工具函数 API

### 日志工具

**位置**: `src/modular_dashboard/utils/logger.py`

#### `get_logger(name: str) -> structlog.stdlib.BoundLogger`
获取结构化日志器。

**参数**:
- `name`: 日志器名称

**返回**:
- 结构化日志器实例

**示例**:
```python
from modular_dashboard.utils.logger import get_logger

logger = get_logger("my_module")
logger.info("Module initialized", module_id="my_module")
```

### 配置验证工具

#### `validate_config_file(config_path: str | Path) -> bool`
验证配置文件格式。

**参数**:
- `config_path`: 配置文件路径

**返回**:
- 验证结果

#### `validate_module_config(module_id: str, config: dict[str, Any]) -> bool`
验证模块配置。

**参数**:
- `module_id`: 模块 ID
- `config`: 模块配置字典

**返回**:
- 验证结果

### 网络工具

#### `http_client_with_timeout(timeout: float = 30.0) -> httpx.Client`
创建带超时的 HTTP 客户端。

**参数**:
- `timeout`: 超时时间（秒）

**返回**:
- HTTPX 客户端实例

**示例**:
```python
from modular_dashboard.utils.http import http_client_with_timeout

with http_client_with_timeout(10.0) as client:
    response = client.get("https://api.example.com/data")
```

## 事件系统 API

### 事件总线

Modular Dashboard 提供简单的事件系统用于模块间通信。

#### `emit(event_name: str, data: Any = None) -> None`
发射事件。

**参数**:
- `event_name`: 事件名称
- `data`: 事件数据

#### `on(event_name: str, callback: Callable) -> None`
监听事件。

**参数**:
- `event_name`: 事件名称
- `callback`: 回调函数

#### `off(event_name: str, callback: Callable) -> None`
移除事件监听器。

**参数**:
- `event_name`: 事件名称
- `callback`: 回调函数

**示例**:
```python
# 发射事件
emit("data_updated", {"module": "arxiv", "count": 5})

# 监听事件
def on_data_updated(data):
    print(f"Data updated: {data}")

on("data_updated", on_data_updated)
```

## 常量 API

### 模块相关常量

```python
# 默认配置
DEFAULT_CONFIG_VERSION = "0.1.0"
DEFAULT_THEME = "light"
DEFAULT_COLUMNS = 3

# 缓存设置
DEFAULT_CACHE_TTL = 3600  # 1小时
MAX_CACHE_SIZE = 1000    # 最大缓存项数

# 网络设置
DEFAULT_TIMEOUT = 30.0   # 默认超时
MAX_RETRIES = 3         # 最大重试次数
```

### 路径常量

```python
# 配置路径
CONFIG_DIR = get_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG_FILE = Path(__file__).parent / "assets" / "default-config.json"

# 存储路径
STORAGE_BASE_PATH = Path.home() / ".modular_dashboard"
CACHE_PATH = STORAGE_BASE_PATH / "cache"
DATA_PATH = STORAGE_BASE_PATH / "data"
```

## 错误代码

### 模块错误代码

| 代码 | 说明 |
|------|------|
| `MODULE_NOT_FOUND` | 模块未找到 |
| `MODULE_INIT_FAILED` | 模块初始化失败 |
| `MODULE_CONFIG_INVALID` | 模块配置无效 |
| `MODULE_FETCH_FAILED` | 数据获取失败 |
| `MODULE_RENDER_FAILED` | 渲染失败 |

### 配置错误代码

| 代码 | 说明 |
|------|------|
| `CONFIG_FILE_NOT_FOUND` | 配置文件未找到 |
| `CONFIG_INVALID_FORMAT` | 配置格式无效 |
| `CONFIG_VALIDATION_FAILED` | 配置验证失败 |

### 存储错误代码

| 代码 | 说明 |
|------|------|
| `STORAGE_BACKEND_ERROR` | 存储后端错误 |
| `CACHE_ERROR` | 缓存错误 |
| `PERSISTENCE_ERROR` | 持久化错误 |

## 使用示例

### 创建自定义模块

```python
from typing import Any
from nicegui import ui
from modular_dashboard.modules.base import Module
from modular_dashboard.modules.extended import ExtendedModule

class CustomModule(ExtendedModule):
    @property
    def id(self) -> str:
        return "custom_module"

    @property
    def name(self) -> str:
        return "Custom Module"

    @property
    def icon(self) -> str:
        return "🔧"

    @property
    def description(self) -> str:
        return "A custom module example"

    def fetch(self) -> list[dict[str, Any]]:
        # 使用缓存
        cache = self.get_cache(default_ttl=1800)
        cached_data = cache.get("custom_data")
        if cached_data:
            return cached_data
        
        # 获取数据
        data = self._fetch_from_api()
        
        # 缓存数据
        cache.set("custom_data", data)
        
        return data

    def render(self) -> None:
        items = self.fetch()
        
        with ui.card().classes("w-full"):
            ui.label(self.name).classes("text-lg font-semibold")
            
            if items:
                for item in items[:3]:  # 显示前3项
                    ui.label(item["title"]).classes("font-medium")
            else:
                ui.label("暂无数据").classes("text-gray-500")

    def _fetch_from_api(self) -> list[dict[str, Any]]:
        # 实现具体的数据获取逻辑
        return [
            {
                "title": "Custom Item",
                "summary": "This is a custom item",
                "link": "https://example.com",
                "published": "2025-07-30T10:00:00Z",
                "tags": ["custom"],
                "extra": {}
            }
        ]
```

### 使用存储系统

```python
from modular_dashboard.storage import get_storage_manager

# 获取存储管理器
storage_manager = get_storage_manager()

# 获取模块专用存储
module_storage = storage_manager.get_module_storage("my_module")

# 存储数据
module_storage.set("user_preferences", {"theme": "dark"})

# 获取数据
preferences = module_storage.get("user_preferences", {})

# 使用缓存
module_cache = storage_manager.get_module_cache("my_module", default_ttl=1800)
module_cache.set("cached_data", data)
cached_data = module_cache.get("cached_data")
```

### 配置管理

```python
from modular_dashboard.config.manager import load_config, save_config
from modular_dashboard.config.schema import AppConfig, ModuleConfig

# 加载配置
config = load_config()

# 修改配置
config.theme = "dark"
config.layout.columns = 2

# 添加新模块
new_module = ModuleConfig(
    id="custom_module",
    enabled=True,
    config={"refresh_interval": 1800}
)
config.modules.append(new_module)

# 保存配置
save_config(config)
```

## 最佳实践

### 1. 错误处理

```python
try:
    data = self.fetch()
    self._current_data = data
except Exception as e:
    logger.error(f"Failed to fetch data: {e}")
    # 使用缓存数据作为后备
    self._current_data = self._load_cached_data()
```

### 2. 资源管理

```python
def __init__(self, config: dict[str, Any] | None = None):
    super().__init__(config)
    self._http_client = None

def initialize(self) -> None:
    self._http_client = httpx.Client(timeout=30.0)

def shutdown(self) -> None:
    if self._http_client:
        self._http_client.close()
    self.cleanup()
```

### 3. 性能优化

```python
def fetch(self) -> list[dict[str, Any]]:
    # 检查缓存
    cache = self.get_cache(default_ttl=self.config.get("refresh_interval", 3600))
    cached_data = cache.get("module_data")
    if cached_data:
        return cached_data
    
    # 获取新数据
    data = self._fetch_with_retry()
    
    # 缓存数据
    cache.set("module_data", data)
    
    return data
```

### 4. 配置验证

```python
def validate_config(self, config: dict[str, Any]) -> bool:
    required_fields = ["api_key", "refresh_interval"]
    
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field: {field}")
            return False
    
    # 验证数值范围
    if not (60 <= config["refresh_interval"] <= 86400):
        logger.error("refresh_interval must be between 60 and 86400")
        return False
    
    return True
```

通过本 API 文档，您可以充分利用 Modular Dashboard 的所有功能，开发出功能强大、性能优越的自定义模块。
