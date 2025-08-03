# 开发指南

本指南为想要为 Research Dashboard 做贡献的开发者提供信息。

## 概述

Research Dashboard 使用 Python 构建，使用 NiceGUI 作为 Web 界面。它遵循模块化架构，使得添加新的信息来源变得容易。

## 入门

1. 在 GitHub 上 fork 仓库
2. 本地克隆您的 fork
3. 使用 `uv lock` 和 `uv sync` 安装依赖
4. 使用 `uv run -m modular_dashboard.app` 运行应用程序

## 项目结构

```text
research-dashboard/
├── pyproject.toml              # 项目配置和依赖
├── README.md                   # 项目概述
├── LICENSE                     # 许可证信息
├── .gitignore                  # Git 忽略模式
├── mkdocs.yml                  # 文档配置
│
├── src/
│   └── modular_dashboard/     # 主要源代码
│       ├── __init__.py
│       ├── __main__.py         # 应用程序入口点
│       ├── app.py              # 主应用程序逻辑
│       │
│       ├── config/             # 配置管理
│       │   ├── manager.py      # 配置加载/保存
│       │   └── schema.py       # 配置数据类
│       │
│       ├── modules/            # 模块系统
│       │   ├── base.py         # 模块基类
│       │   ├── registry.py     # 模块注册表
│       │   │
│       │   ├── arxiv/          # ArXiv 模块
│       │   │   └── module.py
│       │   │
│       │   ├── github/         # GitHub 模块
│       │   │   └── module.py
│       │   │
│       │   └── rss/            # RSS 模块
│       │       └── module.py
│       │
│       ├── ui/                 # 用户界面组件
│       │   └── dashboard.py    # 仪表盘 UI
│       │
│       ├── static/             # 静态资源
│       │   └── css/
│       │       └── style.css
│       │
│       ├── utils/              # 实用函数
│       │   └── logger.py
│       │
│       ├── assets/             # 应用程序资源
│       │   ├── default-config.json
│       │   └── img/
│       │       └── favicon.ico
│       │
│       └── docs/               # 文档生成器
│           └── generator.py
│
├── config/                     # 用户配置（运行时）
│
├── scripts/                    # 实用脚本
│   ├── create_icon.py
│   └── generate_docs.py
│
├── tests/                      # 测试（计划中）
│
├── docs/                       # 文档源
│   ├── README.md
│   ├── overview.md
│   ├── api/
│   ├── development/
│   ├── modules/
│   └── user-guide/
│
└── dist/                       # 构建输出
```

## 代码风格

Research Dashboard 遵循 Python PEP 8 风格指南。代码使用 `ruff` 自动格式化：

```bash
uv run ruff format .
```

代码也使用 `ruff` 检查风格和正确性：

```bash
uv run ruff check .
```

## 测试

测试功能正在规划中，将来会使用 `pytest`。

## 文档

文档使用 Markdown 编写，用 MkDocs 构建。要构建文档：

```bash
mkdocs build
```

要在本地提供文档服务：

```bash
mkdocs serve
```

文档组织成几个部分：

- 用户指南：面向最终用户
- 模块：有关每个模块的信息
- API 参考：面向扩展应用程序的开发者
- 开发：面向贡献者

## 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 如果适用，添加测试
5. 更新文档
6. 使用 `ruff format` 格式化代码
7. 使用 `ruff check` 检查代码
8. 提交更改
9. 推送到您的 fork
10. 创建拉取请求

## 报告问题

如果您发现 bug 或有功能请求，请在 GitHub 上提交 issue，并包含：

1. 清晰的标题
2. 详细描述
3. 重现步骤（对于 bug）
4. 预期和实际行为（对于 bug）
5. 系统信息（操作系统、Python 版本等）

## 行为准则

请注意，该项目发布了贡献者行为准则。通过参与此项目，您同意遵守其条款。
