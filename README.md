# Research Dashboard

Research Dashboard 是一个面向科研人员的信息聚合仪表盘项目，目前处于超早期开发阶段。

## 当前状态

🚧 **项目初期**: 刚完成项目结构搭建，功能尚未完善  
🚧 **基础框架**: 已实现基本模块结构和UI框架  
🚧 **持续开发**: 正在积极开发核心功能  

欢迎关注项目进展，也欢迎提出功能建议和贡献代码！

## 项目目标

为科研人员提供一个**每日工作第一入口**的桌面级应用，通过高度可定制的卡片式布局，聚合来自 arXiv、GitHub、RSS、日历等多源信息，实现动态信息一眼掌握。

## 快速开始

### 安装依赖

```bash
# 使用 uv 安装依赖（推荐）
uv lock
uv sync
```

### 运行应用

```bash
# 以 Web 应用模式运行
uv run -m research_dashboard

# 以原生桌面应用模式运行（如果支持）
uv run -m research_dashboard --native
```

## 开发指南

### 项目结构

```
research-dashboard/
├── pyproject.toml              # 项目配置和依赖管理
├── README.md                   # 项目说明
├── LICENSE                     # 开源许可证
├── .gitignore                  # Git忽略文件配置
├── mkdocs.yml                  # 文档网站配置
│
├── src/
│   └── research_dashboard/     # 主要源代码
│       ├── __init__.py
│       ├── __main__.py         # 应用入口点
│       ├── main.py             # 主应用逻辑
│       │
│       ├── config/             # 配置管理
│       ├── modules/            # 模块系统
│       ├── ui/                 # 用户界面组件
│       ├── static/             # 静态资源文件
│       ├── utils/              # 工具函数
│       ├── assets/             # 应用资源
│       └── docs/               # 文档生成器
│
├── config/                     # 用户配置（运行时生成）
├── scripts/                    # 脚本工具
├── tests/                      # 测试代码（计划中）
├── docs/                       # 文档源文件
└── dist/                       # 编译输出
```

### 开发环境设置

1. 克隆项目仓库:

   ```bash
   git clone https://github.com/your-username/research-dashboard.git
   cd research-dashboard
   ```

2. 安装依赖:

   ```bash
   uv lock
   uv sync
   ```

### 代码规范

我们使用 ruff 进行代码检查和格式化：

```bash
# 检查代码
uv run ruff check .

# 格式化代码
uv run ruff format .
```

### 测试

测试功能正在规划中，将使用 pytest 进行测试:

```bash
# 运行测试（功能尚未实现）
uv run pytest
```

## 技术栈（计划）

| 类别 | 技术 | 状态 |
|------|------|------|
| **项目管理** | `uv` | ✅ 已采用 |
| **构建系统** | `hatchling` | ✅ 已采用 |
| **应用框架** | `NiceGUI` | ✅ 已采用 |
| **前端定制** | HTML/CSS/JS + `Tailwind CSS` | ✅ 计划采用 |
| **数据抓取** | `requests` + `feedparser` + `arxiv` | ✅ 计划采用 |
| **定时任务** | `APScheduler` | ✅ 计划采用 |
| **配置存储** | JSON 文件系统 | ✅ 计划采用 |

> **注意**: 项目仍处于早期阶段，部分技术栈正在实现中。

## 贡献

项目处于早期开发阶段，欢迎通过以下方式参与：

1. 提出功能建议或报告问题
2. 贡献代码实现功能模块
3. 完善文档和测试
4. 改进用户体验和界面设计

请阅读 [贡献指南](docs/development/contributing.md) 了解详情。
