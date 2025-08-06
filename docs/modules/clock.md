# 时钟模块

时钟模块为 Modular Dashboard 提供准确的时间显示功能，支持多种时间格式和显示选项。

## 🎯 功能特性

### 时间显示

- **数字时钟**：清晰的数字时间显示
- **日期显示**：完整的日期信息
- **星期显示**：当前星期信息
- **时区支持**：本地时间和 UTC 时间

### 格式选项

- **12/24 小时制**：灵活的时间显示格式
- **秒数显示**：可选择是否显示秒数
- **日期格式**：自定义日期显示格式
- **时间格式**：自定义时间显示格式

### 自动更新

- **实时更新**：每秒自动刷新时间
- **可配置间隔**：支持自定义更新间隔
- **低资源消耗**：优化的更新机制

## ⚙️ 配置选项

### 基本配置

```json
{
  "id": "clock",
  "config": {
    "timezone": "local",            // 时区设置
    "format_24h": true,              // 24 小时制
    "show_seconds": false,           // 显示秒数
    "show_date": true,               // 显示日期
    "update_interval": 1,            // 更新间隔（秒）
    "date_format": "%Y-%m-%d",       // 日期格式
    "time_format": "%H:%M:%S",       // 时间格式
    "show_weekday": true,            // 显示星期
    "locale": "zh_CN"               // 地区设置
  }
}
```

### 配置参数详解

#### 时区设置 (timezone)

- **`local`** - 使用系统本地时区
- **`UTC`** - 使用 UTC 时间
- **时区名称** - 如 "Asia/Shanghai", "America/New_York"

#### 时间格式 (format_24h)

- **`true`** - 24 小时制 (14:30)
- **`false`** - 12 小时制 (2:30 PM)

#### 显示选项

- **`show_seconds`** - 是否显示秒数
- **`show_date`** - 是否显示日期
- **`show_weekday`** - 是否显示星期

#### 格式化字符串

- **`date_format`** - Python strftime 格式的日期格式
- **`time_format`** - Python strftime 格式的时间格式

## 📱 界面展示

### 主视图

在仪表盘卡片中显示：

- 大号数字时钟
- 日期和星期信息
- 简洁的设计风格

### 详细视图

在独立页面中显示：

- 更大的时间显示
- 详细的日期信息
- 时区信息
- 格式化选项

## 🌍 地区支持

### 中文地区

```json
{
  "config": {
    "locale": "zh_CN",
    "date_format": "%Y年%m月%d日",
    "show_weekday": true
  }
}
```

### 英文地区

```json
{
  "config": {
    "locale": "en_US",
    "date_format": "%B %d, %Y",
    "show_weekday": true
  }
}
```

### 欧洲地区

```json
{
  "config": {
    "locale": "de_DE",
    "date_format": "%d.%m.%Y",
    "format_24h": true
  }
}
```

## 🔧 高级配置

### 自定义格式

```json
{
  "config": {
    "date_format": "%Y年%m月%d日 星期%w",
    "time_format": "%H时%M分%S秒",
    "show_weekday": false  // 不单独显示星期，因为已包含在日期中
  }
}
```

### 世界时钟配置

```json
{
  "config": {
    "timezone": "UTC",
    "format_24h": true,
    "show_seconds": true,
    "update_interval": 1,
    "date_format": "%Y-%m-%d",
    "time_format": "%H:%M:%S UTC"
  }
}
```

### 简洁模式

```json
{
  "config": {
    "show_seconds": false,
    "show_date": false,
    "show_weekday": false,
    "format_24h": true
  }
}
```

## 🎨 样式定制

### 主题适配

时钟模块会自动适配当前主题：

- **亮色主题**：深色文字，浅色背景
- **暗色主题**：浅色文字，深色背景

### 响应式设计

- **桌面端**：大号字体，完整信息
- **移动端**：适中字体，核心信息
- **大屏幕**：更大的字体和间距

## ⚡ 性能优化

### 更新策略

- **智能更新**：只在可见时更新
- **最小化重绘**：仅更新变化的部分
- **低优先级**：避免影响其他模块

### 资源管理

- **单一实例**：避免重复创建定时器
- **自动清理**：模块销毁时清理资源
- **内存优化**：最小化内存占用

## 🛠️ 故障排除

### 常见问题

#### 时间显示不准确

**原因**：系统时间设置错误
**解决**：

```bash
# 检查系统时间
date

# Linux/macOS 同步时间
sudo ntpdate pool.ntp.org

# Windows 同步时间（在设置中）
```

#### 日期格式错误

**原因**：格式字符串不正确
**解决**：

```json
{
  "config": {
    "date_format": "%Y-%m-%d",  // 检查格式字符串
    "locale": "zh_CN"
  }
}
```

#### 时区设置无效

**原因**：时区名称不正确或系统不支持
**解决**：

```json
{
  "config": {
    "timezone": "local",  // 回退到本地时区
    "format_24h": true
  }
}
```

### 调试技巧

#### 启用详细日志

```python
# 在模块配置中添加调试选项
{
  "config": {
    "debug": true,
    "update_interval": 1
  }
}
```

#### 检查时区支持

```python
import zoneinfo
print("可用时区:", zoneinfo.available_timezones()[:10])
```

## 🔄 更新日志

### 版本 1.0.0

- ✨ 初始版本发布
- 🎨 支持基本时间显示
- 🌍 支持多地区格式
- ⚡ 性能优化

### 计划中的功能

- **多时区显示** - 同时显示多个时区的时间
- **模拟时钟** - 圆形模拟时钟界面
- **闹钟功能** - 设置提醒和通知
- **世界时钟** - 主要城市时间显示

---

时钟模块为 Modular Dashboard 提供了准确、美观的时间显示功能，是仪表盘中不可或缺的基础模块。通过灵活的配置选项，您可以定制出适合自己需求的时间显示效果。
