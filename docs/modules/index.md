# 内置模块索引

Modular Dashboard 提供了丰富的内置模块，涵盖数据源、工具、监控和娱乐等多个类别。每个模块都经过精心设计，提供完整的配置选项和用户界面。

## 📦 模块分类

### 🔍 数据源模块
这些模块从外部数据源获取信息，为用户提供实时的数据更新。

| 模块 | 功能 | 特点 |
|------|------|------|
| [ArXiv 模块](arxiv.md) | 学术论文搜索和展示 | 支持关键词搜索、作者筛选、PDF 链接 |
| [GitHub 模块](github.md) | GitHub 活动监控 | 支持个人动态、仓库监控、事件筛选 |
| [RSS 模块](rss.md) | RSS 订阅阅读器 | 支持多源订阅、内容预览、图片显示 |

### 🛠️ 工具模块
这些模块提供实用的工具功能，增强用户体验。

| 模块 | 功能 | 特点 |
|------|------|------|
| [时钟模块](clock.md) | 数字时钟和日期显示 | 支持多时区、格式自定义、秒数显示 |
| [天气模块](weather.md) | 天气信息展示 | 支持多城市、详细预报、多单位 |
| [待办事项模块](todo.md) | 任务管理和待办列表 | 支持优先级、分类、自动保存 |

### 📊 监控模块
这些模块用于监控各种系统和服务的状态。

| 模块 | 功能 | 特点 |
|------|------|------|
| [版本发布模块](releases.md) | 软件版本发布监控 | 支持多平台、版本过滤、发布说明 |
| [网站监控模块](monitor.md) | 网站可用性监控 | 支持响应时间、状态码、告警功能 |

### 🎮 娱乐模块
这些模块提供轻松娱乐的内容。

| 模块 | 功能 | 特点 |
|------|------|------|
| [动物图片模块](animals.md) | 随机动物图片展示 | 支持多种动物、尺寸调整、自动刷新 |

## 🚀 快速开始

### 启用模块

在配置文件中启用所需模块：

```json
{
  "modules": [
    {
      "id": "arxiv",
      "enabled": true,
      "config": {
        "keywords": ["machine learning", "AI"],
        "refresh_interval": 3600
      }
    },
    {
      "id": "github", 
      "enabled": true,
      "config": {
        "username": "your_username",
        "repositories": ["your_repo"]
      }
    }
  ]
}
```

### 布局配置

在布局中安排模块位置：

```json
{
  "layout": {
    "columns": 3,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "clock"]
      },
      {
        "width": "normal",
        "modules": ["github", "weather"]
      },
      {
        "width": "normal", 
        "modules": ["rss", "todo"]
      }
    ]
  }
}
```

## 🎯 推荐组合

### 开发者工作台
```json
{
  "modules": [
    {"id": "github", "enabled": true},
    {"id": "arxiv", "enabled": true},
    {"id": "releases", "enabled": true},
    {"id": "clock", "enabled": true},
    {"id": "todo", "enabled": true},
    {"id": "weather", "enabled": false}
  ]
}
```

### 信息阅读中心
```json
{
  "modules": [
    {"id": "rss", "enabled": true},
    {"id": "arxiv", "enabled": true},
    {"id": "animals", "enabled": true},
    {"id": "clock", "enabled": true}
  ]
}
```

### 系统监控台
```json
{
  "modules": [
    {"id": "monitor", "enabled": true},
    {"id": "releases", "enabled": true},
    {"id": "weather", "enabled": true},
    {"id": "clock", "enabled": true}
  ]
}
```

## 🔧 模块开发

### 创建自定义模块

如果您需要的功能在内置模块中没有提供，可以开发自定义模块：

```python
from typing import Any
from nicegui import ui
from modular_dashboard.modules.base import Module

class CustomModule(Module):
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

    def render(self) -> None:
        items = self.fetch()
        with ui.card().classes("w-full"):
            ui.label(self.name).classes("text-lg font-semibold")
            for item in items[:3]:
                ui.label(item["title"]).classes("font-medium")
```

详细的模块开发指南请参考 [模块开发指南](../developer-guide/module-development.md)。

## 📊 模块统计

| 类别 | 模块数量 | 功能覆盖 |
|------|---------|---------|
| 数据源模块 | 3 | 学术、代码、资讯 |
| 工具模块 | 3 | 时间、天气、任务 |
| 监控模块 | 2 | 版本、网站 |
| 娱乐模块 | 1 | 图片、休闲 |
| **总计** | **9** | **全面覆盖** |

## 🔮 未来计划

### 计划中的模块
- **邮件模块** - 邮件收发和监控
- **日历模块** - 日程安排和提醒
- **股票模块** - 股票行情和财务信息
- **新闻模块** - 新闻聚合和推荐
- **系统监控** - 系统性能和资源监控

### 功能增强
- **模块市场** - 第三方模块分享和安装
- **模块联动** - 模块间的智能联动
- **AI 推荐** - 基于使用习惯的智能推荐

## 🆘 获取帮助

### 模块配置问题
1. **查看文档** - 详细阅读各模块的配置说明
2. **检查格式** - 确认 JSON 配置格式正确
3. **验证启用** - 检查模块是否已启用
4. **查看日志** - 检查应用日志中的错误信息

### 性能问题
1. **调整刷新间隔** - 合理设置 `refresh_interval`
2. **限制显示数量** - 设置 `max_results` 或 `show_limit`
3. **启用缓存** - 确保缓存功能正常工作
4. **网络优化** - 检查网络连接和代理设置

### 功能建议
- 💡 **功能建议**：[GitHub Discussions](https://github.com/WayneXuCN/ModularDashboard/discussions)
- 🐛 **问题反馈**：[GitHub Issues](https://github.com/WayneXuCN/ModularDashboard/issues)
- 📖 **文档改进**：直接编辑文档文件

---

通过合理组合和配置这些内置模块，您可以创建一个功能强大、个性化的仪表盘，满足各种使用场景的需求。