# 项目结构

本文档详细介绍了 Research Dashboard 项目结构。

## 根目录

```
research-dashboard/
├── pyproject.toml              # 项目配置和依赖
├── README.md                   # 项目概述
├── LICENSE                     # 许可证信息
├── .gitignore                  # Git 忽略模式
├── mkdocs.yml                  # 文档配置
│
├── src/                        # 源代码
├── config/                     # 用户配置（运行时）
├── scripts/                    # 实用脚本
├── tests/                      # 测试（计划中）
├── docs/                       # 文档源
└── dist/                       # 构建输出
```

## 源代码目录

主要源代码在 `src/research_dashboard/` 中：

```
src/research_dashboard/
├── __init__.py
├── __main__.py         # 应用程序入口点
├── app.py              # 主应用程序逻辑
│
├── config/             # 配置管理
│   ├── manager.py      # 配置加载/保存
│   └── schema.py       # 配置数据类
│
├── modules/            # 模块系统
│   ├── base.py         # 模块基类
│   ├── registry.py     # 模块注册表
│   │
│   ├── arxiv/          # ArXiv 模块
│   │   └── module.py
│   │
│   ├── github/         # GitHub 模块
│   │   └── module.py
│   │
│   └── rss/            # RSS 模块
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

## 配置

配置管理由 `config/` 目录处理：

- `schema.py`：定义配置对象的数据类
- `manager.py`：处理配置的加载、保存和验证

默认配置存储在 `assets/default-config.json` 中，在首次运行时复制到用户的配置目录。

## 模块

模块系统设计为可扩展：

- `base.py`：定义所有模块的抽象基类
- `registry.py`：维护可用模块的注册表
- 每个模块都有自己的目录和 `module.py` 文件

当前实现的模块：

- ArXiv：根据关键词获取论文
- GitHub：显示 GitHub 活动
- RSS：聚合 RSS 订阅

## UI

UI 使用 NiceGUI 构建：

- `dashboard.py`：包含渲染主仪表盘和模块详细视图的函数
- 使用基于列的布局系统来灵活安排模块

## 静态资源

静态资源包括：

- `static/css/style.css` 中的 CSS 样式
- `assets/` 中的图像和其他资源

## 文档

文档在 `docs/` 目录中组织：

- `README.md`：主文档索引
- `overview.md`：项目概述
- `api/`：API 参考
- `development/`：开发者文档
- `modules/`：模块文档
- `user-guide/`：用户指南

## 脚本

实用脚本在 `scripts/` 目录中：

- `create_icon.py`：创建应用程序图标
- `generate_docs.py`：生成文档（计划中）

## 测试

`tests/` 目录为未来的测试实现保留。

## 分发

`dist/` 目录包含应用程序的构建分发。