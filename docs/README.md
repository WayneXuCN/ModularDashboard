# Research Dashboard Documentation

欢迎阅读 Research Dashboard 的文档。本文档包含项目规划、开发者信息和 API 设计。

## 当前状态

🚧 **项目初期**: 刚完成项目结构搭建，功能尚未完善  
🚧 **文档规划**: 文档结构已建立，内容正在完善中  
🚧 **持续开发**: 正在积极开发核心功能  

项目仍处于超早期开发阶段，文档内容可能会随着开发进展而变化。

## 文档结构

```
docs/
├── index.md                 # 首页
├── README.md                # 项目README副本
├── user-guide/              # 用户指南
│   ├── installation.md      # 安装指南
│   ├── getting-started.md   # 快速开始
│   ├── configuration.md     # 配置说明
│   └── packaging.md         # 打包说明
├── modules/                 # 模块文档
├── api/                     # API参考
└── development/             # 开发指南
```

## 浏览文档

### 在线浏览

您可以直接浏览 docs/ 目录中的 Markdown 文件。

### 本地预览（计划）

将来会支持使用 MkDocs 在本地预览文档网站:

```bash
# 启动本地开发服务器（功能尚未完善）
uv run mkdocs serve

# 访问 http://localhost:8000 查看文档
```

### 构建静态网站（计划）

构建静态文档网站:

```bash
# 构建文档（功能尚未完善）
uv run mkdocs build

# 输出位于 site/ 目录
```

## 文档内容

文档目前包含以下内容：

- [项目结构](development/structure.md) - 代码组织方式
- [模块设计](modules/index.md) - 模块系统规划
- [API 规划](api/module-base.md) - 核心接口设计

## 贡献文档

如果您想为 Research Dashboard 贡献文档，请查看以下信息：

- [贡献指南](development/contributing.md) - 如何贡献代码和文档
- 保持文档与代码同步更新
- 使用清晰简洁的语言描述功能和用法

## 技术栈

有关项目使用的技术栈信息，请参阅主项目的 [README](README.md) 文件。
