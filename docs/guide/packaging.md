# 打包指南

本指南解释如何打包 Research Dashboard 以进行分发。

## 先决条件

在打包 Research Dashboard 之前，请确保您已：

1. 安装了 Python 3.8 或更高版本
2. 安装了所有项目依赖
3. 正确配置了环境

## 创建分发包

Research Dashboard 使用标准的 Python 打包工具。要创建分发包：

1. 确保所有依赖都列在 `pyproject.toml` 中
2. 如有必要，更新 `pyproject.toml` 中的版本号
3. 构建包：

```bash
python -m build
```

这将在 `dist/` 目录中创建源码和 wheel 分发包。

## 创建独立可执行文件

要创建无需安装 Python 即可运行的独立可执行文件：

1. 安装 PyInstaller：

```bash
pip install pyinstaller
```

2. 创建可执行文件：

```bash
pyinstaller --onefile --windowed src/modular_dashboard/app.py
```

这将在 `dist/` 目录中创建一个独立的可执行文件。

## 平台特定打包

### Windows

对于 Windows，您可以使用 Inno Setup 或 NSIS 等工具创建安装程序。

### macOS

对于 macOS，您可以创建 .app 包或使用 py2app 等工具。

### Linux

对于 Linux，您可以根据目标发行版创建 DEB 或 RPM  包。

## 分发

打包后，您可以通过以下方式分发 Research Dashboard：

1. PyPI 用于 Python  包分发
2. GitHub Releases 用于独立可执行文件
3. 包管理器如 Homebrew (macOS) 或 Snap (Linux)

## 最佳实践

1. 在分发前始终在目标平台上测试您的包
2. 包含带有安装和使用说明的 README
3. 清晰指定兼容的 Python 版本和依赖
4. 考虑同时提供源码和二进制分发包