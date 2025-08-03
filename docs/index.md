# Modular Dashboard

<div align="center">

![Modular Dashboard Logo](assets/images/logo.png)

**一个现代化的模块化仪表盘系统**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/WayneXuCN/ModularDashboard/actions)

[快速开始](getting-started.md) • [用户指南](user-guide/index.md) • [开发者指南](developer-guide/index.md) • [API 参考](api-reference/index.md)

</div>

## 🎯 项目简介

Modular Dashboard 是一个基于 Python 和 NiceGUI 的现代化模块化仪表盘系统。它采用插件化架构，支持动态加载各种功能模块，为用户提供个性化的信息聚合和工作台解决方案。

### ✨ 核心特性

- 🎨 **现代化 UI**：基于 NiceGUI 的响应式用户界面
- 🔧 **模块化架构**：支持动态加载和扩展功能模块
- 💾 **智能存储**：多后端存储系统，支持缓存和数据持久化
- ⚙️ **灵活配置**：JSON 格式的配置文件，支持实时配置更新
- 🌐 **多平台支持**：支持 Web 应用和原生桌面应用两种运行模式

### 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/WayneXuCN/ModularDashboard.git
cd ModularDashboard

# 安装依赖
uv sync

# 启动应用
uv run -m modular_dashboard.app
```

访问 [http://localhost:8080](http://localhost:8080) 即可使用。

### 📚 文档导航

#### 📖 用户指南
- [安装指南](user-guide/installation.md) - 系统要求和安装步骤
- [配置管理](user-guide/configuration.md) - 配置文件详解和最佳实践
- [布局配置](user-guide/layout.md) - 仪表盘布局和界面定制
- [模块使用](user-guide/modules.md) - 内置模块的使用方法

#### 🔧 开发者指南
- [架构设计](developer-guide/architecture.md) - 系统架构和技术原理
- [模块开发](developer-guide/module-development.md) - 开发自定义模块的完整指南
- [项目结构](developer-guide/project-structure.md) - 代码结构和文件组织
- [贡献指南](developer-guide/contributing.md) - 参与项目开发的方法

#### 📚 API 参考
- [模块基类](api-reference/module-base.md) - 核心模块接口和基类
- [配置 API](api-reference/configuration.md) - 配置管理相关接口
- [存储 API](api-reference/storage.md) - 存储和缓存系统接口

#### 🎯 内置模块
- [ArXiv 模块](modules/arxiv.md) - 学术论文搜索和展示
- [GitHub 模块](modules/github.md) - GitHub 活动监控
- [RSS 模块](modules/rss.md) - RSS 订阅阅读器
- [天气模块](modules/weather.md) - 天气信息展示
- [待办事项](modules/todo.md) - 任务管理和待办列表

### 🛠️ 技术栈

- **后端框架**：Python 3.12+
- **UI 框架**：NiceGUI 2.0+
- **包管理**：UV
- **数据存储**：JSON/Pickle 文件存储
- **网络请求**：HTTPX、Requests
- **任务调度**：APScheduler
- **日志系统**：Structlog、Loguru

### 🏗️ 系统架构

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

### 🎨 界面预览

![Dashboard Preview](assets/images/dashboard-preview.png)

### 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

### 🤝 参与贡献

欢迎贡献代码、报告问题或提出改进建议！

- 查看 [贡献指南](developer-guide/contributing.md)
- 提交 [Issue](https://github.com/WayneXuCN/ModularDashboard/issues)
- 创建 [Pull Request](https://github.com/WayneXuCN/ModularDashboard/pulls)

---

<div align="center">

**Made with ❤️ by Wayne Xu**

[GitHub](https://github.com/WayneXuCN) • [Website](https://waynexucn.github.io) • [Email](mailto:wenjie.xu.cn@outlook.com)

</div>