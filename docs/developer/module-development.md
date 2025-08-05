# Module Development Guide

This comprehensive guide details how to develop custom modules for Modular Dashboard. By following this guide, you'll be able to create feature-rich, standards-compliant modules that seamlessly integrate into the dashboard system.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Module Base Classes](#module-base-classes)
- [Creating a Basic Module](#creating-a-basic-module)
- [Data Fetching and Format](#data-fetching-and-format)
- [UI Rendering](#ui-rendering)
- [Configuration Management](#configuration-management)
- [Storage and Caching](#storage-and-caching)
- [Asynchronous Support](#asynchronous-support)
- [Error Handling and Recovery](#error-handling-and-recovery)
- [Module Lifecycle](#module-lifecycle)
- [Complete Example: RSS Reader](#complete-example-rss-reader)
- [Testing](#testing)
- [Best Practices](#best-practices)
- [Publishing and Maintenance](#publishing-and-maintenance)

## Architecture Overview

### Core Design Principles

Modular Dashboard uses a plugin-based module architecture with these core characteristics:

- **Standardized Interface**: All modules implement a unified interface ensuring interoperability
- **Layered Design**: Provides basic and extended base classes to meet different complexity needs
- **Complete Lifecycle**: Includes initialization, runtime, cleanup, and update management
- **Built-in Features**: Integrated storage, caching, statistics, and error handling mechanisms

### Module Types

The system supports multiple types of modules:

1. **Data Source Modules**: Fetch data from external APIs (e.g. ArXiv, GitHub, RSS)
2. **Tool Modules**: Provide utility functions (e.g. clock, weather, todo list)
3. **Monitoring Modules**: Monitor system and network status
4. **Entertainment Modules**: Provide entertainment content (e.g. animal images, random quotes)

## Module Base Classes

### Module Base Class

All modules must inherit from the `Module` base class, which is the most fundamental abstract class:

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

**Core Features**:

- Storage management: `get_storage()` and `get_cache()` methods
- Update support: Built-in module update system
- Resource cleanup: `cleanup()` method
- Optional methods: `render_detail()` for detailed views

### ExtendedModule Class

For modules requiring more complex functionality, you can inherit from `ExtendedModule`:

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
```

**Extended Features**:

- Error handling: Error handlers and retry mechanisms
- Statistics tracking: Fetch count, error count, time statistics
- Asynchronous support: `async_fetch()` method
- Configuration management: Configuration schema validation and UI generation
- Data import/export: Support for JSON, CSV and other formats
- Lifecycle management: `initialize()` and `shutdown()` methods
- Built-in UI components: Statistics, configuration and action buttons

## Creating a Basic Module

### 1. Module File Structure

```
src/modular_dashboard/modules/
├── your_module/
│   ├── __init__.py
│   └── module.py
└── registry.py           # Register your module here
```

### 2. Simplest Module Example

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

### 3. Registering the Module

Add module registration in `registry.py`:

```python
# src/modular_dashboard/modules/registry.py

from .your_module.module import YourModule

MODULE_REGISTRY = {
    "your_module": YourModule,
    # Other existing modules...
}
```

## Data Fetching and Format

### Standard Data Format

The `fetch()` method must return data in the following format:

```python
def fetch(self) -> list[dict[str, Any]]:
    return [
        {
            "title": str,           # Required: Item title
            "summary": str,         # Required: Item summary
            "link": str,            # Required: Item link
            "published": str,       # Required: ISO8601 formatted time
            "tags": list[str],      # Optional: List of tags
            "extra": dict[str, Any] # Optional: Extra data
        }
    ]
```

### Data Fetching Best Practices

#### 1. Network Request Handling

```python
import httpx
from typing import Any

def fetch(self) -> list[dict[str, Any]]:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get("https://api.example.com/data")
            response.raise_for_status()
            data = response.json()
            
            # Transform to standard format
            return self._transform_data(data)
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        return []

def _transform_data(self, raw_data: Any) -> list[dict[str, Any]]:
    """Transform raw data to standard format"""
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

#### 2. Cache Usage

```python
def fetch(self) -> list[dict[str, Any]]:
    cache = self.get_cache(default_ttl=3600)  # 1 hour cache
    
    # Try to get from cache
    cached_data = cache.get("module_data")
    if cached_data:
        return cached_data
    
    # Fetch fresh data
    data = self._fetch_from_source()
    
    # Store in cache
    cache.set("module_data", data)
    
    return data

def _fetch_from_source(self) -> list[dict[str, Any]]:
    """Actual data fetching logic"""
    # Implement actual data fetching
    pass
```

#### 3. Error Handling and Retry

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
            time.sleep(2 ** attempt)  # Exponential backoff
```

## UI Rendering

### Basic Rendering

```python
def render(self) -> None:
    """Main view rendering - displayed in dashboard card"""
    items = self.fetch()
    
    with ui.card().classes("w-full"):
        # Module title
        with ui.row().classes("items-center justify-between w-full"):
            ui.label(self.name).classes("text-lg font-semibold")
            ui.icon(self.icon).classes("text-xl")
        
        # Module content
        if items:
            self._render_main_view(items)
        else:
            ui.label("No data available").classes("text-gray-500")
        
        # Refresh button
        ui.button("Refresh", on_click=self._refresh).classes("mt-2")

def _render_main_view(self, items: list[dict[str, Any]]) -> None:
    """Render main view content"""
    # Usually only display the first or first few items
    for item in items[:2]:  # Display at most 2 items
        with ui.element().classes("mb-2"):
            ui.label(item["title"]).classes("font-medium")
            ui.label(item["summary"][:100] + "...").classes("text-sm text-gray-600")
```

### Detailed View Rendering

```python
def render_detail(self) -> None:
    """Detailed view rendering - displayed on standalone page"""
    items = self.fetch()
    
    with ui.column().classes("w-full gap-4"):
        # Page title
        ui.label(f"{self.name} - Detailed Information").classes("text-2xl font-bold")
        
        # Statistics
        self._render_stats()
        
        # Item list
        if items:
            for item in items:
                self._render_detail_item(item)
        else:
            ui.label("No data available").classes("text-gray-500")

def _render_detail_item(self, item: dict[str, Any]) -> None:
    """Render detailed item"""
    with ui.card().classes("w-full p-4"):
        # Title and link
        with ui.link(target=item["link"]).classes("no-underline"):
            ui.label(item["title"]).classes("text-xl font-bold hover:underline")
        
        # Metadata
        with ui.row().classes("items-center gap-2 my-2"):
            ui.label(item["published"][:10]).classes("text-sm text-gray-500")
            for tag in item.get("tags", [])[:3]:
                ui.chip(tag).classes("text-xs")
        
        # Summary
        ui.label(item["summary"]).classes("text-gray-700")
        
        # Extra information
        if item.get("extra"):
            self._render_extra_info(item["extra"])

def _render_stats(self) -> None:
    """Render statistics"""
    stats = self.get_stats()
    
    with ui.card().classes("w-full p-4 bg-gray-50"):
        ui.label("Statistics").classes("font-semibold mb-2")
        with ui.row().classes("gap-4"):
            ui.label(f"Fetch count: {stats['fetch_count']}").classes("text-sm")
            ui.label(f"Error count: {stats['error_count']}").classes("text-sm")
            if stats.get("last_fetch"):
                ui.label(f"Last update: {stats['last_fetch'].strftime('%H:%M')}").classes("text-sm")
```

## Configuration Management

### Configuration Schema Definition

```python
def get_config_schema(self) -> dict[str, Any]:
    """Define configuration schema"""
    return {
        "api_key": {
            "type": "string",
            "label": "API Key",
            "description": "Key for accessing external API",
            "required": False,
            "secret": True
        },
        "refresh_interval": {
            "type": "number",
            "label": "Refresh Interval",
            "description": "Data refresh interval (seconds)",
            "default": 3600,
            "min": 60,
            "max": 86400
        },
        "max_items": {
            "type": "number",
            "label": "Max Items",
            "description": "Maximum number of items to display",
            "default": 10,
            "min": 1,
            "max": 100
        },
        "enabled_categories": {
            "type": "select",
            "label": "Enabled Categories",
            "description": "Select content categories to display",
            "options": ["All", "Technology", "Science", "Art"],
            "default": "All",
            "multiple": True
        }
    }

def get_default_config(self) -> dict[str, Any]:
    """Get default configuration"""
    return {
        "refresh_interval": 3600,
        "max_items": 10,
        "enabled_categories": ["All"]
    }

def validate_config(self, config: dict[str, Any]) -> bool:
    """Validate configuration"""
    required_fields = ["refresh_interval", "max_items"]
    
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Validate value ranges
    if not (60 <= config["refresh_interval"] <= 86400):
        logger.error("refresh_interval must be between 60 and 86400")
        return False
    
    return True
```

### Configuration Validation and Defaults

```python
def __init__(self, config: dict[str, Any] | None = None):
    super().__init__(config)
    
    # Merge default configuration
    default_config = self.get_default_config()
    self.config = {**default_config, **(self.config or {})}
    
    # Validate configuration
    if not self.validate_config(self.config):
        logger.warning("Invalid config, using defaults")
        self.config = default_config
```

## Storage and Caching

### Persistent Storage

```python
class YourModule(Module):
    def has_persistence(self) -> bool:
        """Check if module requires persistent storage"""
        return True

    def save_user_preferences(self, preferences: dict[str, Any]) -> None:
        """Save user preferences"""
        storage = self.get_storage()
        storage.set("user_preferences", preferences)

    def load_user_preferences(self) -> dict[str, Any]:
        """Load user preferences"""
        storage = self.get_storage()
        return storage.get("user_preferences", {})

    def save_data(self, data: list[dict[str, Any]]) -> None:
        """Save data to persistent storage"""
        storage = self.get_storage()
        storage.set("saved_data", {
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def load_saved_data(self) -> list[dict[str, Any]]:
        """Load data from persistent storage"""
        storage = self.get_storage()
        saved = storage.get("saved_data")
        if saved:
            return saved.get("data", [])
        return []
```

### Cache Usage

```python
class YourModule(Module):
    def has_cache(self) -> bool:
        """Check if module uses cache"""
        return True

    def fetch_with_cache(self) -> list[dict[str, Any]]:
        """Fetch data with cache"""
        cache = self.get_cache(default_ttl=self.config.get("refresh_interval", 3600))
        
        # Try to get from cache
        cached_data = cache.get("fetched_data")
        if cached_data:
            logger.debug("Using cached data")
            return cached_data
        
        # Fetch fresh data
        fresh_data = self._fetch_from_source()
        
        # Store in cache
        cache.set("fetched_data", fresh_data)
        
        logger.debug("Fetched fresh data")
        return fresh_data

    def invalidate_cache(self) -> None:
        """Invalidate cache"""
        cache = self.get_cache()
        cache.delete("fetched_data")
        logger.info("Cache invalidated")
```

## Asynchronous Support

### Asynchronous Data Fetching

```python
class YourModule(ExtendedModule):
    async def async_fetch(self) -> list[dict[str, Any]]:
        """Asynchronous version of data fetching"""
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
        """Fetch data from multiple sources asynchronously"""
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

## Error Handling and Recovery

### Error Handling Strategy

```python
class YourModule(ExtendedModule):
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.add_error_handler(self._handle_fetch_error)
        self.add_error_handler(self._handle_render_error)

    def _handle_fetch_error(self, error: Exception) -> None:
        """Handle data fetching errors"""
        logger.error(f"Fetch error in {self.id}: {error}")
        
        # Try to use cached data
        cache = self.get_cache()
        cached_data = cache.get("fetched_data")
        if cached_data:
            logger.info("Using cached data as fallback")
            self._cached_data = cached_data

    def _handle_render_error(self, error: Exception) -> None:
        """Handle rendering errors"""
        logger.error(f"Render error in {self.id}: {error}")
        
        # Display error state
        ui.label("Failed to load").classes("text-red-500")
        ui.button("Retry", on_click=self._retry_fetch).classes("mt-2")

    def _retry_fetch(self) -> None:
        """Retry data fetching"""
        try:
            self.invalidate_cache()
            data = self.fetch_with_retry()
            if data:
                ui.notify("Data loaded successfully", type="positive")
                # Re-render
                self.render()
            else:
                ui.notify("Retry failed", type="negative")
        except Exception as e:
            ui.notify(f"Retry failed: {str(e)}", type="negative")
```

### Health Check

```python
def health_check(self) -> dict[str, Any]:
    """Module health check"""
    status = {
        "module_id": self.id,
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Check configuration
    try:
        self.validate_config(self.config)
        status["checks"]["config"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["config"] = {"status": "error", "message": str(e)}
        status["status"] = "unhealthy"
    
    # Check network connectivity
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("https://api.example.com/health")
            response.raise_for_status()
            status["checks"]["api"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["api"] = {"status": "error", "message": str(e)}
        status["status"] = "degraded"
    
    # Check cache
    try:
        cache = self.get_cache()
        cache.get("health_check_test")
        status["checks"]["cache"] = {"status": "ok"}
    except Exception as e:
        status["checks"]["cache"] = {"status": "error", "message": str(e)}
        status["status"] = "degraded"
    
    return status
```

## Module Lifecycle

### Lifecycle Methods

```python
class YourModule(ExtendedModule):
    def initialize(self) -> None:
        """Module initialization"""
        if not self._is_initialized:
            try:
                # Initialize resources
                self._setup_http_client()
                self._setup_scheduler()
                self._load_initial_data()
                
                self._is_initialized = True
                logger.info(f"Module {self.id} initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize module {self.id}: {e}")
                raise

    def _setup_http_client(self) -> None:
        """Setup HTTP client"""
        self._http_client = httpx.Client(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5)
        )

    def _setup_scheduler(self) -> None:
        """Setup scheduled tasks"""
        from apscheduler.schedulers.background import BackgroundScheduler
        
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(
            self._scheduled_refresh,
            'interval',
            seconds=self.config.get("refresh_interval", 3600)
        )
        self._scheduler.start()

    def _load_initial_data(self) -> None:
        """Load initial data"""
        try:
            data = self.fetch_with_cache()
            self._current_data = data
        except Exception as e:
            logger.warning(f"Failed to load initial data: {e}")
            self._current_data = []

    def shutdown(self) -> None:
        """Module shutdown"""
        try:
            # Stop scheduled tasks
            if hasattr(self, '_scheduler'):
                self._scheduler.shutdown()
            
            # Close HTTP client
            if hasattr(self, '_http_client'):
                self._http_client.close()
            
            # Cleanup cache
            self.cleanup()
            
            logger.info(f"Module {self.id} shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down module {self.id}: {e}")

    def cleanup(self) -> None:
        """Cleanup resources"""
        if self._cache:
            self._cache.cleanup_expired()
        
        # Save data to persistent storage
        if hasattr(self, '_current_data'):
            self.save_data(self._current_data)
```

## Complete Example: RSS Reader

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
        return "RSS Reader"

    @property
    def icon(self) -> str:
        return "📡"

    @property
    def description(self) -> str:
        return "Subscribe and read RSS feeds"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_config_schema(self) -> dict[str, Any]:
        return {
            "feed_urls": {
                "type": "string",
                "label": "RSS Feed URLs",
                "description": "RSS feed URLs, separated by commas",
                "default": ""
            },
            "refresh_interval": {
                "type": "number",
                "label": "Refresh Interval",
                "description": "Refresh interval (minutes)",
                "default": 30,
                "min": 5,
                "max": 1440
            },
            "max_items": {
                "type": "number",
                "label": "Max Items",
                "description": "Maximum items to display per feed",
                "default": 10,
                "min": 1,
                "max": 50
            },
            "show_description": {
                "type": "boolean",
                "label": "Show Description",
                "description": "Whether to show item descriptions",
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
        """Fetch RSS data"""
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
        
        # Sort by publication time
        all_items.sort(key=lambda x: x["published"], reverse=True)
        
        # Limit total items
        max_total = self.config.get("max_items", 10) * len(urls)
        all_items = all_items[:max_total]
        
        # Cache data
        cache.set("rss_data", all_items)
        
        return all_items

    def _fetch_feed(self, url: str) -> list[dict[str, Any]]:
        """Fetch a single RSS feed"""
        try:
            # Use httpx to fetch RSS content
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                
                # Parse with feedparser
                feed = feedparser.parse(response.content)
                
                items = []
                for entry in feed.entries[:self.config.get("max_items", 10)]:
                    # Parse publication time
                    published = entry.get("published", "")
                    if published:
                        try:
                            published = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z").isoformat()
                        except ValueError:
                            published = datetime.now().isoformat()
                    else:
                        published = datetime.now().isoformat()
                    
                    items.append({
                        "title": entry.get("title", "Untitled"),
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
        """Render main view"""
        items = self.fetch()
        
        with ui.card().classes("w-full"):
            # Title bar
            with ui.row().classes("items-center justify-between w-full mb-3"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon(self.icon).classes("text-xl")
                    ui.label(self.name).classes("text-lg font-semibold")
                
                ui.button("Refresh", on_click=self._refresh).props("flat").classes("text-sm")
            
            # Content area
            if items:
                # Display first 5 items
                for item in items[:5]:
                    self._render_item(item)
            else:
                ui.label("No RSS content available").classes("text-gray-500 text-center py-4")

    def _render_item(self, item: dict[str, Any]) -> None:
        """Render a single item"""
        with ui.element().classes("border-l-2 border-blue-200 pl-3 mb-3"):
            # Title and link
            with ui.link(target=item["link"]).classes("no-underline"):
                ui.label(item["title"]).classes(
                    "font-medium text-sm hover:text-blue-600 transition-colors"
                )
            
            # Publication time and source
            with ui.row().classes("items-center gap-2 mt-1"):
                ui.label(item["published"][:10]).classes("text-xs text-gray-500")
                if item["extra"].get("source_title"):
                    ui.label(item["extra"]["source_title"]).classes(
                        "text-xs text-gray-400 bg-gray-100 px-1 rounded"
                    )
            
            # Description
            if self.config.get("show_description", True) and item["summary"]:
                ui.label(item["summary"]).classes("text-xs text-gray-600 mt-1")

    def render_detail(self) -> None:
        """Render detailed view"""
        items = self.fetch()
        
        with ui.column().classes("w-full gap-4"):
            # Page title
            with ui.row().classes("items-center justify-between w-full"):
                with ui.row().classes("items-center gap-3"):
                    ui.icon(self.icon).classes("text-3xl")
                    ui.label(self.name).classes("text-2xl font-bold")
                
                ui.button("Refresh", on_click=self._refresh).classes("bg-blue-500 text-white")
            
            # Statistics
            stats = self.get_stats()
            with ui.card().classes("w-full p-4 bg-gray-50"):
                with ui.row().classes("gap-6"):
                    ui.label(f"Total items: {len(items)}").classes("text-sm")
                    ui.label(f"Fetch count: {stats['fetch_count']}").classes("text-sm")
                    if stats.get("last_fetch"):
                        ui.label(f"Last update: {stats['last_fetch'].strftime('%H:%M:%S')}").classes("text-sm")
            
            # Configuration
            with ui.expansion("Configuration").classes("w-full"):
                self.render_config_ui()
            
            # Item list
            if items:
                for item in items:
                    self._render_detail_item(item)
            else:
                ui.label("No RSS content available").classes("text-gray-500 text-center py-8")

    def _render_detail_item(self, item: dict[str, Any]) -> None:
        """Render detailed item"""
        with ui.card().classes("w-full p-4 hover:shadow-md transition-shadow"):
            # Title and link
            with ui.link(target=item["link"]).classes("no-underline"):
                ui.label(item["title"]).classes(
                    "text-lg font-semibold hover:text-blue-600 transition-colors"
                )
            
            # Metadata
            with ui.row().classes("items-center gap-3 mt-2 flex-wrap"):
                ui.label(item["published"][:19].replace("T", " ")).classes("text-sm text-gray-500")
                
                if item["extra"].get("author"):
                    ui.label(f"Author: {item['extra']['author']}").classes("text-sm text-gray-600")
                
                if item["extra"].get("source_title"):
                    ui.label(item["extra"]["source_title"]).classes(
                        "text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded"
                    )
                
                # Tags
                for tag in item.get("tags", [])[:3]:
                    ui.chip(tag).classes("text-xs")

    def _refresh(self) -> None:
        """Refresh data"""
        try:
            self.invalidate_cache()
            ui.notify("Refresh successful", type="positive")
        except Exception as e:
            ui.notify(f"Refresh failed: {str(e)}", type="negative")

    def has_persistence(self) -> bool:
        return True

    def has_cache(self) -> bool:
        return True
```

## Testing

### Unit Tests

```python
# tests/modules/test_your_module.py

import pytest
from unittest.mock import Mock, patch
from modular_dashboard.modules.your_module.module import YourModule

class TestYourModule:
    def setup_method(self):
        """Setup before tests"""
        self.config = {
            "refresh_interval": 3600,
            "max_items": 10
        }
        self.module = YourModule(self.config)

    def test_module_properties(self):
        """Test module basic properties"""
        assert self.module.id == "your_module"
        assert self.module.name == "Your Module"
        assert self.module.icon == "📦"
        assert self.module.description == "A simple example module"

    @patch('httpx.Client.get')
    def test_fetch_success(self, mock_get):
        """Test successful data fetching"""
        # Mock API response
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
        
        # Execute test
        result = self.module.fetch()
        
        # Verify results
        assert len(result) == 1
        assert result[0]["title"] == "Test Item"
        assert result[0]["summary"] == "Test description"
        assert result[0]["link"] == "https://example.com"

    @patch('httpx.Client.get')
    def test_fetch_error(self, mock_get):
        """Test error handling"""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        # Execute test
        result = self.module.fetch()
        
        # Verify results
        assert result == []

    def test_config_validation(self):
        """Test configuration validation"""
        # Valid configuration
        valid_config = {"refresh_interval": 3600, "max_items": 10}
        assert self.module.validate_config(valid_config) == True
        
        # Invalid configuration
        invalid_config = {"refresh_interval": -1}
        assert self.module.validate_config(invalid_config) == False

    def test_cache_operations(self):
        """Test cache operations"""
        # Set cache data
        cache = self.module.get_cache()
        test_data = [{"title": "Cached Item"}]
        cache.set("test_key", test_data)
        
        # Get cache data
        cached_data = cache.get("test_key")
        assert cached_data == test_data
        
        # Delete cache data
        cache.delete("test_key")
        assert cache.get("test_key") is None
```

### Integration Tests

```python
# tests/integration/test_module_integration.py

import pytest
from modular_dashboard.modules.registry import MODULE_REGISTRY

class TestModuleIntegration:
    def test_module_registration(self):
        """Test module registration"""
        assert "your_module" in MODULE_REGISTRY
        assert MODULE_REGISTRY["your_module"] == YourModule

    def test_module_instantiation(self):
        """Test module instantiation"""
        module_class = MODULE_REGISTRY["your_module"]
        module = module_class({"refresh_interval": 1800})
        
        assert module.id == "your_module"
        assert module.config["refresh_interval"] == 1800

    @pytest.mark.asyncio
    async def test_async_fetch(self):
        """Test asynchronous data fetching"""
        module = YourModule({})
        
        # If module supports async fetching
        if hasattr(module, 'async_fetch'):
            data = await module.async_fetch()
            assert isinstance(data, list)
```

## Best Practices

### 1. Performance Optimization

- **Caching Strategy**: Set appropriate cache times to avoid frequent API calls
- **Batch Requests**: Combine multiple API requests to reduce network overhead
- **Lazy Loading**: Load data only when needed
- **Resource Management**: Close network connections and clean up resources in a timely manner

### 2. Error Handling

- **Graceful Degradation**: Provide reasonable default behavior in error situations
- **Retry Mechanism**: Implement retry strategies for transient errors
- **User Feedback**: Provide clear error messages and suggestions
- **Logging**: Record detailed error information for debugging

### 3. User Experience

- **Loading States**: Show progress indicators when loading data
- **Empty States**: Provide friendly prompts for no-data states
- **Responsive Design**: Ensure proper display on different screen sizes
- **Interactive Feedback**: Provide immediate feedback for user actions

### 4. Security Considerations

- **Input Validation**: Validate all external input and data
- **Access Control**: Limit access to sensitive operations
- **Data Protection**: Do not log sensitive information
- **Network Security**: Use HTTPS and secure API calls

### 5. Code Quality

- **Type Hints**: Use type hints to improve code readability and IDE support
- **Docstrings**: Write detailed docstrings for all public methods
- **Unit Tests**: Write unit tests for core functionality
- **Code Reuse**: Extract common functionality into helper methods

## Publishing and Maintenance

### 1. Version Management

```python
@property
def version(self) -> str:
    return "1.0.0"
```

### 2. Documentation

- **Module Description**: Detailed description of module functionality and purpose
- **Configuration Guide**: Explanation of all configuration options
- **Usage Examples**: Typical usage scenarios and configurations
- **Troubleshooting**: List of common issues and solutions

### 3. Update Strategy

- **Backward Compatibility**: Maintain backward compatibility of configuration and interfaces
- **Migration Guide**: Provide migration guidance for major changes
- **Changelog**: Record changes between versions
- **Test Coverage**: Ensure new features have adequate test coverage

### 4. Performance Monitoring

- **Statistics**: Track module usage and performance metrics
- **Error Rate**: Monitor module error rate and success rate
- **Response Time**: Monitor data fetching and rendering response times
- **Resource Usage**: Monitor module memory and CPU usage

By following this guide, you'll be able to develop high-quality, maintainable Modular Dashboard modules that provide rich functionality and a great user experience.
