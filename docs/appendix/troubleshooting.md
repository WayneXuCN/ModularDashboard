# 故障排除

本章节提供 Modular Dashboard 使用过程中常见问题的解决方案和调试技巧。

## 🛠️ 常见问题分类

### 安装和运行问题

#### 环境配置问题

**问题**：Python 版本不兼容
```
错误信息：Python 版本过低，需要 3.12 或更高版本
```

**解决方案**：
```bash
# 检查 Python 版本
python --version

# 使用 pyenv 管理 Python 版本
pyenv install 3.12.0
pyenv global 3.12.0

# 或者使用 conda
conda create -n modular-dashboard python=3.12
conda activate modular-dashboard
```

**问题**：依赖包安装失败
```
错误信息：Could not find a version that satisfies the requirement xxx
```

**解决方案**：
```bash
# 更新 pip
pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装依赖
uv sync

# 或者逐个安装
uv install package-name
```

#### 应用启动问题

**问题**：应用无法启动
```
错误信息：ModuleNotFoundError: No module named 'modular_dashboard'
```

**解决方案**：
```bash
# 检查当前目录
pwd

# 确保在项目根目录
cd /path/to/ModularDashboard

# 安装项目
uv install --editable .

# 或者使用 PYTHONPATH
export PYTHONPATH=/path/to/ModularDashboard:$PYTHONPATH
```

**问题**：端口占用
```
错误信息：Address already in use
```

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8080

# 终止进程
kill -9 <PID>

# 或者使用其他端口
uv run modular-dashboard --port 8081
```

### 配置问题

#### 配置文件格式错误

**问题**：配置文件 JSON 格式错误
```
错误信息：JSON decode error: Expecting property name enclosed in double quotes
```

**解决方案**：
```bash
# 验证 JSON 格式
python -m json.tool config/user-config.json

# 使用在线 JSON 验证工具
# https://jsonlint.com/

# 恢复默认配置
cp src/modular_dashboard/assets/default-config.json config/user-config.json
```

**问题**：配置文件不存在
```
错误信息：FileNotFoundError: [Errno 2] No such file or directory: 'config/user-config.json'
```

**解决方案**：
```bash
# 创建配置目录
mkdir -p config

# 复制默认配置
cp src/modular_dashboard/assets/default-config.json config/user-config.json

# 编辑配置文件
nano config/user-config.json
```

#### 模块配置问题

**问题**：模块无法启用
```
错误信息：Module not found: xxx
```

**解决方案**：
```json
// 检查模块 ID 是否正确
{
  "modules": [
    {
      "id": "arxiv",  // 确保模块 ID 正确
      "enabled": true,
      "config": {}
    }
  ]
}
```

**问题**：模块配置无效
```
错误信息：Invalid module configuration
```

**解决方案**：
```json
// 检查配置格式
{
  "id": "arxiv",
  "enabled": true,
  "config": {
    "keywords": ["AI", "machine learning"],
    "refresh_interval": 3600
  }
}
```

### 模块问题

#### 数据获取问题

**问题**：网络连接失败
```
错误信息：ConnectionError: Failed to establish connection
```

**解决方案**：
```bash
# 检查网络连接
ping google.com

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 配置代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

**问题**：API 限制
```
错误信息：Rate limit exceeded
```

**解决方案**：
```json
// 增加刷新间隔
{
  "id": "arxiv",
  "config": {
    "refresh_interval": 7200  // 增加到 2 小时
  }
}
```

#### 显示问题

**问题**：模块显示空白
```
错误信息：Module rendering failed
```

**解决方案**：
```bash
# 检查日志
tail -f logs/modular-dashboard.log

# 启用调试模式
export DEBUG=1
uv run modular-dashboard
```

**问题**：样式错乱
```
错误信息：CSS loading failed
```

**解决方案**：
```bash
# 清理浏览器缓存
# 在浏览器中按 Ctrl+Shift+R (或 Cmd+Shift+R)

# 检查静态文件
ls -la src/modular_dashboard/static/
```

### 性能问题

#### 内存使用过高

**问题**：应用占用内存过多
```
错误信息：Memory usage too high
```

**解决方案**：
```json
// 减少模块数量
{
  "modules": [
    {"id": "clock", "enabled": true},
    {"id": "weather", "enabled": true}
    // 只启用必要的模块
  ]
}
```

**问题**：响应缓慢
```
错误信息：Request timeout
```

**解决方案**：
```json
// 优化刷新间隔
{
  "id": "arxiv",
  "config": {
    "refresh_interval": 3600,
    "max_results": 5
  }
}
```

### 网络问题

#### 代理设置问题

**问题**：代理配置错误
```
错误信息：Proxy authentication failed
```

**解决方案**：
```bash
# 配置代理
export HTTP_PROXY=http://username:password@proxy.example.com:8080
export HTTPS_PROXY=http://username:password@proxy.example.com:8080

# 或者使用环境变量
export PROXY_URL="http://proxy.example.com:8080"
```

**问题**：SSL 证书问题
```
错误信息：SSL certificate verify failed
```

**解决方案**：
```bash
# 更新证书
# macOS
sudo update-ca-trust

# Linux
sudo update-ca-certificates

# 或者临时禁用验证（不推荐）
export SSL_VERIFY=false
```

## 🔧 调试技巧

### 启用调试模式

```bash
# 设置环境变量
export DEBUG=1
export LOG_LEVEL=DEBUG

# 启动应用
uv run modular-dashboard
```

### 查看日志

```bash
# 查看应用日志
tail -f logs/modular-dashboard.log

# 查看系统日志
journalctl -u modular-dashboard -f

# 使用 debug 模式
uv run modular-dashboard --debug
```

### 性能监控

```bash
# 监控内存使用
ps aux | grep modular-dashboard

# 监控网络连接
netstat -an | grep :8080

# 监控 CPU 使用
top -p $(pgrep -f modular-dashboard)
```

### 配置验证

```bash
# 验证配置文件
python -c "import json; json.load(open('config/user-config.json'))"

# 验证模块配置
python -c "from modular_dashboard.config.manager import load_config; print(load_config())"
```

## 📊 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|---------|------|----------|
| `E001` | 配置文件不存在 | 创建默认配置文件 |
| `E002` | JSON 格式错误 | 修复 JSON 格式 |
| `E003` | 模块未找到 | 检查模块 ID |
| `E004` | 网络连接失败 | 检查网络设置 |
| `E005` | API 限制 | 增加刷新间隔 |
| `E006` | 权限不足 | 检查文件权限 |
| `E007` | 端口占用 | 更改端口或终止进程 |
| `E008` | 内存不足 | 减少模块数量 |

## 🆘 获取帮助

### 在线资源

- **GitHub Issues**: [https://github.com/WayneXuCN/ModularDashboard/issues](https://github.com/WayneXuCN/ModularDashboard/issues)
- **GitHub Discussions**: [https://github.com/WayneXuCN/ModularDashboard/discussions](https://github.com/WayneXuCN/ModularDashboard/discussions)
- **项目文档**: [https://wayneXuCN.github.io/ModularDashboard/](https://wayneXuCN.github.io/ModularDashboard/)

### 报告问题

```bash
# 生成诊断信息
uv run modular-dashboard --diagnostic

# 收集系统信息
uname -a
python --version
uv --version
```

### 联系支持

- **邮件**: [wenjie.xu.cn@outlook.com](mailto:wenjie.xu.cn@outlook.com)
- **GitHub**: [@WayneXuCN](https://github.com/WayneXuCN)

## 🔄 定期维护

### 清理缓存

```bash
# 清理应用缓存
rm -rf ~/.cache/modular-dashboard/

# 清理日志文件
rm -f logs/*.log

# 清理临时文件
rm -rf /tmp/modular-dashboard/
```

### 更新应用

```bash
# 更新依赖
uv sync

# 更新应用
uv install --editable .

# 重启应用
uv run modular-dashboard
```

### 备份配置

```bash
# 备份配置文件
cp config/user-config.json config/user-config.json.backup

# 备份数据目录
cp -r ~/.modular-dashboard ~/.modular-dashboard.backup
```

---

通过以上故障排除指南，您应该能够解决大多数使用 Modular Dashboard 时遇到的问题。如果问题仍然存在，请通过上述渠道获取帮助。