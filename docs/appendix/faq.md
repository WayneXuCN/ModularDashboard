# 常见问题解答 (FAQ)

本节收集了用户在使用 Modular Dashboard 过程中最常见的问题和解答，帮助您快速解决遇到的各种问题。

## 安装和运行问题

### Q: 应用无法启动，提示 "ModuleNotFoundError" 或 "ImportError"

**A**: 这通常是因为 Python 环境或依赖包安装问题。请尝试以下解决方案：

```bash
# 1. 确保在正确的虚拟环境中
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 2. 重新安装依赖
uv sync

# 3. 以可编辑模式安装
pip install -e .

# 4. 检查 Python 版本
python --version  # 应该是 3.12+
```

### Q: 运行时出现 "端口已被占用" 错误

**A**: 默认端口 8080 被其他程序占用。您可以：

```bash
# 1. 查找占用端口的进程
lsof -i :8080  # Linux/macOS
netstat -ano | findstr :8080  # Windows

# 2. 终止占用进程或使用其他端口
uv run -m modular_dashboard.app --port 8081
```

### Q: 应用启动但浏览器无法访问

**A**: 请检查以下方面：

1. **防火墙设置**：确保防火墙允许本地端口访问
2. **网络配置**：尝试使用 `127.0.0.1:8080` 而非 `localhost:8080`
3. **浏览器设置**：清除浏览器缓存或尝试隐私模式
4. **代理设置**：临时禁用系统代理

## 配置问题

### Q: 配置文件在哪里？如何修改配置？

**A**: 配置文件位置取决于您的操作系统：

- **Windows**: `%APPDATA%\ModularDashboard\config.json`
- **macOS**: `~/Library/Application Support/ModularDashboard/config.json`
- **Linux**: `~/.config/ModularDashboard/config.json`

您可以直接编辑这些文件，或使用预设配置：

```bash
# 使用预设配置
cp config/user-config-1column.json ~/.config/ModularDashboard/config.json
```

### Q: 修改配置后没有生效

**A**: 请尝试以下步骤：

1. **重启应用**：大多数配置更改需要重启应用才能生效
2. **验证 JSON 格式**：确保配置文件是有效的 JSON
3. **检查配置路径**：确认修改的是正确的配置文件
4. **查看日志**：检查控制台是否有配置相关的错误信息

### Q: 如何重置为默认配置？

**A**: 您可以删除当前配置文件，应用会在下次启动时重新创建：

```bash
# 删除配置文件
rm ~/.config/ModularDashboard/config.json  # Linux/macOS
del %APPDATA%\ModularDashboard\config.json  # Windows

# 重启应用
uv run -m modular_dashboard.app
```

## 模块问题

### Q: 某个模块不显示数据或显示错误

**A**: 这可能是由于以下原因：

1. **模块未启用**：检查配置中模块的 `enabled` 字段是否为 `true`
2. **网络问题**：检查网络连接和 API 访问权限
3. **配置错误**：验证模块的配置参数是否正确
4. **API 限制**：某些 API 可能有访问频率限制

**调试步骤**：
```bash
# 1. 检查模块是否启用
grep -A 5 '"id": "module_name"' ~/.config/ModularDashboard/config.json

# 2. 查看应用日志
uv run -m modular_dashboard.app 2>&1 | grep -i error

# 3. 手动测试 API
curl "https://api.example.com/endpoint"
```

### Q: 如何添加新的模块？

**A**: 请按照以下步骤：

1. **创建模块文件**：在 `src/modular_dashboard/modules/your_module/` 目录下创建模块
2. **实现模块接口**：继承 `Module` 或 `ExtendedModule` 基类
3. **注册模块**：在 `registry.py` 中添加模块注册
4. **更新配置**：在配置文件中添加模块配置

详细步骤请参考 [模块开发指南](../development/module-development.md)。

### Q: 模块数据不更新或更新很慢

**A**: 这通常与缓存和刷新间隔设置有关：

1. **检查刷新间隔**：
```json
{
  "id": "your_module",
  "config": {
    "refresh_interval": 1800  // 减少这个值以更频繁刷新
  }
}
```

2. **手动刷新缓存**：
   - 重启应用
   - 或等待缓存过期

3. **检查网络连接**：确保可以访问外部 API

## 性能问题

### Q: 应用运行缓慢，占用大量内存

**A**: 请尝试以下优化措施：

1. **关闭不必要的模块**：
```json
{
  "id": "resource_heavy_module",
  "enabled": false
}
```

2. **调整刷新间隔**：
```json
{
  "id": "data_module",
  "config": {
    "refresh_interval": 7200  // 增加到2小时
  }
}
```

3. **清理缓存**：
```bash
# 删除缓存文件
rm -rf ~/.modular_dashboard/cache/
```

4. **监控资源使用**：
```bash
# 查看内存使用
ps aux | grep modular_dashboard

# 查看文件描述符
lsof -p <pid>
```

### Q: 页面加载很慢或卡顿

**A**: 可能的解决方案：

1. **减少模块数量**：禁用一些不常用的模块
2. **优化布局**：使用单列或两列布局
3. **检查网络延迟**：特别是对于外部数据源
4. **浏览器性能**：尝试使用不同的浏览器或清除缓存

## 数据和存储问题

### Q: 我的设置和数据没有保存

**A**: 检查以下方面：

1. **文件权限**：确保应用有写入配置目录的权限
2. **磁盘空间**：检查磁盘是否有足够空间
3. **配置文件路径**：确认修改的是正确的配置文件
4. **自动保存**：某些模块需要手动保存或启用自动保存

### Q: 如何备份和恢复我的配置？

**A**: 备份和恢复配置：

```bash
# 备份配置
cp -r ~/.config/ModularDashboard ~/modular_dashboard_backup_$(date +%Y%m%d)

# 恢复配置
cp -r ~/modular_dashboard_backup_20250730/* ~/.config/ModularDashboard/

# 备份单个配置文件
cp ~/.config/ModularDashboard/config.json ~/config_backup.json
```

### Q: 存储数据在哪里？如何清理？

**A**: 数据存储位置：

- **配置数据**：`~/.config/ModularDashboard/`
- **应用数据**：`~/.modular_dashboard/`
- **缓存数据**：`~/.modular_dashboard/cache/`

清理数据：
```bash
# 清理缓存
rm -rf ~/.modular_dashboard/cache/

# 清理所有数据（谨慎操作）
rm -rf ~/.modular_dashboard/

# 重置应用
rm -rf ~/.config/ModularDashboard/
rm -rf ~/.modular_dashboard/
```

## 网络和 API 问题

### Q: 模块显示 "网络错误" 或 "API 不可用"

**A**: 网络相关问题的解决方案：

1. **检查网络连接**：
```bash
ping google.com
curl -I https://api.github.com
```

2. **检查代理设置**：
```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

3. **测试 API 访问**：
```bash
curl "https://api.github.com/users/your_username"
curl "https://export.arxiv.org/api/query?search=all:machine+learning"
```

4. **配置超时设置**：
```json
{
  "id": "api_module",
  "config": {
    "timeout": 60  // 增加超时时间
  }
}
```

### Q: 如何配置代理？

**A**: 通过环境变量配置代理：

```bash
# Linux/macOS
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

# Windows
set HTTP_PROXY=http://proxy.example.com:8080
set HTTPS_PROXY=http://proxy.example.com:8080

# 然后启动应用
uv run -m modular_dashboard.app
```

## UI 和显示问题

### Q: 界面显示异常或布局错乱

**A**: UI 问题的解决方案：

1. **清除浏览器缓存**：按 `Ctrl+Shift+R` (Windows) 或 `Cmd+Shift+R` (Mac)
2. **检查浏览器兼容性**：推荐使用 Chrome、Firefox 或 Safari 最新版本
3. **调整显示缩放**：浏览器缩放设置为 100%
4. **检查配置**：确保布局配置正确

### Q: 暗色主题不工作

**A**: 当前版本主要支持亮色主题。暗色主题正在开发中。

### Q: 移动设备上显示效果不佳

**A**: 建议使用单列布局以获得更好的移动体验：

```json
{
  "layout": {
    "columns": 1,
    "width": "slim"
  }
}
```

## 开发和扩展问题

### Q: 如何开发自定义模块？

**A**: 请参考详细的 [模块开发指南](../development/module-development.md)，包含完整的开发流程和示例代码。

### Q: 模块开发时如何调试？

**A**: 调试技巧：

1. **启用详细日志**：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **使用开发模式**：
```bash
export ENVIRONMENT=development
uv run -m modular_dashboard.app
```

3. **添加调试输出**：
```python
def fetch(self):
    logger.debug(f"Fetching data for module {self.id}")
    # 你的代码
    logger.debug(f"Received {len(data)} items")
    return data
```

### Q: 如何贡献代码或报告问题？

**A**: 欢迎贡献！请按照以下步骤：

1. **Fork 项目**：在 GitHub 上 fork 项目
2. **创建分支**：`git checkout -b feature/your-feature`
3. **开发测试**：确保代码有测试覆盖
4. **提交 PR**：遵循项目的代码规范

报告问题请使用 [GitHub Issues](https://github.com/WayneXuCN/ModularDashboard/issues)。

## 系统兼容性问题

### Q: 在 Windows 上运行遇到权限问题

**A**: Windows 权限问题的解决方案：

1. **以管理员身份运行**：右键命令提示符，选择"以管理员身份运行"
2. **检查用户权限**：确保用户对配置目录有写入权限
3. **使用用户安装**：`pip install --user -e .`
4. **调整 UAC 设置**：临时降低用户账户控制设置

### Q: macOS 上应用无法访问网络

**A**: macOS 网络访问问题的解决方案：

1. **检查防火墙**：系统偏好设置 → 安全性与隐私 → 防火墙
2. **检查网络隐私**：确保终端/命令行工具有网络访问权限
3. **重置网络配置**：
```bash
sudo dscacheutil -flushcache
sudo ifconfig en0 down && sudo ifconfig en0 up
```

### Q: Linux 上依赖包安装失败

**A**: Linux 依赖问题的解决方案：

1. **更新系统包**：
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade

# CentOS/RHEL
sudo yum update
```

2. **安装系统依赖**：
```bash
# Ubuntu/Debian
sudo apt install python3-dev python3-venv build-essential

# CentOS/RHEL
sudo yum install python3-devel python3-virtualin gcc gcc-c++
```

3. **使用虚拟环境**：避免使用系统 Python

## 更新和升级问题

### Q: 如何更新到最新版本？

**A**: 更新步骤：

```bash
# 1. 备份当前配置
cp -r ~/.config/ModularDashboard ~/modular_dashboard_backup/

# 2. 获取最新代码
git pull origin main

# 3. 更新依赖
uv sync

# 4. 重启应用
uv run -m modular_dashboard.app
```

### Q: 更新后配置不兼容

**A**: 配置兼容性问题的解决方案：

1. **查看更新日志**：了解配置变更
2. **使用默认配置**：临时重置为默认配置
3. **手动迁移配置**：根据新格式调整配置文件
4. **回滚版本**：如果问题严重，可以回滚到之前的版本

## 安全问题

### Q: 如何保护我的 API 密钥？

**A**: API 密钥安全最佳实践：

1. **使用环境变量**：
```bash
export API_KEY="your_api_key_here"
```

2. **不要提交到版本控制**：确保 `.gitignore` 包含配置文件
3. **使用配置文件模板**：创建配置模板但不包含真实密钥
4. **定期轮换密钥**：定期更换 API 密钥

### Q: 应用是否安全？会不会泄露我的数据？

**A**: Modular Dashboard 的安全特性：

- **本地运行**：所有数据都在本地处理
- **开源代码**：代码完全开源，可以审查
- **最小权限**：只请求必要的权限
- **数据加密**：敏感数据在存储时加密

建议：
- 使用来自可信源的 RSS 和 API
- 定期更新应用到最新版本
- 不要在配置中存储敏感信息

## 故障排除指南

### 基本故障排除步骤

1. **检查日志**：查看控制台输出和日志文件
2. **验证配置**：确保配置文件格式正确
3. **测试网络**：确认网络连接正常
4. **重启应用**：简单的重启可以解决很多问题
5. **重置配置**：使用默认配置进行测试

### 收集诊断信息

```bash
# 创建诊断报告
echo "=== Modular Dashboard 诊断报告 ===" > diagnosis.txt
echo "日期: $(date)" >> diagnosis.txt
echo "系统: $(uname -a)" >> diagnosis.txt
echo "Python: $(python --version)" >> diagnosis.txt
echo "配置文件:" >> diagnosis.txt
cat ~/.config/ModularDashboard/config.json >> diagnosis.txt
echo "日志:" >> diagnosis.txt
tail -n 50 ~/.modular_dashboard/logs/app.log >> diagnosis.txt
```

### 获取帮助

如果以上解决方案都无法解决您的问题：

1. **查看文档**：仔细阅读相关文档
2. **搜索 Issues**：在 GitHub Issues 中搜索类似问题
3. **创建新 Issue**：提供详细的错误信息和重现步骤
4. **社区支持**：在相关技术社区寻求帮助

---

通过本 FAQ，您应该能够解决大多数使用 Modular Dashboard 时遇到的问题。如果问题仍然存在，请参考相关文档或寻求社区支持。