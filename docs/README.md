# Modular Dashboard 技术文档

## 概述

Modular Dashboard 是一个现代化的、模块化的信息聚合仪表盘系统，旨在为用户提供统一的信息入口界面。该系统采用插件化架构，支持多种数据源的集成，具有高度的可定制性和扩展性。

### 核心特性

- 🏗️ **模块化架构**：基于插件的模块系统，支持动态加载和扩展
- 🎨 **现代化UI**：基于 NiceGUI 的响应式用户界面，支持亮色/暗色主题
- 💾 **智能存储**：多后端存储系统，支持缓存和数据持久化
- ⚙️ **灵活配置**：JSON 格式的配置文件，支持实时配置更新
- 🌐 **多平台支持**：支持 Web 应用和原生桌面应用两种运行模式
- 🔌 **丰富扩展**：内置多种实用模块，支持第三方模块开发

### 技术栈

- **后端框架**：Python 3.12+
- **UI 框架**：NiceGUI 2.0+
- **数据存储**：JSON/Pickle 文件存储、内存缓存
- **网络请求**：HTTPX、Requests
- **任务调度**：APScheduler
- **日志系统**：Structlog、Loguru
- **文档系统**：MkDocs + Material

### 项目结构

```
ModularDashboard/
├── src/modular_dashboard/          # 主应用代码
│   ├── app.py                      # 应用入口和路由
│   ├── config/                     # 配置管理
│   │   ├── manager.py              # 配置文件管理
│   │   └── schema.py               # 配置数据模型
│   ├── modules/                    # 模块系统
│   │   ├── base.py                 # 模块基类
│   │   ├── extended.py             # 扩展模块基类
│   │   ├── registry.py             # 模块注册表
│   │   └── [具体模块]/             # 各功能模块
│   ├── ui/                         # 用户界面组件
│   │   ├── dashboard.py            # 仪表盘主界面
│   │   ├── layout.py               # 布局管理
│   │   └── [其他UI组件]/
│   ├── storage.py                  # 存储管理系统
│   └── utils/                      # 工具函数
├── config/                         # 用户配置文件
├── docs/                           # 文档目录
├── scripts/                        # 构建脚本
└── pyproject.toml                  # 项目配置
```

### 适用场景

- **个人工作台**：整合常用工具和信息源
- **研发监控**：系统集成和状态监控
- **信息聚合**：多源信息的统一展示
- **快速原型**：模块化应用的快速开发

### 版本信息

- **当前版本**：0.1.0
- **开发状态**：Alpha 阶段
- **兼容性**：Python 3.12+
- **许可证**：MIT License

---

## 快速开始

### 环境要求

- Python 3.12 或更高版本
- 操作系统：Windows、macOS、Linux
- 内存：推荐 4GB 以上
- 存储：至少 100MB 可用空间

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/WayneXuCN/ModularDashboard.git
   cd ModularDashboard
   ```

2. **安装依赖**
   ```bash
   # 使用 uv 包管理器（推荐）
   uv sync
   
   # 或使用 pip
   pip install -e .
   ```

3. **运行应用**
   ```bash
   # Web 应用模式
   uv run -m modular_dashboard.app
   
   # 原生桌面应用模式
   uv run -m modular_dashboard.app --native
   ```

4. **访问应用**
   - Web 模式：打开浏览器访问 `http://localhost:8080`
   - 桌面模式：应用会自动启动原生窗口

### 基本配置

应用首次运行时会自动创建默认配置文件。配置文件位置：

- **Windows**：`%APPDATA%\ModularDashboard\config.json`
- **macOS/Linux**：`~/.config/ModularDashboard/config.json`

### 下一步

- 阅读 [架构设计](./development/architecture.md) 了解系统架构
- 查看 [模块开发](./development/module-development.md) 学习如何开发自定义模块
- 参考 [配置指南](./user-guide/configuration.md) 进行高级配置
- 探索 [内置模块](./modules/) 了解可用的功能模块

---

## 目录结构

### 📚 用户指南

- [快速开始](./user-guide/getting-started.md) - 安装和基本使用
- [配置说明](./user-guide/configuration.md) - 配置文件详解
- [布局定制](./user-guide/layout.md) - 界面布局和主题
- [模块管理](./user-guide/module-management.md) - 模块的启用和配置

### 🔧 开发指南

- [架构设计](./development/architecture.md) - 系统架构和设计理念
- [模块开发](./development/module-development.md) - 开发自定义模块
- [API 参考](./development/api-reference.md) - 完整的 API 文档
- [贡献指南](./development/contributing.md) - 参与项目开发

### 📖 模块文档

- [核心模块](./modules/core/) - 基础功能模块
- [数据源模块](./modules/data-sources/) - 外部数据集成模块
- [工具模块](./modules/tools/) - 实用工具模块
- [第三方模块](./modules/third-party/) - 社区贡献模块

### 🛠️ 技术文档

- [存储系统](./technical/storage.md) - 数据存储和缓存机制
- [配置系统](./technical/configuration.md) - 配置管理实现
- [UI 组件](./technical/ui-components.md) - 用户界面组件库
- [性能优化](./technical/performance.md) - 性能优化指南

### 📄 附录

- [常见问题](./appendix/faq.md) - 常见问题解答
- [故障排除](./appendix/troubleshooting.md) - 问题诊断和解决
- [更新日志](./appendix/changelog.md) - 版本更新记录
- [词汇表](./appendix/glossary.md) - 技术术语解释