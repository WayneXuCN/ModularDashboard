# 贡献指南

感谢您有兴趣为 Research Dashboard 做贡献！本指南将帮助您了解如何参与项目开发。

## 行为准则

请遵守我们的行为准则，确保为所有人创造一个友好和包容的环境。

## 开发环境设置

1. 在 GitHub 上 fork 仓库
2. 本地克隆您的 fork
3. 使用 `uv lock` 和 `uv sync` 安装依赖
4. 使用 `uv run -m modular_dashboard.app` 运行应用程序

## 贡献流程

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

## 代码风格

Research Dashboard 遵循 Python PEP 8 风格指南。代码会使用 `ruff` 自动格式化：

```bash
uv run ruff format .
```

代码也会使用 `ruff` 检查风格和正确性：

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

## 报告问题

如果您发现 bug 或有功能请求，请在 GitHub 上提交 issue，并包含：

1. 清晰的标题
2. 详细描述
3. 重现步骤（对于 bug）
4. 预期和实际行为（对于 bug）
5. 系统信息（操作系统、Python 版本等）

## 添加新模块

要添加新模块：

1. 创建继承自基础 `Module` 类的新模块类
2. 实现所有必需的方法
3. 在 `src/modular_dashboard/modules/registry.py` 中注册模块
4. 在 `src/modular_dashboard/assets/default-config.json` 中添加默认配置
5. 在 docs 目录中记录模块

## 代码审查

所有拉取请求都需要通过代码审查。审查人员会检查：

1. 代码质量和风格
2. 功能正确性
3. 文档完整性
4. 测试覆盖（如果适用）

## 发布流程

项目维护人员负责发布新版本。发布流程包括：

1. 更新版本号
2. 更新 CHANGELOG
3. 创建发布标签
4. 构建和上传到 PyPI

## 获得帮助

如果您在贡献过程中需要帮助：

1. 查看现有文档
2. 在 GitHub 上提交 issue
3. 联系项目维护人员

感谢您对 Research Dashboard 的贡献！
