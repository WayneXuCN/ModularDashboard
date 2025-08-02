# 📄 信息速览 Dashboard  

> **项目名称**：`Research Dashboard`  
> **定位**：面向科研人员的本地化、模块化、可扩展信息聚合仪表盘  
> **核心原则**：极简、高效、可配置、离线优先、隐私安全

---

## 项目愿景

为科研人员提供一个**每日工作第一入口**的桌面级应用，通过高度可定制的卡片式布局，聚合来自 arXiv、GitHub、RSS、日历等多源信息，实现"一眼掌握学术动态"的体验。

- ✅ **非操作平台**：只展示，不操作（点击跳转原站）
- ✅ **本地运行**：无账户、无云端同步，配置文件本地存储
- ✅ **可扩展**：模块通过 JSON 配置定义，支持第三方开发
- ✅ **跨平台**：支持 macOS / Windows / Linux
- ✅ **可迁移**：支持导出/导入配置，实现多设备复现

---

## 核心需求

| 类别 | 需求 |
|------|------|
| 🔹 基础功能 | - 首页为响应式卡片网格布局<br>- 支持自由拖拽排序、折叠/展开、列数切换<br>- 支持暗色/亮色主题 |
| 🔹 模块系统 | - 模块可插拔（arXiv / GitHub / RSS / Calendar / Scholar）<br>- 每个模块可独立配置刷新频率<br>- 模块数据通过 Python 脚本抓取 |
| 🔹 数据源 | - arXiv：按关键词自动获取最新论文<br>- GitHub：展示关注仓库、个人活动<br>- RSS：解析用户订阅源<br>- 日历：同步本地/Google Calendar（只读）<br>- 学术指标：Google Scholar 引用变化（未来） |
| 🔹 交互 | - 卡片点击 → 跳转原链接或进入模块详情页<br>- 支持"全局刷新"按钮 + "下拉刷新"<br>- 不支持内嵌操作（如标记已读） |
| 🔹 配置管理 | - 所有配置以 JSON 文件存储<br>- 支持导出/导入 `user-config.json`<br>- 初始配置可通过 GUI 或手动编辑 |
| 🔹 跨平台 | - 打包为独立桌面应用（.app / .exe / .deb）<br>- 支持 Web 访问（开发时） |

---

## 🛠 技术栈

| 类别 | 技术 | 理由 |
|------|------|------|
| **项目管理** | `uv` | 现代化替代 `pip + venv`，速度快，依赖解析强 |
| **构建系统** | `hatchling` | 标准化构建，支持 `pyproject.toml`，兼容 PyPI |
| **应用框架** | `NiceGUI`（v3+） | Python 写 Web UI，支持 WebSocket、响应式、暗色模式 |
| **前端定制** | HTML/CSS/JS + `Tailwind CSS`（CDN） | 你熟悉前端，可精细控制 UI |
| **拖拽排序** | `SortableJS`（CDN） | 轻量、成熟、支持触摸设备 |
| **样式框架** | `Tailwind CSS`（CDN 引入） | 无需构建，原子类快速布局响应式网格 |
| **数据抓取** | `requests` + `feedparser` + `arxiv`（官方库） | 稳定、无额外依赖 |
| **定时任务** | `APScheduler`（异步） | 支持动态增删任务，适合模块独立刷新 |
| **配置存储** | JSON 文件系统（`config/user-config.json`） | 简单、可读、可迁移 |
| **日志** | `structlog` 或标准 `logging` | 结构化日志，便于调试 |

> ⚠️ **不使用数据库**：避免 SQLite 等引入复杂性，纯文件系统更轻量。

---

## 🚀 快速开始

### 安装依赖

```bash
# 使用 uv 安装依赖
uv pip install -e .
```

### 运行应用

```bash
# 以 Web 应用模式运行
uv run -m research_dashboard

# 以原生桌面应用模式运行
uv run -m research_dashboard --native
```

### 打包为桌面应用（macOS）

```bash
# 创建 macOS 应用程序包
uv run scripts/package.py
```

打包后的应用将位于 `dist/ResearchDashboard.app`，可直接运行。

---

## 📁 项目结构

```
research-dashboard/
│
├── pyproject.toml             # uv + hatchling 配置
├── README.md                  # 项目说明、启动、打包指南
├── LICENSE
├── .gitignore                 # 忽略 config/、dist/、__pycache__/
│
├── src/
│   └── research_dashboard/
│       │
│       ├── __init__.py
│       ├── __main__.py        # 入口：`python -m research_dashboard`
│       ├── app.py             # 核心应用逻辑（NiceGUI 页面定义）
│       │
│       ├── config/
│       │   ├── __init__.py
│       │   ├── manager.py     # load_config(), save_config(), export/import
│       │   └── schema.py      # 配置结构定义（Python 类型提示 + JSON Schema 输出）
│       │
│       ├── modules/
│       │   ├── __init__.py
│       │   ├── base.py        # Module 抽象基类（定义接口）
│       │   ├── registry.py    # 模块注册表（自动发现或手动注册）
│       │   │
│       │   ├── arxiv/
│       │   │   ├── __init__.py
│       │   │   ├── module.py  # ArxivModule 实现
│       │   │   └── fetcher.py # 数据抓取逻辑
│       │   │
│       │   ├── github/
│       │   │   ├── __init__.py
│       │   │   ├── module.py
│       │   │   └── fetcher.py
│       │   │
│       │   ├── rss/
│       │   │   ├── __init__.py
│       │   │   ├── module.py
│       │   │   └── fetcher.py
│       │   │
│       │   └── ...            # 其他模块（calendar, scholar 等）
│       │
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── dashboard.py   # 主页布局、卡片渲染
│       │   ├── components.py  # 通用 UI 组件（卡片、标题栏、刷新按钮）
│       │   └── templates.py   # 可选：HTML 模板字符串（避免文件碎片）
│       │
│       ├── static/
│       │   ├── css/
│       │   │   └── style.css  # 自定义样式（覆盖 Tailwind）
│       │   ├── js/
│       │   │   └── drag.js    # SortableJS 初始化脚本
│       │   └── icons/         # SVG 图标（模块专用）
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── scheduler.py   # APScheduler 管理（add/remove job）
│       │   ├── logger.py      # 日志配置
│       │   └── helpers.py     # 工具函数（时间格式化、链接安全检查等）
│       │
│       └── assets/
│           ├── default-config.json  # 默认配置模板
│           └── modules.json         # 模块元信息（名称、图标、描述）
│
├── config/                    # 用户配置（运行时生成，.gitignore）
│   └── user-config.json
│
├── scripts/
│   └── package.py             # 打包脚本
│
├── tests/                     # 可选：测试用例
│   ├── test_config.py
│   └── test_modules.py
│
└── dist/                      # 打包输出（.gitignore）
```

---

## 🔧 关键设计决策说明

### 1. **模块目录结构**：`modules/arxiv/module.py` 而非 `modules/arxiv.py`

- ✅ 为未来支持**多文件模块**预留空间（如 `fetcher.py`, `parser.py`, `ui.py`）
- ✅ 支持模块内测试、文档独立管理
- ✅ 避免单文件过大，便于维护

### 2. **配置管理**：`config/schema.py` 定义结构

```python
# config/schema.py
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
```

- ✅ 提供类型提示，IDE 自动补全
- ✅ 可生成 JSON Schema 用于配置校验
- ✅ 避免 `dict` 嵌套过深导致错误

### 3. **模块注册机制**：`modules/registry.py`

```python
# modules/registry.py
from .base import Module
from .arxiv.module import ArxivModule
from .github.module import GithubModule
from .rss.module import RssModule

# 注册表（未来可支持插件发现）
MODULE_REGISTRY = {
    'arxiv': ArxivModule,
    'github': GithubModule,
    'rss': RssModule,
}

def get_module_class(module_id: str) -> type[Module]:
    return MODULE_REGISTRY.get(module_id)
```

- ✅ 避免在 `app.py` 中硬编码导入
- ✅ 未来支持动态加载第三方模块（如从 `plugins/` 目录）

### 4. **入口文件**：`__main__.py`

```python
# src/research_dashboard/__main__.py
from .app import run_app
if __name__ == "__main__":
    run_app()
```

- ✅ 支持 `python -m research_dashboard` 启动
- ✅ 避免路径导入问题

### 5. **静态资源**：CDN 优先，本地回退

```html
<!-- 在 NiceGUI 中引入 -->
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4/dist/tailwind.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
```

- ✅ 减少打包体积
- ✅ 可本地缓存，未来支持离线模式

---

## 🧩 模块开发规范

每个模块必须实现：

```python
# modules/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Module(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def icon(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """
        返回标准化条目列表，格式：
        [
          {
            "title": str,
            "summary": str,
            "link": str,
            "published": str (ISO8601),
            "tags": List[str],
            "extra": Dict  # 可选字段
          }
        ]
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        使用 NiceGUI 或 HTML 渲染主页上的模块卡片
        默认只显示摘要信息
        """
        pass

    def render_detail(self) -> None:
        """
        使用 NiceGUI 或 HTML 渲染模块的详细页面
        可以显示更完整的信息
        默认实现调用 render() 方法
        """
        self.render()
```

### 模块页面导航

Research Dashboard 为每个模块自动创建了详细页面，可通过 `/module/{module_id}` 访问。
用户可以通过点击主页上的模块卡片进入详细页面。

在详细页面中，模块可以展示比主页更丰富的信息，例如：

- 完整的文章摘要而不是截断的版本
- 更多的标签和分类信息
- 附加的元数据（如作者、来源等）
- 更多的交互元素
