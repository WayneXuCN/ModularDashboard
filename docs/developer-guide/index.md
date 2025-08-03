# 开发者指南

欢迎来到 Modular Dashboard 开发者指南！本章节为开发者提供详细的技术文档，帮助您理解系统架构、开发自定义模块以及参与项目贡献。

## 📚 章节内容

### 🏗️ 系统架构

#### [架构设计](architecture.md)
- 系统整体架构
- 核心组件说明
- 模块系统原理
- 技术选型分析

#### [项目结构](project-structure.md)
- 代码目录结构
- 文件组织规范
- 模块文件说明
- 开发环境设置

### 🔧 模块开发

#### [模块开发指南](module-development.md)
- 模块基础概念
- 模块基类介绍
- 开发步骤详解
- 最佳实践和模式
- 测试和调试

### 🤝 贡献指南

#### [贡献指南](contributing.md)
- 开发环境设置
- 代码提交规范
- 测试要求
- 文档编写
- 发布流程

## 🎯 学习路径

### 新手开发者
1. 阅读 [架构设计](architecture.md) 了解系统整体
2. 学习 [项目结构](project-structure.md) 熟悉代码组织
3. 按照 [模块开发指南](module-development.md) 开发第一个模块

### 经验开发者
1. 深入理解模块系统和 API
2. 学习高级特性和最佳实践
3. 参与 [贡献指南](contributing.md) 为项目做贡献

### 核心开发者
1. 参与架构设计和决策
2. 负责重要功能开发
3. 指导和帮助其他开发者

## 🛠️ 开发工具

### 必需工具
- **Python 3.12+** - 主要开发语言
- **UV** - 包管理和虚拟环境
- **Git** - 版本控制
- **VS Code** - 推荐的代码编辑器

### 推荐插件
- **Python 扩展** - Python 语言支持
- **Pylance** - Python 类型检查
- **GitLens** - Git 增强功能
- **Material Theme** - UI 主题

### 调试工具
- **内置调试器** - VS Code 调试功能
- **日志系统** - Structlog 日志记录
- **性能监控** - 应用性能分析

## 📝 开发规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用类型注解提高代码可读性
- 编写清晰的文档字符串
- 保持函数和类的单一职责

### 测试要求
- 单元测试覆盖率 > 80%
- 集成测试覆盖核心功能
- 测试代码遵循 AAA 模式
- 使用 pytest 测试框架

### 文档要求
- 所有公共 API 需要文档字符串
- 重要的设计决策需要文档说明
- 更新相关文档和示例
- 提供使用示例和最佳实践

## 🔄 开发流程

### 1. 环境设置
```bash
# 克隆项目
git clone https://github.com/WayneXuCN/ModularDashboard.git
cd ModularDashboard

# 创建虚拟环境
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 安装依赖
uv sync

# 安装开发依赖
uv sync --group dev
```

### 2. 开发新功能
```bash
# 创建功能分支
git checkout -b feature/your-feature-name

# 开发代码...
# 编写测试...
# 更新文档...

# 提交更改
git add .
git commit -m "feat: add your new feature"

# 推送分支
git push origin feature/your-feature-name
```

### 3. 测试和验证
```bash
# 运行单元测试
uv run pytest

# 运行集成测试
uv run pytest tests/integration/

# 检查代码质量
uv run ruff check
uv run mypy .
```

## 🎯 核心概念

### 模块系统
- **Module 基类** - 所有模块的基类
- **ExtendedModule** - 扩展功能基类
- **模块注册** - 模块发现和加载机制
- **生命周期** - 模块的初始化、运行和清理

### 配置系统
- **配置管理器** - 配置文件的读取和写入
- **配置验证** - 配置格式和有效性检查
- **配置迁移** - 版本升级时的配置迁移
- **环境变量** - 动态配置支持

### 存储系统
- **存储后端** - 多种存储实现（JSON、Pickle、内存）
- **缓存系统** - 智能缓存和过期机制
- **数据管理** - 数据的持久化和恢复
- **存储管理器** - 统一的存储接口

## 📚 API 参考

详细的 API 文档请参考 [API 参考](../api-reference/index.md) 章节，包含：

- 模块基类接口
- 配置管理 API
- 存储系统 API
- 工具函数和常量

## 🆘 获取帮助

### 技术支持
- 📖 [API 文档](../api-reference/index.md)
- 🐛 [问题反馈](https://github.com/WayneXuCN/ModularDashboard/issues)
- 💬 [技术讨论](https://github.com/WayneXuCN/ModularDashboard/discussions)

### 开发资源
- 📦 [代码仓库](https://github.com/WayneXuCN/ModularDashboard)
- 📋 [项目看板](https://github.com/WayneXuCN/ModularDashboard/projects)
- 📊 [构建状态](https://github.com/WayneXuCN/ModularDashboard/actions)

## 🚀 参与贡献

我们欢迎各种形式的贡献：

- 💻 **代码贡献** - 新功能、bug 修复、性能优化
- 📖 **文档改进** - 文档修正、补充说明、翻译
- 🎨 **UI 改进** - 界面优化、用户体验提升
- 🧪 **测试覆盖** - 增加测试用例、提高测试质量
- 📋 **问题反馈** - 报告 bug、提出改进建议

详细的贡献指南请参考 [贡献指南](contributing.md)。

---

开始您的 Modular Dashboard 开发之旅吧！我们期待您的贡献。