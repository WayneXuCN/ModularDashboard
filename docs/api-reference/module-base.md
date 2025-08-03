# 模块基类

`Module` 基类为 Research Dashboard 中的所有模块提供了基础。

## 概述

Research Dashboard 中的所有模块都继承自抽象的 `Module` 基类。这确保了一致的接口，并使得向系统添加新模块变得容易。

## 类定义

```python
class Module(ABC):
    def __init__(self, config: dict[str, Any] | None = None):
        """
        使用可选配置初始化模块。

        参数:
            config: 包含模块特定配置的可选字典
        """
        self.config = config or {}

    @property
    @abstractmethod
    def id(self) -> str:
        """模块的唯一标识符。"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """模块的人类可读名称。"""
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """模块的图标（例如，表情符号或 SVG 路径）。"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """模块功能的描述。"""
        pass

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """
        从源获取数据并返回标准化项目。

        返回:
            项目列表，每个项目包含以下键：
            - title (str): 项目标题
            - summary (str): 简要描述
            - link (str): 完整项目的 URL
            - published (str): ISO8601 格式的日期
            - tags (List[str]): 可选标签
            - extra (Dict): 可选额外字段
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        使用 NiceGUI 组件渲染模块的 UI。
        """
        pass

    def render_detail(self) -> None:
        """
        渲染模块的详细视图页面。
        默认情况下，它显示与主视图相同的内容，
        但模块可以覆盖此方法以提供更详细的展示。
        """
        self.render()
```

## 必需属性

所有模块都必须实现以下属性：

### id

模块的唯一标识符。这应该是一个短小的、小写的、无空格的字符串。

### name

模块的人类可读名称。这将在 UI 中显示。

### icon

模块的图标。这可以是一个表情符号或 SVG 路径。

### description

模块功能的简要描述。这将在 UI 中显示。

## 必需方法

所有模块都必须实现以下方法：

### fetch

从模块的数据源获取数据并返回标准化项目列表。

每个项目应该是一个包含以下键的字典：

- `title` (str): 项目标题
- `summary` (str): 简要描述
- `link` (str): 完整项目的 URL
- `published` (str): ISO8601 格式的日期
- `tags` (List[str]): 可选标签
- `extra` (Dict): 可选额外字段

### render

为仪表盘主视图渲染模块的 UI，使用 NiceGUI 组件。

### render_detail

为详细视图页面渲染模块的 UI。默认情况下，这会调用 `render()`，但模块可以覆盖此方法以提供更详细的展示。

## 可选方法

模块可以根据需要实现其他方法以满足其特定功能。

## 示例实现

这是一个模块实现的最小示例：

```python
from typing import Any
from nicegui import ui
from .base import Module

class ExampleModule(Module):
    @property
    def id(self) -> str:
        return "example"

    @property
    def name(self) -> str:
        return "示例模块"

    @property
    def icon(self) -> str:
        return "📝"

    @property
    def description(self) -> str:
        return "示例模块实现"

    def fetch(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "示例项目",
                "summary": "这是一个示例项目",
                "link": "https://example.com",
                "published": "2023-01-01T00:00:00Z",
                "tags": ["example"],
                "extra": {}
            }
        ]

    def render(self) -> None:
        items = self.fetch()
        if items:
            item = items[0]
            ui.label(item["title"])
            ui.link("查看详情", target=f"/module/{self.id}")

    def render_detail(self) -> None:
        items = self.fetch()
        for item in items:
            with ui.card():
                ui.label(item["title"]).classes("text-xl")
                ui.label(item["summary"])
                ui.link("查看完整项目", target=item["link"])
```

## 最佳实践

在实现模块时：

1. 使用 `fetch` 方法将数据获取与 UI 渲染分离
2. 在 `fetch` 中实现缓存以避免过多的 API 调用
3. 使用类型提示以获得更好的代码文档和 IDE 支持
4. 优雅地处理错误，特别是在 `fetch` 中
5. 保持 `render` 实现轻量级以用于仪表盘主视图
6. 在 `render_detail` 中提供详细视图
7. 遵循现有的代码风格和约定