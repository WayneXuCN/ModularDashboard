# Getting Started

本指南将帮助您开始使用 Research Dashboard，从初始设置到首次运行。

## 初始设置

Installation依赖后，您需要设置Configuration。Research Dashboard 在首次运行时会自动在系统的ConfigurationTable of Contents中创建默认Configuration文件：

- **Windows**: `%APPDATA%\ModularDashboard\config.json`
- **macOS/Linux**: `~/.config/ModularDashboard/config.json`

## 运行应用程序

要作为 Web 应用程序运行 Research Dashboard：

```bash
uv run -m modular_dashboard.app
```

要Run as a native desktop application Research Dashboard：

```bash
uv run -m modular_dashboard.app native
```

默认情况下，应用程序将在 `http://localhost:8080` 上可用。

## 首次运行体验

首次运行时，Research Dashboard 将：

1. 在系统的标准Configuration位置创建ConfigurationTable of Contents
2. 将默认Configuration复制到该Table of Contents中的 `config.json`
3. 启动 Web 服务器并在默认浏览器中打开仪表盘

## Configuration

Research Dashboard 是高度可Configuration的。Configuration文件采用 JSON 格式，包括以下设置：

- 主题（浅色/深色）
- 布局（列数、宽度、导航）
- Modules（启用/禁用、设置）

有关Configuration Research Dashboard 的详细信息，请参阅[Configuration指南](./configuration.md)。

## 故障排除

如果遇到问题：

1. 检查所有依赖是否已正确Installation
2. 确保Configuration文件是有效的 JSON
3. 检查控制台输出中的错误消息
4. 验证防火墙是否阻止了应用程序

如果继续遇到问题，请在 GitHub 上[报告问题](https://github.com/WayneXuCN/ModularDashboard/issues)。
