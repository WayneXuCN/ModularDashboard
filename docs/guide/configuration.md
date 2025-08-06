# 配置指南

Modular Dashboard 通过位于系统配置目录中的 JSON 配置文件进行管理。本指南详细介绍配置文件的结构、选项和最佳实践。

## 配置文件位置

### 自动创建机制
应用首次运行时会自动创建配置文件，基于 `src/modular_dashboard/assets/default-config.json` 模板。

### 配置文件路径
- **Windows**: `%APPDATA%\modular_dashboard\config.json`
- **macOS**: `~/.modular_dashboard/config.json`
- **Linux**: `~/.modular_dashboard/config.json`

### 多配置文件支持
项目提供了多个预设配置文件模板：
- `config/user-config.json` - 默认三列布局
- `config/user-config-1column.json` - 单列布局
- `config/user-config-3column.json` - 三列布局
- `config/user-config-slim.json` - 紧凑布局

## 配置文件结构

### 完整配置示例

```json
{
  "version": "0.1.0",
  "theme": "light",
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "clock"]
      },
      {
        "width": "normal",
        "modules": ["github", "weather", "todo"]
      },
      {
        "width": "normal",
        "modules": ["rss", "releases", "animals"]
      }
    ]
  },
  "modules": [
    {
      "id": "arxiv",
      "collapsed": false,
      "config": {
        "refresh_interval": 3600,
        "keywords": [
          "machine learning",
          "artificial intelligence",
          "quantum computing"
        ]
      }
    }
  ]
}
```

### 顶级配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `version` | string | "0.1.0" | 配置文件版本 |
| `theme` | string | "light" | 主题模式 |
| `layout` | object | - | 布局配置 |
| `modules` | array | [] | 模块配置数组 |

## 主题配置

### 可用主题
- `"light"` - 亮色主题
- `"dark"` - 暗色主题（未来版本支持）

### 主题切换
```json
{
  "theme": "light"
}
```

## 布局配置详解

### 布局基本参数

| 参数 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `columns` | integer | 3 | 1-3 | 列数 |
| `width` | string | "default" | "slim", "default", "wide" | 页面宽度 |
| `show_nav` | boolean | true | true/false | 显示导航栏 |
| `column_config` | array | - | - | 列配置数组 |

### 列配置结构

每个列配置对象包含：

```json
{
  "width": "normal",        // 列宽度
  "modules": ["arxiv", "clock"]  // 模块ID数组
}
```

#### 列宽度选项
- `"narrow"` - 窄列（约25%宽度）
- `"normal"` - 标准列（约33%宽度）
- `"wide"` - 宽列（约50%宽度，仅在1-2列布局中有效）

### 布局配置示例

#### 1. 三列平衡布局
```json
{
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "clock"]
      },
      {
        "width": "normal", 
        "modules": ["github", "weather"]
      },
      {
        "width": "normal",
        "modules": ["rss", "todo"]
      }
    ]
  }
}
```

#### 2. 两列主次布局
```json
{
  "layout": {
    "columns": 2,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "wide",
        "modules": ["github", "arxiv", "rss"]
      },
      {
        "width": "narrow",
        "modules": ["clock", "weather", "todo"]
      }
    ]
  }
}
```

#### 3. 单列专注布局
```json
{
  "layout": {
    "columns": 1,
    "width": "slim",
    "show_nav": true,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "github", "rss", "todo"]
      }
    ]
  }
}
```

## 模块配置详解

### 通用模块配置

每个模块配置对象包含以下字段：

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 模块唯一标识符 |
| `enabled` | boolean | true | 是否启用模块 |
| `collapsed` | boolean | false | 初始状态是否折叠 |
| `config` | object | {} | 模块特定配置 |

### 数据源模块配置

#### ArXiv 模块
```json
{
      "id": "arxiv",
      "config": {
        "refresh_interval": 3600,        // 刷新间隔（秒）
        "keywords": [                   // 搜索关键词
          "machine learning",
          "artificial intelligence", 
          "quantum computing"
        ]
      }
    }
```

#### GitHub 模块
```json
{
      "id": "github",
      "config": {
        "refresh_interval": 3600,        // 刷新间隔（秒）
        "username": "wayneXuCN",         // GitHub用户名
        "repositories": [               // 监控的仓库
          "ModularDashboard",
          "nicegui"
        ]
      }
    }
```

#### RSS 模块
```json
{
      "id": "rss",
      "config": {
        "refresh_interval": 3600,        // 刷新间隔（秒）
        "feed_urls": [                   // RSS源URL数组
          "https://sspai.com/feed",
          "https://waynexucn.github.io/feed.xml"
        ],
        "fetch_limit": 10,               // 每个源获取条数
        "show_limit": 5,                 // 主视图显示条数
        "show_author": true,             // 显示作者
        "show_description": true,        // 显示描述
        "show_date": true,               // 显示日期
        "show_image": true               // 显示图片
      }
    }
```

### 工具模块配置

#### 时钟模块
```json
{
      "id": "clock",
      "config": {
        "timezone": "local",            // 时区
        "format_24h": true,              // 24小时制
        "show_seconds": false,           // 显示秒
        "update_interval": 1,            // 更新间隔（秒）
        "date_format": "%Y-%m-%d"        // 日期格式
      }
    }
```

#### 天气模块
```json
{
      "id": "weather",
      "config": {
        "city": "北京",                  // 城市名称
        "api_key": ""                    // 天气API密钥
      }
    }
```

#### 待办事项模块
```json
{
      "id": "todo",
      "config": {
        "max_items": 10,                 // 最大项目数
        "auto_save": true                // 自动保存
      }
    }
```

### 监控模块配置

#### 版本发布模块
```json
{
      "id": "releases",
      "config": {
        "refresh_interval": 1800,        // 刷新间隔（秒）
        "repositories": [               // 监控的仓库
          "torvalds/linux",
          "gitlab:gitlab-org/gitlab-runner",
          "codeberg:forgejo/forgejo",
          "docker:library/postgres"
        ],
        "max_releases": 3                // 显示版本数
      }
    }
```

#### 网站监控模块
```json
{
      "id": "monitor",
      "config": {
        "timeout": 15,                   // 超时时间（秒）
        "sites": [                       // 监控的网站
          "https://www.google.com",
          "https://www.github.com",
          "https://www.apple.com",
          "https://www.microsoft.com"
        ]
      }
    }
```

### 娱乐模块配置

#### 动物图片模块
```json
{
      "id": "animals",
      "config": {
        "animal_type": "cat",            // 动物类型
        "height": 200,                   // 图片高度
        "auto_refresh": false,           // 自动刷新
        "refresh_interval": 30,          // 刷新间隔（秒）
        "show_title": true,              // 显示标题
        "border_radius": 8               // 圆角大小
      }
    }
```

## 配置管理最佳实践

### 1. 配置文件维护

#### 备份配置
```bash
# 创建配置备份
cp ~/.config/ModularDashboard/config.json ~/.config/ModularDashboard/config.json.backup

# 恢复配置
cp ~/.config/ModularDashboard/config.json.backup ~/.config/ModularDashboard/config.json
```

#### 版本控制
将个人配置文件纳入版本控制：
```bash
# 添加到git仓库
git add config/user-config.json
git commit -m "添加个人配置文件"
```

### 2. 性能优化配置

#### 刷新间隔优化
```json
{
  "modules": [
    {
      "id": "arxiv",
      "config": {
        "refresh_interval": 7200  // 2小时刷新一次
      }
    },
    {
      "id": "github", 
      "config": {
        "refresh_interval": 1800  // 30分钟刷新一次
      }
    }
  ]
}
```

#### 模块启用策略
```json
{
  "modules": [
    {
      "id": "arxiv",
      "enabled": true    // 启用重要模块
    },
    {
      "id": "weather",
      "enabled": false   // 禁用不常用模块
    }
  ]
}
```

### 3. 安全配置

#### 敏感信息处理
```json
{
  "modules": [
    {
      "id": "weather",
      "config": {
        "api_key": "${WEATHER_API_KEY}"  // 使用环境变量
      }
    }
  ]
}
```

#### 网络访问限制
```json
{
  "modules": [
    {
      "id": "rss",
      "config": {
        "feed_urls": [
          "https://trusted-source.com/feed"  // 仅使用可信源
        ]
      }
    }
  ]
}
```

## 配置验证和调试

### 1. 配置文件验证

#### JSON格式验证
```bash
# 使用python验证JSON
python -m json.tool ~/.config/ModularDashboard/config.json

# 使用jq验证
cat ~/.config/ModularDashboard/config.json | jq empty
```

#### 配置项验证
检查必需字段：
- `version` - 配置版本
- `theme` - 主题设置
- `layout.columns` - 列数 (1-3)
- `layout.column_config` - 列配置
- 每个模块的 `id` 和 `enabled` 字段

### 2. 常见配置问题

#### 模块不显示
**问题**：配置的模块没有在界面中显示
**解决**：
1. 检查 `enabled` 字段是否为 `true`
2. 确认模块在 `column_config` 中被引用
3. 验证模块配置格式正确

#### 布局错乱
**问题**：界面布局显示异常
**解决**：
1. 检查 `columns` 数值是否在 1-3 范围内
2. 确认 `column_config` 数组长度与 `columns` 匹配
3. 验证列宽度设置正确

#### 数据不更新
**问题**：模块数据长时间不更新
**解决**：
1. 检查 `refresh_interval` 设置是否合理
2. 确认网络连接正常
3. 验证API密钥或访问权限

### 3. 配置重置

#### 重置为默认配置
```bash
# 删除当前配置
rm ~/.config/ModularDashboard/config.json

# 重启应用，会自动创建默认配置
uv run -m modular_dashboard.app
```

#### 使用预设配置
```bash
# 复制预设配置
cp config/user-config-1column.json ~/.config/ModularDashboard/config.json
```

## 高级配置技巧

### 1. 环境特定配置

#### 开发环境配置
```json
{
  "theme": "light",
  "layout": {
    "columns": 1,
    "width": "wide"
  },
  "modules": [
    {
      "id": "github",
      "enabled": true,
      "config": {
        "refresh_interval": 300  // 开发时更频繁刷新
      }
    }
  ]
}
```

#### 生产环境配置
```json
{
  "theme": "light",
  "layout": {
    "columns": 3,
    "width": "default"
  },
  "modules": [
    {
      "id": "arxiv",
      "config": {
        "refresh_interval": 7200  // 生产环境减少刷新频率
      }
    }
  ]
}
```

### 2. 动态配置

#### 条件模块启用
可以通过脚本动态生成配置：
```python
import json
import os

config = {
    "version": "0.1.0",
    "theme": "light",
    "layout": {
        "columns": 3,
        "width": "default",
        "show_nav": True,
        "column_config": [
            {"width": "normal", "modules": ["arxiv", "clock"]},
            {"width": "normal", "modules": ["github", "weather"]},
            {"width": "normal", "modules": ["rss", "todo"]}
        ]
    },
    "modules": []
}

# 根据环境变量动态添加模块
if os.getenv('ENABLE_RSS', 'true').lower() == 'true':
    config["modules"].append({
        "id": "rss",
        "enabled": True,
        "config": {
            "feed_urls": ["https://example.com/feed"]
        }
    })

# 保存配置
with open(os.path.expanduser('~/.config/ModularDashboard/config.json'), 'w') as f:
    json.dump(config, f, indent=2)
```

### 3. 配置模板

#### 工作专用配置
```json
{
  "layout": {
    "columns": 2,
    "width": "default",
    "column_config": [
      {
        "width": "wide",
        "modules": ["github", "arxiv", "releases"]
      },
      {
        "width": "narrow", 
        "modules": ["clock", "todo", "weather"]
      }
    ]
  },
  "modules": [
    {"id": "github", "enabled": true},
    {"id": "arxiv", "enabled": true},
    {"id": "releases", "enabled": true},
    {"id": "clock", "enabled": true},
    {"id": "todo", "enabled": true},
    {"id": "weather", "enabled": false}
  ]
}
```

#### 个人生活配置
```json
{
  "layout": {
    "columns": 1,
    "width": "slim",
    "column_config": [
      {
        "width": "normal",
        "modules": ["rss", "weather", "animals", "todo"]
      }
    ]
  },
  "modules": [
    {"id": "rss", "enabled": true},
    {"id": "weather", "enabled": true},
    {"id": "animals", "enabled": true},
    {"id": "todo", "enabled": true},
    {"id": "github", "enabled": false},
    {"id": "arxiv", "enabled": false}
  ]
}
```

## 配置迁移和升级

### 版本兼容性
- 配置文件版本字段用于向后兼容
- 新版本会自动迁移旧配置格式
- 建议备份配置后再升级应用

### 配置迁移工具
未来版本将提供配置迁移工具，自动：
- 更新配置文件版本
- 迁移过时的配置项
- 添加新的默认配置

---

通过合理配置 Modular Dashboard，您可以创建一个完全个性化的信息聚合工作台，满足不同场景下的使用需求。