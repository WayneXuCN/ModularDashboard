# 存储 API

Modular Dashboard 提供了强大的存储系统，支持多种存储后端、智能缓存机制和数据持久化。本 API 文档详细介绍存储系统的使用方法。

## 📋 概述

### 核心特性
- **多后端支持**：JSON 文件、Pickle 文件、内存存储
- **智能缓存**：TTL 缓存、自动过期、内存管理
- **线程安全**：支持多线程并发访问
- **接口统一**：统一的存储接口，易于切换后端

### 架构设计
```
┌─────────────────────────────────────────────────────────────┐
│                    StorageManager                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   Backend Pool  │ │   Cache Pool    │ │   Module Mgr    │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                 StorageBackend (Interface)                  │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │  JSONFileBackend│ │PickleFileBackend│ │  MemoryBackend  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   CachedStorage                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │    TTL Logic    │ │   Memory Cache   │ │   Cleanup       │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 基本使用

```python
from modular_dashboard.storage import get_storage_manager

# 获取存储管理器
storage_manager = get_storage_manager()

# 获取模块专用存储
module_storage = storage_manager.get_module_storage("my_module")

# 基本操作
module_storage.set("key", "value")
value = module_storage.get("key")
module_storage.delete("key")
```

### 使用缓存

```python
# 获取模块专用缓存
module_cache = storage_manager.get_module_cache("my_module", default_ttl=3600)

# 缓存操作
module_cache.set("cached_data", data)
cached_data = module_cache.get("cached_data")
```

## 📚 API 参考

### StorageManager

存储管理器是存储系统的核心组件，负责管理所有存储后端和缓存实例。

#### 获取存储管理器

```python
from modular_dashboard.storage import get_storage_manager, set_storage_manager

# 获取全局存储管理器
storage_manager = get_storage_manager()

# 设置自定义存储管理器
set_storage_manager(custom_manager)
```

#### 模块存储管理

```python
def get_module_storage(self, module_id: str) -> StorageBackend:
    """获取模块专用存储后端
    
    Args:
        module_id: 模块唯一标识符
        
    Returns:
        模块专用的存储后端实例
    """

def get_module_cache(self, module_id: str, default_ttl: int = 3600) -> CachedStorage:
    """获取模块专用缓存
    
    Args:
        module_id: 模块唯一标识符
        default_ttl: 默认缓存时间（秒）
        
    Returns:
        模块专用的缓存存储实例
    """
```

#### 存储后端管理

```python
def get_backend(self, name: str, backend_type: str = "json") -> StorageBackend:
    """获取或创建存储后端
    
    Args:
        name: 存储后端名称
        backend_type: 后端类型（json/pickle/memory）
        
    Returns:
        存储后端实例
    """

def get_cached_storage(self, name: str, default_ttl: int = 3600) -> CachedStorage:
    """获取或创建缓存存储
    
    Args:
        name: 缓存名称
        default_ttl: 默认缓存时间（秒）
        
    Returns:
        缓存存储实例
    """
```

#### 清理和维护

```python
def cleanup_expired_caches(self) -> None:
    """清理所有过期缓存"""

def clear_all(self) -> None:
    """清空所有存储和缓存"""

def get_stats(self) -> dict[str, Any]:
    """获取存储统计信息"""
```

### StorageBackend 接口

所有存储后端都必须实现此接口。

#### 基本操作

```python
@abstractmethod
def get(self, key: str, default: Any = None) -> Any:
    """获取值
    
    Args:
        key: 键名
        default: 默认值（键不存在时返回）
        
    Returns:
        存储的值或默认值
    """

@abstractmethod
def set(self, key: str, value: Any) -> None:
    """设置值
    
    Args:
        key: 键名
        value: 要存储的值
    """

@abstractmethod
def delete(self, key: str) -> bool:
    """删除值
    
    Args:
        key: 键名
        
    Returns:
        是否成功删除
    """

@abstractmethod
def exists(self, key: str) -> bool:
    """检查键是否存在
    
    Args:
        key: 键名
        
    Returns:
        键是否存在
    """

@abstractmethod
def clear(self) -> None:
    """清空所有数据"""

@abstractmethod
def keys(self) -> list[str]:
    """返回所有键
    
    Returns:
        键列表
    """
```

#### 批量操作

```python
def get_many(self, keys: list[str]) -> dict[str, Any]:
    """批量获取多个值
    
    Args:
        keys: 键列表
        
    Returns:
        键值对字典
    """

def set_many(self, data: dict[str, Any]) -> None:
    """批量设置多个值
    
    Args:
        data: 键值对字典
    """

def delete_many(self, keys: list[str]) -> int:
    """批量删除多个值
    
    Args:
        keys: 键列表
        
    Returns:
        成功删除的数量
    """
```

### JSONFileBackend

JSON 文件存储后端，用于存储结构化数据。

#### 构造函数

```python
def __init__(self, file_path: str | Path):
    """初始化 JSON 文件存储后端
    
    Args:
        file_path: JSON 文件路径
    """
```

#### 使用示例

```python
from modular_dashboard.storage import JSONFileBackend
from pathlib import Path

# 创建存储后端
backend = JSONFileBackend("data.json")

# 存储数据
backend.set("user_preferences", {
    "theme": "dark",
    "language": "zh",
    "modules": ["arxiv", "github"]
})

# 获取数据
preferences = backend.get("user_preferences", {})

# 检查键是否存在
if backend.exists("user_preferences"):
    print("用户偏好设置已保存")
```

### PickleFileBackend

Pickle 文件存储后端，用于存储复杂对象。

#### 构造函数

```python
def __init__(self, file_path: str | Path):
    """初始化 Pickle 文件存储后端
    
    Args:
        file_path: Pickle 文件路径
    """
```

#### 使用示例

```python
from modular_dashboard.storage import PickleFileBackend
import datetime

# 创建存储后端
backend = PickleFileBackend("complex_data.pkl")

# 存储复杂对象
complex_data = {
    "timestamp": datetime.datetime.now(),
    "objects": [object(), object()],
    "nested": {"deep": {"data": "value"}}
}

backend.set("complex_data", complex_data)

# 获取数据
loaded_data = backend.get("complex_data")
```

### MemoryBackend

内存存储后端，用于临时数据存储。

#### 构造函数

```python
def __init__(self):
    """初始化内存存储后端"""
```

#### 使用示例

```python
from modular_dashboard.storage import MemoryBackend

# 创建内存存储
backend = MemoryBackend()

# 临时数据存储
backend.set("temp_session", {"user_id": 123, "token": "abc123"})

# 获取临时数据
session = backend.get("temp_session")
```

### CachedStorage

缓存存储，为其他存储后端添加缓存功能。

#### 构造函数

```python
def __init__(self, backend: StorageBackend, default_ttl: int = 3600):
    """初始化缓存存储
    
    Args:
        backend: 底层存储后端
        default_ttl: 默认缓存时间（秒）
    """
```

#### 缓存操作

```python
def set(self, key: str, value: Any, ttl: int | None = None) -> None:
    """设置缓存值
    
    Args:
        key: 键名
        value: 要缓存的值
        ttl: 缓存时间（秒），None 表示使用默认值
    """

def get(self, key: str, default: Any = None) -> Any:
    """获取缓存值（如果未过期）
    
    Args:
        key: 键名
        default: 默认值
        
    Returns:
        缓存的值或默认值
    """

def delete(self, key: str) -> bool:
    """删除缓存值
    
    Args:
        key: 键名
        
    Returns:
        是否成功删除
    """

def cleanup_expired(self) -> int:
    """清理过期缓存
    
    Returns:
        清理的缓存项数量
    """

def get_cache_info(self, key: str) -> dict[str, Any] | None:
    """获取缓存信息
    
    Args:
        key: 键名
        
    Returns:
        缓存信息字典或 None
    """
```

#### 使用示例

```python
from modular_dashboard.storage import JSONFileBackend, CachedStorage

# 创建底层存储
backend = JSONFileBackend("data.json")

# 创建缓存存储（1小时 TTL）
cache = CachedStorage(backend, default_ttl=3600)

# 使用缓存
cache.set("api_data", expensive_to_fetch_data)
cached_data = cache.get("api_data")

# 检查缓存状态
cache_info = cache.get_cache_info("api_data")
if cache_info:
    print(f"缓存创建时间: {cache_info['created_at']}")
    print(f"缓存过期时间: {cache_info['expires_at']}")
```

## 🎯 最佳实践

### 1. 模块存储管理

```python
class MyModule(Module):
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.storage = self.get_storage()
        self.cache = self.get_cache(default_ttl=1800)

    def save_user_preferences(self, preferences: dict[str, Any]) -> None:
        """保存用户偏好设置"""
        self.storage.set("user_preferences", preferences)

    def load_user_preferences(self) -> dict[str, Any]:
        """加载用户偏好设置"""
        return self.storage.get("user_preferences", {})
```

### 2. 缓存策略

```python
def fetch_with_cache(self) -> list[dict[str, Any]]:
    """带缓存的数据获取"""
    cache = self.get_cache(default_ttl=self.config.get("refresh_interval", 3600))
    
    # 尝试从缓存获取
    cached_data = cache.get("module_data")
    if cached_data:
        return cached_data
    
    # 获取新数据
    fresh_data = self._fetch_from_source()
    
    # 缓存数据
    cache.set("module_data", fresh_data)
    
    return fresh_data
```

### 3. 错误处理

```python
def safe_storage_operation(self) -> None:
    """安全的存储操作"""
    try:
        self.storage.set("important_data", data)
    except Exception as e:
        logger.error(f"存储操作失败: {e}")
        # 降级处理或使用备用存储
```

### 4. 性能优化

```python
def batch_operations(self) -> None:
    """批量操作优化"""
    data = {
        "key1": "value1",
        "key2": "value2", 
        "key3": "value3"
    }
    
    # 批量设置比多次设置更高效
    self.storage.set_many(data)
    
    # 批量获取
    values = self.storage.get_many(["key1", "key2", "key3"])
```

## 🔧 高级功能

### 1. 自定义存储后端

```python
from modular_dashboard.storage import StorageBackend
from typing import Any

class CustomStorageBackend(StorageBackend):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._data = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
    
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        return key in self._data
    
    def clear(self) -> None:
        self._data.clear()
    
    def keys(self) -> list[str]:
        return list(self._data.keys())
```

### 2. 存储监控

```python
def monitor_storage_usage(self) -> None:
    """监控存储使用情况"""
    storage_manager = get_storage_manager()
    stats = storage_manager.get_stats()
    
    print(f"总存储后端数: {stats['total_backends']}")
    print(f"总缓存实例数: {stats['total_caches']}")
    print(f"缓存命中率: {stats['cache_hit_rate']:.2%}")
```

### 3. 存储迁移

```python
def migrate_storage(self, old_backend: StorageBackend, new_backend: StorageBackend) -> None:
    """存储迁移"""
    # 获取所有数据
    all_data = {key: old_backend.get(key) for key in old_backend.keys()}
    
    # 迁移到新存储
    new_backend.set_many(all_data)
    
    # 验证数据完整性
    for key in all_data:
        assert new_backend.get(key) == all_data[key]
    
    # 清理旧存储
    old_backend.clear()
```

## 🆘 故障排除

### 常见问题

#### 1. 文件权限错误
```python
# 确保有文件写入权限
import os
data_dir = os.path.dirname(file_path)
os.makedirs(data_dir, exist_ok=True)
```

#### 2. 内存使用过高
```python
# 定期清理过期缓存
storage_manager = get_storage_manager()
storage_manager.cleanup_expired_caches()
```

#### 3. 数据损坏
```python
# 使用备份和验证
def safe_load(self, key: str):
    try:
        return self.storage.get(key)
    except Exception:
        # 尝试从备份恢复
        return self._load_from_backup(key)
```

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 监控存储操作
class LoggingStorageBackend(StorageBackend):
    def __init__(self, backend: StorageBackend):
        self.backend = backend
    
    def get(self, key: str, default: Any = None) -> Any:
        logger.debug(f"Storage get: {key}")
        return self.backend.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        logger.debug(f"Storage set: {key}")
        self.backend.set(key, value)
```

---

通过使用 Modular Dashboard 的存储系统，您可以轻松管理数据的持久化和缓存，提高应用性能和用户体验。