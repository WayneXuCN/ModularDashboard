# 快速开始指南

本指南将帮助您快速安装和运行 Modular Dashboard，让您在几分钟内开始使用这个强大的信息聚合工具。

## 前置要求

### 系统要求
- **操作系统**：Windows 10+、macOS 10.15+、Linux (Ubuntu 18.04+)
- **Python 版本**：3.12 或更高版本
- **内存**：推荐 4GB RAM 以上
- **存储**：至少 100MB 可用空间
- **网络**：稳定的互联网连接（用于获取外部数据）

### 必需软件
- Python 3.12+
- Git (用于克隆项目)
- 包管理器：uv (推荐) 或 pip

## 安装步骤

### 1. 安装 Python

#### Windows
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.12+ 安装程序
3. 运行安装程序，确保勾选 "Add Python to PATH"

#### macOS
```bash
# 使用 Homebrew (推荐)
brew install python@3.12

# 或使用官方安装程序
# 从 https://www.python.org/downloads/macos/ 下载
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

### 2. 安装包管理器

#### 推荐：uv (现代 Python 包管理器)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.sh | iex"
```

#### 备选：pip
```bash
# 升级 pip
python -m pip install --upgrade pip
```

### 3. 获取项目代码

```bash
# 克隆项目
git clone https://github.com/WayneXuCN/ModularDashboard.git
cd ModularDashboard
```

### 4. 创建虚拟环境

```bash
# 使用 uv
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

# 或使用标准 Python
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows
```

### 5. 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

## 运行应用

### Web 应用模式 (推荐用于开发)

```bash
# 激活虚拟环境后运行
uv run -m modular_dashboard.app
```

应用启动后，打开浏览器访问：`http://localhost:8080`

### 原生桌面应用模式

```bash
# 修改 app.py 最后一行
# 将 run_app(native=False) 改为 run_app(native=True)

# 然后运行
uv run -m modular_dashboard.app
```

应用会启动一个原生桌面窗口。

## 首次配置

### 1. 配置文件位置

应用首次运行时会自动创建配置文件：

- **Windows**：`%APPDATA%\ModularDashboard\config.json`
- **macOS**：`~/Library/Application Support/ModularDashboard/config.json`
- **Linux**：`~/.config/ModularDashboard/config.json`

### 2. 基本配置

配置文件包含以下主要部分：

```json
{
  "version": "0.1.0",
  "theme": "light",
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true
  },
  "modules": [
    {
      "id": "arxiv",
      "config": {
        "keywords": ["machine learning", "AI"]
      }
    }
  ]
}
```

### 3. 配置模块

根据您的需求配置各个模块：

#### ArXiv 模块
```json
{
  "id": "arxiv",
  "config": {
    "keywords": ["您的兴趣关键词"],
    "refresh_interval": 3600
  }
}
```

#### GitHub 模块
```json
{
  "id": "github",
  "config": {
    "username": "您的GitHub用户名",
    "repositories": ["您关注的项目"]
  }
}
```

#### RSS 模块
```json
{
  "id": "rss",
  "config": {
    "feed_urls": ["https://example.com/feed.xml"],
    "show_limit": 5
  }
}
```

## 基本使用

### 1. 界面导航

- **主仪表盘**：显示所有启用的模块
- **模块详情**：点击模块标题查看详细信息
- **配置界面**：通过设置按钮调整配置

### 2. 模块操作

- **刷新数据**：点击刷新按钮更新模块数据
- **折叠/展开**：点击模块标题折叠或展开内容
- **查看详情**：点击"查看更多"进入模块详情页

### 3. 布局调整

- **列数调整**：通过配置文件修改布局列数 (1-3列)
- **模块排序**：通过配置文件调整模块显示顺序
- **主题切换**：支持亮色和暗色主题

## 常见模块配置

### 时钟模块
```json
{
  "id": "clock",
  "config": {
    "timezone": "local",
    "format_24h": true,
    "show_seconds": false
  }
}
```

### 天气模块
```json
{
  "id": "weather",
  "config": {
    "city": "北京",
    "api_key": "您的天气API密钥"
  }
}
```

### 待办事项模块
```json
{
  "id": "todo",
  "config": {
    "max_items": 10,
    "auto_save": true
  }
}
```

## 开发环境设置

如果您计划开发自定义模块，请设置开发环境：

### 1. 安装开发依赖
```bash
# 使用 uv
uv sync --dev

# 或使用 pip
pip install -e ".[dev]"
```

### 2. 启用热重载
```bash
# 设置环境变量
export ENVIRONMENT=development  # Linux/macOS
set ENVIRONMENT=development     # Windows

# 运行应用
uv run -m modular_dashboard.app
```

### 3. 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_specific_module.py

# 生成覆盖率报告
pytest --cov=src/modular_dashboard
```

## 故障排除

### 1. 安装问题

**问题**：`ModuleNotFoundError: No module named 'modular_dashboard'`
```bash
# 解决方案：确保以可编辑模式安装
pip install -e .
```

**问题**：权限错误
```bash
# 解决方案：使用用户安装
pip install --user -e .
```

### 2. 运行问题

**问题**：端口被占用
```bash
# 解决方案：指定其他端口
uv run -m modular_dashboard.app --port 8081
```

**问题**：模块加载失败
```bash
# 解决方案：检查模块依赖
uv sync
```

### 3. 配置问题

**问题**：配置文件格式错误
- 使用 JSON 验证工具检查配置文件
- 参考 `config/user-config.json` 示例

**问题**：模块不显示
- 检查模块是否启用 (`"enabled": true`)
- 确认模块配置正确

## 下一步

### 基础使用
- 阅读 [配置指南](./configuration.md) 了解详细配置选项
- 探索 [内置模块](../modules/) 了解可用功能
- 自定义您的仪表盘布局和主题

### 开发扩展
- 学习 [模块开发](../development/module-development.md)
- 了解 [API 参考](../development/api-reference.md)
- 查看 [贡献指南](../development/contributing.md)

### 社区支持
- 访问 [GitHub 仓库](https://github.com/WayneXuCN/ModularDashboard)
- 报告问题或提出功能请求
- 贡献代码或文档改进

## 性能优化建议

### 1. 系统优化
- 关闭不必要的模块以减少资源使用
- 调整刷新间隔以平衡实时性和性能
- 使用 SSD 存储以提高 I/O 性能

### 2. 网络优化
- 配置合理的超时时间
- 使用缓存减少网络请求
- 考虑使用代理服务器

### 3. 内存优化
- 限制内存缓存大小
- 定期清理过期数据
- 监控内存使用情况

## 安全建议

### 1. 配置安全
- 不要在配置文件中存储敏感信息
- 使用环境变量存储 API 密钥
- 定期更新依赖包

### 2. 网络安全
- 使用 HTTPS 连接
- 验证外部数据源
- 限制网络访问权限

### 3. 数据安全
- 定期备份配置文件
- 加密敏感数据
- 监控异常访问

恭喜！您已经成功安装并运行了 Modular Dashboard。开始探索和定制您的个人仪表盘吧！