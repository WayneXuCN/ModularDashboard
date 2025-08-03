# 模块开发指南

本指南详细介绍如何为 Modular Dashboard 开发自定义模块。通过遵循本指南，您将能够创建功能丰富、符合标准的模块，无缝集成到仪表盘系统中。

## 模块系统概述

### 模块架构

Modular Dashboard 采用基于插件模块的架构，每个模块都是独立的组件，具有以下特点：

- **独立封装**：每个模块都是自包含的，有自己的配置和数据
- **标准接口**：所有模块都实现统一的接口，确保互操作性
- **动态加载**：模块在运行时动态加载，支持热插拔
- **生命周期管理**：完整的模块生命周期管理，包括初始化、运行和清理

### 模块类型

系统支持多种类型的模块：

1. **数据源模块**：从外部 API 获取数据（如 ArXiv、GitHub、RSS）
2. **工具模块**：提供实用功能（如时钟、天气、待办事项）
3. **监控模块**：监控系统和网络状态
4. **娱乐模块**：提供娱乐内容（如动物图片、随机引用）

## 模块基类

### Module 基类

所有模块都必须继承自 `Module` 基类：

```python
from abc import ABC, abstractmethod
from typing import Any

class Module(ABC):
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self._storage: StorageBackend | None = None
        self._cache: CachedStorage | None = None
        self._storage_manager = get_storage_manager()

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

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]: pass

    @abstractmethod
    def render(self) -> None: pass
```

### ExtendedModule 扩展基类

对于需要更复杂功能的模块，可以继承 `ExtendedModule`：

```python
class ExtendedModule(Module):
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self._refresh_callbacks: list[Callable] = []
        self._error_handlers: list[Callable] = []
        self._is_initialized = False
        self._last_error: Exception | None = None
        self._stats: dict[str, Any] = {
            "fetch_count": 0,
            "error_count": 0,
            "last_fetch": None,
            "last_error": None,
        }

    # 提供额外功能：异步支持、重试机制、错误处理、统计信息等
```

## 创建基础模块

### 1. 模块文件结构

```
src/modular_dashboard/modules/
├── your_module/
│   ├── __init__.py
│   └── module.py
└── registry.py           # 需要在此注册模块
```

### 2. 最简单的模块示例

```python
# src/modular_dashboard/modules/your_module/module.py

from typing import Any
from nicegui import ui
from ..base import Module

class YourModule(Module):
    @property
    def id(self) -> str:
        return "your_module"

    @property
    def name(self) -> str:
        return "Your Module"

    @property
    def icon(self) -> str:
        return "📦"

    @property
    def description(self) -> str:
        return "A simple example module"

    def fetch(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Example Item",
                "summary": "This is an example item",
                "link": "https://example.com",
                "published": "2025-07-30T10:00:00Z",
                "tags": ["example"],
                "extra": {}
            }
        ]

    def render(self) -> None:
        items = self.fetch()
        if items:
            item = items[0]
            with ui.element().classes("w-full"):
                ui.label(item["title"]).classes("text-lg font-bold")
                ui.label(item["summary"]).classes("text-gray-600")
```

### 3. 注册模块

在 `registry.py` 中添加模块注册：

```python
# src/modular_dashboard/modules/registry.py

from .your_module.module import YourModule

MODULE_REGISTRY = {
    "your_module": YourModule,
    # 其他现有模块...
}
```

## 数据获取和返回格式

### 标准数据格式

`fetch()` 方法必须返回符合以下格式的数据：

```python
def fetch(self) -> list[dict[str, Any]]:
    return [
        {
            "title": str,           # 必需：项目标题
            "summary": str,         # 必需：项目摘要
            "link": str,            # 必需：项目链接
            "published": str,       # 必需：ISO8601 格式时间
            "tags": list[str],      # 可选：标签列表
            "extra": dict[str, Any] # 可选：额外数据
        }
    ]
```

### 数据获取最佳实践

#### 1. 网络请求处理

```python
import httpx
from typing import Any

def fetch(self) -> list[dict[str, Any]]:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get("https://api.example.com/data")
            response.raise_for_status()
            data = response.json()
            
            # 转换为标准格式
            return self._transform_data(data)
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return []

def _transform_data(self, raw_data: Any) -> list[dict[str, Any]]:
    """将原始数据转换为标准格式"""
    transformed = []
    for item in raw_data.get("items", []):
        transformed.append({
            "title": item.get("title", ""),
            "summary": item.get("description", ""),
            "link": item.get("url", ""),
            "published": item.get("created_at", ""),
            "tags": item.get("tags", []),
            "extra": {
                "author": item.get("author"),
                "category": item.get("category")
            }
        })
    return transformed
```

#### 2. 缓存使用

```python
def fetch(self) -> list[dict[str, Any]]:
    cache = self.get_cache(default_ttl=3600)  # 1小时缓存
    
    # 尝试从缓存获取
    cached_data = cache.get("module_data")
    if cached_data:
        return cached_data
    
    # 获取新数据
    data = self._fetch_from_source()
    
    # 存储到缓存
    cache.set("module_data", data)
    
    return data

def _fetch_from_source(self) -> list[dict[str, Any]]:
    """实际的数据获取逻辑"""
    # 实现具体的数据获取
    pass
```

#### 3. 错误处理和重试

```python
def fetch_with_retry(self, max_retries: int = 3) -> list[dict[str, Any]]:
    for attempt in range(max_retries):
        try:
            return self._fetch_from_source()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                return []
            logger.warning(f"Attempt {attempt + 1} failed, retrying...")
            import time
            time.sleep(2 ** attempt)  # 指数退避
```

## UI 渲染

### 基础渲染

```python
def render(self) -> None:
    """主视图渲染 - 显示在仪表盘卡片中"""
    items = self.fetch()
    
    with ui.card().classes("w-full"):
        # 模块标题
        with ui.row().classes("items-center justify-between w-full"):
            ui.label(self.name).classes("text-lg font-semibold")
            ui.icon(self.icon).classes("text-xl")
        
        # 模块内容
        if items:
            self._render_main_view(items)
        else:
            ui.label("暂无数据").classes("text-gray-500")
        
        # 刷新按钮
        ui.button("刷新", on_click=self._refresh).classes("mt-2")

def _render_main_view(self, items: list[dict[str, Any]]) -> None:
    """渲染主视图内容"""
    # 通常只显示第一个或前几个项目
    for item in items[:2]:  # 最多显示2个项目
        with ui.element().classes("mb-2"):
            ui.label(item["title"]).classes("font-medium")
            ui.label(item["summary"][:100] + "...").classes("text-sm text-gray-600")
```

### 详细视图渲染

```python
def render_detail(self) -> None:
    """详细视图渲染 - 显示在独立页面中"""
    items = self.fetch()
    
    with ui.column().classes("w-full gap-4"):
        # 页面标题
        ui.label(f"{self.name} - 详细信息").classes("text-2xl font-bold")
        
        # 统计信息
        self._render_stats()
        
        # 项目列表
        if items:
            for item in items:
                self._render_detail_item(item)
        else:
            ui.label("暂无数据").classes("text-gray-500")

def _render_detail_item(self, item: dict[str, Any]) -> None:
    """渲染详细项目"""
    with ui.card().classes("w-full p-4"):
        # 标题和链接
        with ui.link(target=item["link"]).classes("no-underline"):
            ui.label(item["title"]).classes("text-xl font-bold hover:underline")
        
        # 元数据
        with ui.row().classes("items-center gap-2 my-2"):
            ui.label(item["published"][:10]).classes("text-sm text-gray-500")
            for tag in item.get("tags", [])[:3]:
                ui.chip(tag).classes("text-xs")
        
        # 摘要
        ui.label(item["summary"]).classes("text-gray-700")
        
        # 额外信息
        if item.get("extra"):
            self._render_extra_info(item["extra"])

def _render_stats(self) -> None:
    """渲染统计信息"""
    stats = self.get_stats()
    
    with ui.card().classes("w-full p-4 bg-gray-50"):
        ui.label("统计信息").classes("font-semibold mb-2")
        with ui.row().classes("gap-4"):
            ui.label(f"获取次数: {stats['fetch_count']}").classes("text-sm")
            ui.label(f"错误次数: {stats['error_count']}").classes("text-sm")
            if stats.get("last_fetch"):
                ui.label(f"最后更新: {stats['last_fetch'].strftime('%H:%M')}").classes("text-sm")
```

### 配置界面渲染

```python
def render_config_ui(self) -> None:
    """渲染配置界面"""
    schema = self.get_config_schema()
    
    with ui.card().classes("w-full p-4"):
        ui.label(f"{self.name} 配置").classes("text-lg font-semibold mb-4")
        
        for field_name, field_config in schema.items():
            self._render_config_field(field_name, field_config)

def _render_config_field(self, field_name: str, field_config: dict[str, Any]) -> None:
    """渲染单个配置字段"""
    field_type = field_config.get("type", "string")
    field_label = field_config.get("label", field_name)
    field_default = field_config.get("default", "")
    
    with ui.column().classes("w-full gap-1 mb-3"):
        ui.label(field_label).classes("text-sm font-medium")
        
        if field_type == "string":
            ui.input(
                placeholder=field_label,
                value=self.config.get(field_name, field_default),
            ).bind_value(self.config, field_name).classes("w-full")
        
        elif field_type == "number":
            ui.number(
                label=field_label,
                value=self.config.get(field_name, field_default),
            ).bind_value(self.config, field_name).classes("w-full")
        
        elif field_type == "boolean":
            ui.switch(
                text=field_label,
                value=self.config.get(field_name, field_default),
            ).bind_value(self.config, field_name)
        
        elif field_type == "select":
            ui.select(
                options=field_config.get("options", []),
                label=field_label,
                value=self.config.get(field_name, field_default),
            ).bind_value(self.config, field_name).classes("w-full")
```

## 配置管理

### 配置模式定义

```python
def get_config_schema(self) -> dict[str, Any]:
    """定义配置模式"""
    return {
        "api_key": {
            "type": "string",
            "label": "API 密钥",
            "description": "用于访问外部 API 的密钥",
            "required": False,
            "secret": True
        },
        "refresh_interval": {
            "type": "number",
            "label": "刷新间隔",
            "description": "数据刷新的时间间隔（秒）",
            "default": 3600,
            "min": 60,
            "max": 86400
        },
        "max_items": {
            "type": "number",
            "label": "最大项目数",
            "description": "显示的最大项目数量",
            "default": 10,
            "min": 1,
            "max": 100
        },
        "enabled_categories": {
            "type": "select",
            "label": "启用的分类",
            "description": "选择要显示的内容分类",
            "options": ["全部", "技术", "科学", "艺术"],
            "default": "全部",
            "multiple": True
        }
    }

def get_default_config(self) -> dict[str, Any]:
    """获取默认配置"""
    return {
        "refresh_interval": 3600,
        "max_items": 10,
        "enabled_categories": ["全部"]
    }

def validate_config(self, config: dict[str, Any]) -> bool:
    """验证配置"""
    required_fields = ["refresh_interval", "max_items"]
    
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

### 配置验证和默认值

```python
def __init__(self, config: dict[str, Any] | None = None):
    super().__init__(config)
    
    # 合并默认配置
    default_config = self.get_default_config()
    self.config = {**default_config, **(self.config or {})}
    
    # 验证配置
    if not self.validate_config(self.config):
        logger.warning("Invalid config, using defaults")
        self.config = default_config
```

## 存储和缓存

### 持久化存储

```python
class YourModule(Module):
    def has_persistence(self) -> bool:
        """检查模块是否需要持久化存储"""
        return True

    def save_user_preferences(self, preferences: dict[str, Any]) -> None:
        """保存用户偏好设置"""
        storage = self.get_storage()
        storage.set("user_preferences", preferences)

    def load_user_preferences(self) -> dict[str, Any]:
        """加载用户偏好设置"""
        storage = self.get_storage()
        return storage.get("user_preferences", {})

    def save_data(self, data: list[dict[str, Any]]) -> None:
        """保存数据到持久化存储"""
        storage = self.get_storage()
        storage.set("saved_data", {
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def load_saved_data(self) -> list[dict[str, Any]]:
        """从持久化存储加载数据"""
        storage = self.get_storage()
        saved = storage.get("saved_data")
        if saved:
            return saved.get("data", [])
        return []
```

### 缓存使用

```python
class YourModule(Module):
    def has_cache(self) -> bool:
        """检查模块是否使用缓存"""
        return True

    def fetch_with_cache(self) -> list[dict[str, Any]]:
        """带缓存的数据获取"""
        cache = self.get_cache(default_ttl=self.config.get("refresh_interval", 3600))
        
        # 尝试从缓存获取
        cached_data = cache.get("fetched_data")
        if cached_data:
            logger.debug("Using cached data")
            return cached_data
        
        # 获取新数据
        fresh_data = self._fetch_from_source()
        
        # 存储到缓存
        cache.set("fetched_data", fresh_data)
        
        logger.debug("Fetched fresh data")
        return fresh_data

    def invalidate_cache(self) -> None:
        """使缓存失效"""
        cache = self.get_cache()
        cache.delete("fetched_data")
        logger.info("Cache invalidated")
```

## 异步支持

### 异步数据获取

```python
class YourModule(ExtendedModule):
    async def async_fetch(self) -> list[dict[str, Any]]:
        """异步版本的数据获取"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("https://api.example.com/data")
                response.raise_for_status()
                data = response.json()
                return self._transform_data(data)
        except Exception as e:
            logger.error(f"Async fetch failed: {e}")
            return []

    async def fetch_multiple_sources(self) -> list[dict[str, Any]]:
        """从多个源异步获取数据"""
        urls = [
            "https://api.example.com/source1",
            "https://api.example.com/source2",
            "https://api.example.com/source3"
        ]
        
        async with httpx.AsyncClient() as client:
            tasks = [client.get(url) for url in urls]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        results = []
        for response in responses:
            if isinstance(response, Exception):
                logger.error(f"Request failed: {response}")
                continue
            
            try:
                response.raise_for_status()
                data = response.json()
                results.extend(self._transform_data(data))
            except Exception as e:
                logger.error(f"Failed to process response: {e}")
        
        return results
```

## 错误处理和恢复

### 错误处理策略

```python
class YourModule(ExtendedModule):
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.add_error_handler(self._handle_fetch_error)
        self.add_error_handler(self._handle_render_error)

    def _handle_fetch_error(self, error: Exception) -> None:
        """处理数据获取错误"""
        logger.error(f"Fetch error in {self.id}: {error}")
        
        # 尝试使用缓存数据
        cache = self.get_cache()
        cached_data = cache.get("fetched_data")
        if cached_data:
            logger.info("Using cached data as fallback")
            self._cached_data = cached_data

    def _handle_render_error(self, error: Exception) -> None:
        """处理渲染错误"""
        logger.error(f"Render error in {self.id}: {error}")
        
        # 显示错误状态
        ui.label("加载失败").classes("text-red-500")
        ui.button("重试", on_click=self._retry_fetch).classes("mt-2")

    def _retry_fetch(self) -> None:
        """重试数据获取"""
        try:
            self.invalidate_cache()
            data = self.fetch_with_retry()
            if data:
                ui.notify("数据加载成功", type="positive")
                # 重新渲染
                self.render()
            else:
                ui.notify("重试失败", type="negative")
        except Exception as e:
            ui.notify(f"重试失败: {str(e)}", type="negative")
```

### 健康检查

```python
def health_check(self) -> dict[str, Any]:
    """模块健康检查"""
    status = {
        "module_id": self.id,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # 检查配置
    try:
        self.validate_config(self.config)
        status["checks"]["config"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["config"] = {"status": "error", "message": str(e)}
        status["status"] = "unhealthy"
    
    # 检查网络连接
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("https://api.example.com/health")
            response.raise_for_status()
            status["checks"]["api"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["api"] = {"status": "error", "message": str(e)}
        status["status"] = "degraded"
    
    # 检查缓存
    try:
        cache = self.get_cache()
        cache.get("health_check_test")
        status["checks"]["cache"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["cache"] = {"status": "error", "message": str(e)}
        status["status"] = "degraded"
    
    return status
```

## 模块生命周期

### 生命周期方法

```python
class YourModule(ExtendedModule):
    def initialize(self) -> None:
        """模块初始化"""
        if not self._is_initialized:
            try:
                # 初始化资源
                self._setup_http_client()
                self._setup_scheduler()
                self._load_initial_data()
                
                self._is_initialized = True
                logger.info(f"Module {self.id} initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize module {self.id}: {e}")
                raise

    def _setup_http_client(self) -> None:
        """设置 HTTP 客户端"""
        self._http_client = httpx.Client(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5)
        )

    def _setup_scheduler(self) -> None:
        """设置定时任务"""
        from apscheduler.schedulers.background import BackgroundScheduler
        
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(
            self._scheduled_refresh,
            'interval',
            seconds=self.config.get("refresh_interval", 3600)
        )
        self._scheduler.start()

    def _load_initial_data(self) -> None:
        """加载初始数据"""
        try:
            data = self.fetch_with_cache()
            self._current_data = data
        except Exception as e:
            logger.warning(f"Failed to load initial data: {e}")
            self._current_data = []

    def shutdown(self) -> None:
        """模块关闭"""
        try:
            # 停止定时任务
            if hasattr(self, '_scheduler'):
                self._scheduler.shutdown()
            
            # 关闭 HTTP 客户端
            if hasattr(self, '_http_client'):
                self._http_client.close()
            
            # 清理缓存
            self.cleanup()
            
            logger.info(f"Module {self.id} shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down module {self.id}: {e}")

    def cleanup(self) -> None:
        """清理资源"""
        if self._cache:
            self._cache.cleanup_expired()
        
        # 保存数据到持久化存储
        if hasattr(self, '_current_data'):
            self.save_data(self._current_data)
```

## 实际模块示例

### RSS 阅读器模块

```python
# src/modular_dashboard/modules/rss_reader/module.py

import feedparser
import httpx
from datetime import datetime, timedelta
from typing import Any
from loguru import logger
from nicegui import ui

from ..extended import ExtendedModule

class RSSReaderModule(ExtendedModule):
    @property
    def id(self) -> str:
        return "rss_reader"

    @property
    def name(self) -> str:
        return "RSS 阅读器"

    @property
    def icon(self) -> str:
        return "📡"

    @property
    def description(self) -> str:
        return "订阅和阅读 RSS 源"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_config_schema(self) -> dict[str, Any]:
        return {
            "feed_urls": {
                "type": "string",
                "label": "RSS 源 URL",
                "description": "RSS 源的 URL，多个源用逗号分隔",
                "default": ""
            },
            "refresh_interval": {
                "type": "number",
                "label": "刷新间隔",
                "description": "刷新间隔（分钟）",
                "default": 30,
                "min": 5,
                "max": 1440
            },
            "max_items": {
                "type": "number",
                "label": "最大项目数",
                "description": "每个源显示的最大项目数",
                "default": 10,
                "min": 1,
                "max": 50
            },
            "show_description": {
                "type": "boolean",
                "label": "显示描述",
                "description": "是否显示项目描述",
                "default": True
            }
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "feed_urls": "https://example.com/feed.xml",
            "refresh_interval": 30,
            "max_items": 10,
            "show_description": True
        }

    def fetch(self) -> list[dict[str, Any]]:
        """获取 RSS 数据"""
        urls = self.config.get("feed_urls", "").split(",")
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            return []
        
        cache = self.get_cache(default_ttl=self.config.get("refresh_interval", 30) * 60)
        cached_data = cache.get("rss_data")
        if cached_data:
            return cached_data
        
        all_items = []
        
        for url in urls:
            try:
                items = self._fetch_feed(url)
                all_items.extend(items)
            except Exception as e:
                logger.error(f"Failed to fetch feed {url}: {e}")
        
        # 按时间排序
        all_items.sort(key=lambda x: x["published"], reverse=True)
        
        # 限制数量
        max_total = self.config.get("max_items", 10) * len(urls)
        all_items = all_items[:max_total]
        
        # 缓存数据
        cache.set("rss_data", all_items)
        
        return all_items

    def _fetch_feed(self, url: str) -> list[dict[str, Any]]:
        """获取单个 RSS 源"""
        try:
            # 使用 httpx 获取 RSS 内容
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                
                # 使用 feedparser 解析
                feed = feedparser.parse(response.content)
                
                items = []
                for entry in feed.entries[:self.config.get("max_items", 10)]:
                    # 解析发布时间
                    published = entry.get("published", "")
                    if published:
                        try:
                            published = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z").isoformat()
                        except ValueError:
                            published = datetime.now().isoformat()
                    else:
                        published = datetime.now().isoformat()
                    
                    items.append({
                        "title": entry.get("title", "无标题"),
                        "summary": entry.get("summary", "")[:200],
                        "link": entry.get("link", ""),
                        "published": published,
                        "tags": [tag.get("term", "") for tag in entry.get("tags", [])],
                        "extra": {
                            "author": entry.get("author", ""),
                            "source_url": url,
                            "source_title": feed.feed.get("title", "")
                        }
                    })
                
                return items
                
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
            return []

    def render(self) -> None:
        """渲染主视图"""
        items = self.fetch()
        
        with ui.card().classes("w-full"):
            # 标题栏
            with ui.row().classes("items-center justify-between w-full mb-3"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon(self.icon).classes("text-xl")
                    ui.label(self.name).classes("text-lg font-semibold")
                
                ui.button("刷新", on_click=self._refresh).props("flat").classes("text-sm")
            
            # 内容区域
            if items:
                # 显示前 5 个项目
                for item in items[:5]:
                    self._render_item(item)
            else:
                ui.label("暂无 RSS 内容").classes("text-gray-500 text-center py-4")

    def _render_item(self, item: dict[str, Any]) -> None:
        """渲染单个项目"""
        with ui.element().classes("border-l-2 border-blue-200 pl-3 mb-3"):
            # 标题和链接
            with ui.link(target=item["link"]).classes("no-underline"):
                ui.label(item["title"]).classes(
                    "font-medium text-sm hover:text-blue-600 transition-colors"
                )
            
            # 发布时间和来源
            with ui.row().classes("items-center gap-2 mt-1"):
                ui.label(item["published"][:10]).classes("text-xs text-gray-500")
                if item["extra"].get("source_title"):
                    ui.label(item["extra"]["source_title"]).classes(
                        "text-xs text-gray-400 bg-gray-100 px-1 rounded"
                    )
            
            # 描述
            if self.config.get("show_description", True) and item["summary"]:
                ui.label(item["summary"]).classes("text-xs text-gray-600 mt-1")

    def render_detail(self) -> None:
        """渲染详细视图"""
        items = self.fetch()
        
        with ui.column().classes("w-full gap-4"):
            # 页面标题
            with ui.row().classes("items-center justify-between w-full"):
                with ui.row().classes("items-center gap-3"):
                    ui.icon(self.icon).classes("text-3xl")
                    ui.label(self.name).classes("text-2xl font-bold")
                
                ui.button("刷新", on_click=self._refresh).classes("bg-blue-500 text-white")
            
            # 统计信息
            stats = self.get_stats()
            with ui.card().classes("w-full p-4 bg-gray-50"):
                with ui.row().classes("gap-6"):
                    ui.label(f"总项目数: {len(items)}").classes("text-sm")
                    ui.label(f"获取次数: {stats['fetch_count']}").classes("text-sm")
                    if stats.get("last_fetch"):
                        ui.label(f"最后更新: {stats['last_fetch'].strftime('%H:%M:%S')}").classes("text-sm")
            
            # 配置
            with ui.expansion("配置").classes("w-full"):
                self.render_config_ui()
            
            # 项目列表
            if items:
                for item in items:
                    self._render_detail_item(item)
            else:
                ui.label("暂无 RSS 内容").classes("text-gray-500 text-center py-8")

    def _render_detail_item(self, item: dict[str, Any]) -> None:
        """渲染详细项目"""
        with ui.card().classes("w-full p-4 hover:shadow-md transition-shadow"):
            # 标题和链接
            with ui.link(target=item["link"]).classes("no-underline"):
                ui.label(item["title"]).classes(
                    "text-lg font-semibold hover:text-blue-600 transition-colors"
                )
            
            # 元数据
            with ui.row().classes("items-center gap-3 mt-2 flex-wrap"):
                ui.label(item["published"][:19].replace("T", " ")).classes("text-sm text-gray-500")
                
                if item["extra"].get("author"):
                    ui.label(f"作者: {item['extra']['author']}").classes("text-sm text-gray-600")
                
                if item["extra"].get("source_title"):
                    ui.label(item["extra"]["source_title"]).classes(
                        "text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded"
                    )
                
                # 标签
                for tag in item.get("tags", [])[:3]:
                    ui.chip(tag).classes("text-xs")

    def _refresh(self) -> None:
        """刷新数据"""
        try:
            self.invalidate_cache()
            ui.notify("刷新成功", type="positive")
        except Exception as e:
            ui.notify(f"刷新失败: {str(e)}", type="negative")

    def has_persistence(self) -> bool:
        return True

    def has_cache(self) -> bool:
        return True
```

## 模块测试

### 单元测试

```python
# tests/modules/test_your_module.py

import pytest
from unittest.mock import Mock, patch
from modular_dashboard.modules.your_module.module import YourModule

class TestYourModule:
    def setup_method(self):
        """测试前设置"""
        self.config = {
            "refresh_interval": 3600,
            "max_items": 10
        }
        self.module = YourModule(self.config)

    def test_module_properties(self):
        """测试模块基本属性"""
        assert self.module.id == "your_module"
        assert self.module.name == "Your Module"
        assert self.module.icon == "📦"
        assert self.module.description == "A simple example module"

    @patch('httpx.Client.get')
    def test_fetch_success(self, mock_get):
        """测试成功的数据获取"""
        # 模拟 API 响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "title": "Test Item",
                    "description": "Test description",
                    "url": "https://example.com",
                    "created_at": "2025-07-30T10:00:00Z"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 执行测试
        result = self.module.fetch()
        
        # 验证结果
        assert len(result) == 1
        assert result[0]["title"] == "Test Item"
        assert result[0]["summary"] == "Test description"
        assert result[0]["link"] == "https://example.com"

    @patch('httpx.Client.get')
    def test_fetch_error(self, mock_get):
        """测试错误处理"""
        # 模拟网络错误
        mock_get.side_effect = Exception("Network error")
        
        # 执行测试
        result = self.module.fetch()
        
        # 验证结果
        assert result == []

    def test_config_validation(self):
        """测试配置验证"""
        # 有效配置
        valid_config = {"refresh_interval": 3600, "max_items": 10}
        assert self.module.validate_config(valid_config) == True
        
        # 无效配置
        invalid_config = {"refresh_interval": -1}
        assert self.module.validate_config(invalid_config) == False

    def test_cache_operations(self):
        """测试缓存操作"""
        # 设置缓存数据
        cache = self.module.get_cache()
        test_data = [{"title": "Cached Item"}]
        cache.set("test_key", test_data)
        
        # 获取缓存数据
        cached_data = cache.get("test_key")
        assert cached_data == test_data
        
        # 删除缓存数据
        cache.delete("test_key")
        assert cache.get("test_key") is None
```

### 集成测试

```python
# tests/integration/test_module_integration.py

import pytest
from modular_dashboard.modules.registry import MODULE_REGISTRY

class TestModuleIntegration:
    def test_module_registration(self):
        """测试模块注册"""
        assert "your_module" in MODULE_REGISTRY
        assert MODULE_REGISTRY["your_module"] == YourModule

    def test_module_instantiation(self):
        """测试模块实例化"""
        module_class = MODULE_REGISTRY["your_module"]
        module = module_class({"refresh_interval": 1800})
        
        assert module.id == "your_module"
        assert module.config["refresh_interval"] == 1800

    @pytest.mark.asyncio
    async def test_async_fetch(self):
        """测试异步数据获取"""
        module = YourModule({})
        
        # 如果模块支持异步获取
        if hasattr(module, 'async_fetch'):
            data = await module.async_fetch()
            assert isinstance(data, list)
```

## 最佳实践

### 1. 性能优化

- **缓存策略**：合理设置缓存时间，避免频繁的 API 调用
- **批量请求**：合并多个 API 请求，减少网络开销
- **懒加载**：只在需要时加载数据
- **资源管理**：及时关闭网络连接和清理资源

### 2. 错误处理

- **优雅降级**：在错误情况下提供合理的默认行为
- **重试机制**：对临时性错误实施重试策略
- **用户反馈**：提供清晰的错误信息和建议
- **日志记录**：记录详细的错误信息用于调试

### 3. 用户体验

- **加载状态**：在数据加载时显示进度指示器
- **空状态**：为无数据状态提供友好的提示
- **响应式设计**：确保在不同屏幕尺寸下正常显示
- **交互反馈**：为用户操作提供即时反馈

### 4. 安全考虑

- **输入验证**：验证所有外部输入和数据
- **权限控制**：限制敏感操作的访问权限
- **数据保护**：不在日志中记录敏感信息
- **网络安全**：使用 HTTPS 和安全的 API 调用

## 发布和维护

### 1. 版本管理

```python
@property
def version(self) -> str:
    return "1.0.0"
```

### 2. 文档

- **模块说明**：详细描述模块的功能和用途
- **配置说明**：说明所有配置选项的作用
- **使用示例**：提供典型的使用场景和配置
- **故障排除**：列出常见问题和解决方案

### 3. 更新策略

- **向后兼容**：保持配置和接口的向后兼容性
- **迁移指南**：为重大变更提供迁移指导
- **变更日志**：记录版本间的变更内容
- **测试覆盖**：确保新功能有充分的测试覆盖

通过遵循本指南，您将能够开发出高质量、易维护的 Modular Dashboard 模块，为用户提供丰富的功能和良好的体验。