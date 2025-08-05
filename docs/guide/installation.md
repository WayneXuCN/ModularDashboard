# 安装指南

本指南将引导您完成在系统上安装 Research Dashboard。

## 系统要求

Research Dashboard 需要：

- Python 3.8 或更高版本
- pip 或 uv 包管理器
- 用于从外部来源获取数据的互联网连接

## 安装方法

### 方法 1：使用 uv（推荐）

uv 是一个快速的 Python 包安装程序和解析器。如果您没有安装 uv，可以使用以下命令安装：

```bash
pip install uv
```

然后安装 Research Dashboard 依赖：

```bash
uv lock
uv sync
```

### 方法 2：使用 pip

如果您更喜欢使用 pip，可以使用以下命令安装依赖：

```bash
pip install -r requirements.txt
```

注意：该项目主要使用 `uv` 作为包管理器，因此使用 pip 可能需要额外步骤。

## 验证安装

安装依赖后，您可以通过运行以下命令验证安装：

```bash
uv run -m modular_dashboard.app --help
```

这应该会显示 Research Dashboard 应用程序的帮助信息。

## 下一步

安装完成后，请继续阅读[快速开始](./getting-started.md)指南，了解如何配置和运行 Research Dashboard。