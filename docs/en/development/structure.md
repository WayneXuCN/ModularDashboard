# Project Structure

本文档详细介绍了 Research Dashboard Project Structure。

## 根Table of Contents

```
research-dashboard/
├── pyproject.toml              # 项目Configuration和依赖
├── README.md                   # 项目Overview
├── LICENSE                     # 许可证信息
├── .gitignore                  # Git 忽略模式
├── mkdocs.yml                  # 文档Configuration
│
├── src/                        # 源代码
├── config/                     # 用户Configuration（运行时）
├── scripts/                    # 实用脚本
├── tests/                      # 测试（计划中）
├── docs/                       # 文档源
└── dist/                       # 构建输出
```

## 源代码Table of Contents

主要源代码在 `src/research_dashboard/` 中：

```
src/research_dashboard/
├── __init__.py
├── __main__.py         # 应用程序入口点
├── app.py              # 主应用程序逻辑
│
├── config/             # Configuration管理
│   ├── manager.py      # Configuration加载/保存
│   └── schema.py       # Configuration数据类
│
├── modules/            # Modules系统
│   ├── base.py         # Modules基类
│   ├── registry.py     # Modules注册表
│   │
│   ├── arxiv/          # ArXiv Modules
│   │   └── module.py
│   │
│   ├── github/         # GitHub Modules
│   │   └── module.py
│   │
│   └── rss/            # RSS Modules
│       └── module.py
│
├── ui/                 # 用户界面组件
│   └── dashboard.py    # 仪表盘 UI
│
├── static/             # 静态资源
│   └── css/
│       └── style.css
│
├── utils/              # 实用函数
│   └── logger.py
│
├── assets/             # 应用程序资源
│   ├── default-config.json
│   └── img/
│       └── favicon.ico
│
└── docs/               # 文档生成器
    └── generator.py
```

## Configuration

Configuration管理由 `config/` Table of Contents处理：

- `schema.py`：定义Configuration对象的数据类
- `manager.py`：处理Configuration的加载、保存和验证

默认Configuration存储在 `assets/default-config.json` 中，在首次运行时复制到用户的ConfigurationTable of Contents。

## Modules

Modules系统设计为可扩展：

- `base.py`：定义所有Modules的抽象基类
- `registry.py`：维护可用Modules的注册表
- 每个Modules都有自己的Table of Contents和 `module.py` 文件

当前实现的Modules：

- ArXiv：根据关键词获取论文
- GitHub：显示 GitHub Activity
- RSS：聚合 RSS Feeds

## UI

UI 使用 NiceGUI 构建：

- `dashboard.py`：包含渲染主仪表盘和Modules详细视图的函数
- 使用基于列的Layout System来灵活安排Modules

## 静态资源

静态资源包括：

- `static/css/style.css` 中的 CSS 样式
- `assets/` 中的图像和其他资源

## 文档

文档在 `docs/` Table of Contents中组织：

- `README.md`：主文档索引
- `overview.md`：项目Overview
- `api/`：API Reference
- `development/`：Development者文档
- `modules/`：Modules文档
- `user-guide/`：用户指南

## 脚本

实用脚本在 `scripts/` Table of Contents中：

- `create_icon.py`：创建应用程序图标
- `generate_docs.py`：生成文档（计划中）

## 测试

`tests/` Table of Contents为未来的测试实现保留。

## 分发

`dist/` Table of Contents包含应用程序的构建分发。