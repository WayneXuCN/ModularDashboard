<div align="center">

# 模块化仪表盘

<!-- Project Status & Release -->
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/WayneXuCN/ModularDashboard?label=latest%20release)](https://github.com/WayneXuCN/ModularDashboard/releases)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/WayneXuCN/ModularDashboard?label=latest%20tag)](https://github.com/WayneXuCN/ModularDashboard/tags)
[![Documentation Status](https://img.shields.io/badge/docs-available-brightgreen)](https://waynexucn.github.io/ModularDashboard/)
[![GitHub last commit](https://img.shields.io/github/last-commit/WayneXuCN/ModularDashboard)](https://github.com/WayneXuCN/ModularDashboard/commits/main)

<!-- Community & Activity -->
[![GitHub stars](https://img.shields.io/github/stars/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/WayneXuCN/ModularDashboard?style=social)](https://github.com/WayneXuCN/ModularDashboard/watchers)

</div>

<div align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a>
</div>

一个现代化、模块化、可扩展的信息聚合仪表盘应用，将来自多个来源的信息聚合到一个可自定义的界面中。

## 🌟 概述

模块化仪表盘是一个本地化、模块化、可扩展的信息聚合仪表盘项目，旨在为用户提供一个**每日信息第一入口**的桌面级应用。通过高度可定制的卡片式布局，聚合来自多种数据源的动态信息，实现信息一目了然。

## 🚀 核心特性

- **模块化架构**：基于插件的模块系统，支持动态加载和扩展
- **现代化UI**：响应式用户界面，支持亮色/暗色主题，基于 [NiceGUI](https://nicegui.io)
- **灵活布局**：可配置的单列、双列或三列布局
- **丰富的模块生态系统**：内置多种数据源模块
- **智能存储**：多后端存储系统，支持缓存和数据持久化
- **跨平台**：支持以Web应用和原生桌面应用两种模式运行
- **高度可配置**：基于JSON的配置文件，支持实时更新

## 🧩 可用模块

<div align="center">

| 模块 | 图标 | 描述 | 数据源 | 更新频率 | 可定制性 |
|------|------|------|--------|----------|----------|
| **时钟** | 🕐 | 实时时间显示，支持自定义时间格式 | 系统时间 | 实时 | ✅ 格式、时区 |
| **天气** | ☁️ | 显示您所在位置的天气信息 | 天气API | 每小时 | ✅ 位置、单位 |
| **待办事项** | 📝 | 简单的任务管理，支持数据持久化 | 本地存储 | 手动 | ✅ 分类、优先级 |
| **学术论文** | 📚 | 根据您的兴趣获取最新研究论文 | ArXiv API | 每日 | ✅ 关键词、分类 |
| **动物图片** | 🐱 | 可爱的动物图片，为您的日常增添乐趣 | 随机API | 刷新时 | ✅ 动物类型 |
| **RSS订阅** | 📡 | RSS订阅阅读器，支持您喜爱的信息源 | RSS源 | 可配置 | ✅ 订阅源、刷新率 |
| **GitHub活动** | 🐙 | GitHub活动跟踪，支持用户和仓库 | GitHub API | 每小时 | ✅ 用户、仓库、事件 |
| **软件发布** | 📦 | 最新软件版本跟踪 | GitHub Releases | 每日 | ✅ 仓库选择 |
| **时间进度** | 📊 | 可视化日、月、年的时间进度 | 系统时间 | 实时 | ✅ 周期选择 |

</div>

### 模块特性

- **🔄 自动刷新**: 所有模块都支持可配置的自动更新
- **💾 智能缓存**: 智能缓存系统减少API调用并提升性能
- **🎨 主题适配**: 一致的视觉设计，适配亮色/暗色主题
- **⚙️ 配置化**: 基于JSON的配置，便于自定义
- **🔧 可扩展**: 插件架构允许轻松添加新模块

### 核心依赖

```python
# 核心框架
nicegui>=2.0.0                 # 现代化Web UI框架
pywebview>=5.0                 # 桌面应用包装器

# 数据获取与处理
httpx>=0.25.0                  # 异步HTTP客户端
requests>=2.25.0               # HTTP库
beautifulsoup4>=4.9.0          # HTML/XML解析器
feedparser>=6.0.0              # RSS/Atom订阅解析器
arxiv>=2.0.0                   # ArXiv API客户端

# 任务管理与日志
APScheduler>=3.0.0             # 后台任务调度器
loguru>=0.7.0                  # 结构化日志
structlog>=25.0.0              # 结构化日志框架

# 开发与文档
mkdocs-material>=9.0.0         # 文档主题
pytest>=6.0.0                  # 测试框架
black                          # 代码格式化工具
mypy                           # 类型检查
```

## 📦 安装

### 环境要求

- Python 3.12 或更高版本
- [uv 包管理器](https://docs.astral.sh/uv/) (推荐)

### 快速开始

1. **克隆项目**

   ```bash
   git clone https://github.com/WayneXuCN/ModularDashboard.git
   cd ModularDashboard
   ```

2. **安装依赖**

   ```bash
   # 使用 uv (推荐)
   uv sync
   
   # 或使用 pip
   pip install -e .
   ```

3. **运行应用**

   ```bash
   # 以 Web 应用模式运行
   uv run -m modular_dashboard.app
   
   # 以原生桌面应用模式运行
   uv run -m modular_dashboard.app --native
   ```

## ⚙️ 配置

模块化仪表盘使用 JSON 配置文件进行自定义。首次运行时，应用会在系统配置目录中创建默认配置：

- **Windows**: `%APPDATA%\modular_dashboard\config.json`
- **macOS/Linux**: `~/.modular_dashboard/config.json`

您可以自定义：

- 布局 (1-3列，不同模块排列)
- 主题 (亮色/暗色)
- 模块特定设置
- 启用/禁用模块

## 🧪 开发

### 搭建开发环境

```bash
# 克隆并进入项目目录
git clone https://github.com/WayneXuCN/ModularDashboard.git
cd ModularDashboard

# 安装带开发工具的依赖
uv sync --extra dev

# 运行测试
uv run pytest
```

### 项目结构

```
ModularDashboard/
├── src/modular_dashboard/          # 主应用代码
│   ├── app.py                      # 应用入口
│   ├── config/                     # 配置管理
│   ├── modules/                    # 模块系统
│   ├── ui/                         # UI 组件
│   ├── storage.py                  # 存储系统
│   └── utils/                      # 工具函数
├── config/                         # 示例配置
├── docs/                           # 文档
├── scripts/                        # 辅助脚本
└── pyproject.toml                  # 项目配置
```

### 创建自定义模块

要创建自定义模块，请扩展 [Module](src/modular_dashboard/modules/base.py) 基类：

```python
from modular_dashboard.modules.base import Module

class MyCustomModule(Module):
    @property
    def id(self) -> str:
        return "my_module"
    
    @property
    def name(self) -> str:
        return "我的自定义模块"
    
    @property
    def icon(self) -> str:
        return "custom_icon"
    
    @property
    def description(self) -> str:
        return "我的模块的功能描述"
    
    def fetch(self) -> list[dict[str, Any]]:
        # 从数据源获取数据
        return [
            {
                "title": "项目标题",
                "summary": "简要描述",
                "link": "https://example.com",
                "published": "2023-01-01T00:00:00Z",
                "tags": ["标签1", "标签2"]
            }
        ]
    
    def render(self) -> None:
        # 使用 NiceGUI 组件渲染模块 UI
        ui.label("来自我的自定义模块的问候！")
```

在 [registry.py](src/modular_dashboard/modules/registry.py) 中注册你的模块：

```python
from .my_module.module import MyCustomModule

MODULE_REGISTRY = {
    # ... 其他模块
    "my_module": MyCustomModule,
}
```

## 📚 文档

详细文档请查看 [docs](docs/) 目录，或运行：

```bash
uv run mkdocs serve
```

然后在浏览器中访问 <http://localhost:8000。>

## 🗺️ 发展路线图

### 当前版本 (v0.1.x)

- [x] 核心模块化架构
- [x] 基础模块生态系统（时钟、天气、待办等）
- [x] 基于JSON的配置系统
- [x] 亮色/暗色主题支持
- [x] 桌面和Web部署选项

### 下一版本 (v0.2.x)

- [ ] **增强模块系统**
  - [ ] 模块市场/商店
  - [ ] 热模块重载
  - [ ] 模块依赖管理
- [ ] **用户体验**
  - [ ] 拖拽式布局编辑器
  - [ ] 模块搜索和过滤
  - [ ] 键盘快捷键
- [ ] **数据与安全**
  - [ ] 加密数据存储选项
  - [ ] 多用户支持
  - [ ] 云端同步

### 未来版本 (v0.3.x+)

- [ ] **高级功能**
  - [ ] AI驱动的内容推荐
  - [ ] 与流行服务集成（Notion、Slack等）
  - [ ] 移动端配套应用
- [ ] **企业功能**
  - [ ] 团队/组织仪表盘
  - [ ] 基于角色的访问控制
  - [ ] 分析和报告
- [ ] **平台扩展**
  - [ ] 浏览器扩展
  - [ ] Docker容器部署
  - [ ] 云端托管选项

> 📢 **想要为这些目标做出贡献？** 查看我们的[贡献指南](docs/development/contributing.md)并加入我们的社区！

## 🤝 贡献

欢迎贡献！请阅读我们的 [贡献指南](docs/development/contributing.md) 了解如何提交拉取请求、报告问题或请求功能。

我们特别欢迎以下方面的贡献：

- 针对不同数据源的新模块
- UI/UX 改进
- 性能优化
- 文档增强
- Bug 修复

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
