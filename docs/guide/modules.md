# 模块使用指南

Modular Dashboard 提供了丰富的内置模块，每个模块都有特定的功能和配置选项。本指南介绍如何使用和管理这些模块。

## 📦 内置模块概览

### 数据源模块
- **ArXiv 模块** - 学术论文搜索和展示
- **GitHub 模块** - GitHub 活动监控
- **RSS 模块** - RSS 订阅阅读器

### 工具模块
- **时钟模块** - 数字时钟和日期显示
- **天气模块** - 天气信息展示
- **待办事项模块** - 任务管理和待办列表

### 监控模块
- **版本发布模块** - 软件版本发布监控
- **网站监控模块** - 网站可用性监控

### 娱乐模块
- **动物图片模块** - 随机动物图片展示

## 🔧 模块管理

### 启用/禁用模块

在配置文件中控制模块的启用状态：

```json
{
  "modules": [
    {
      "id": "arxiv",
      "enabled": true,    // 启用模块
      "config": { ... }
    },
    {
      "id": "weather",
      "enabled": false,   // 禁用模块
      "config": { ... }
    }
  ]
}
```

### 模块配置

每个模块都有自己的配置选项：

```json
{
  "id": "arxiv",
  "enabled": true,
  "config": {
    "refresh_interval": 3600,
    "keywords": ["machine learning", "AI"],
    "max_results": 10
  }
}
```

### 模块位置

在布局配置中指定模块的显示位置：

```json
{
  "layout": {
    "columns": 3,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "clock"]
      },
      {
        "width": "normal", 
        "modules": ["github", "weather"]
      }
    ]
  }
}
```

## 📚 详细模块说明

### ArXiv 模块

**功能**：搜索和展示 ArXiv 学术论文

**配置选项**：
```json
{
  "id": "arxiv",
  "enabled": true,
  "config": {
    "refresh_interval": 3600,        // 刷新间隔（秒）
    "keywords": [                   // 搜索关键词
      "machine learning",
      "artificial intelligence",
      "quantum computing"
    ],
    "max_results": 10,              // 最大结果数
    "show_abstract": true,          // 显示摘要
    "show_authors": true,           // 显示作者
    "show_pdf_link": true           // 显示 PDF 链接
  }
}
```

**使用场景**：
- 科研人员跟踪最新论文
- 技术人员了解前沿技术
- 学术研究动态监控

### GitHub 模块

**功能**：监控 GitHub 用户活动和仓库动态

**配置选项**：
```json
{
  "id": "github",
  "enabled": true,
  "config": {
    "refresh_interval": 1800,        // 刷新间隔（秒）
    "username": "wayneXuCN",         // GitHub 用户名
    "repositories": [               // 监控的仓库
      "ModularDashboard",
      "nicegui"
    ],
    "show_events": [                // 显示的事件类型
      "push",
      "issues",
      "pull_requests",
      "releases"
    ],
    "max_events": 20               // 最大事件数
  }
}
```

**使用场景**：
- 开源项目维护者监控项目动态
- 开发者跟踪关注的项目
- 团队协作和代码审查

### RSS 模块

**功能**：订阅和阅读 RSS 源

**配置选项**：
```json
{
  "id": "rss",
  "enabled": true,
  "config": {
    "refresh_interval": 1800,        // 刷新间隔（秒）
    "feed_urls": [                   // RSS 源列表
      "https://sspai.com/feed",
      "https://waynexucn.github.io/feed.xml"
    ],
    "max_items_per_feed": 10,        // 每个源最大项目数
    "show_limit": 5,                 // 主视图显示数
    "show_author": true,             // 显示作者
    "show_description": true,        // 显示描述
    "show_date": true,               // 显示日期
    "show_image": true,              // 显示图片
    "open_in_new_tab": true          // 新标签页打开
  }
}
```

**使用场景**：
- 博客和新闻订阅
- 技术文章阅读
- 信息聚合和跟踪

### 时钟模块

**功能**：显示当前时间和日期

**配置选项**：
```json
{
  "id": "clock",
  "enabled": true,
  "config": {
    "timezone": "local",            // 时区（local 或 UTC）
    "format_24h": true,              // 24 小时制
    "show_seconds": false,           // 显示秒
    "show_date": true,               // 显示日期
    "update_interval": 1,            // 更新间隔（秒）
    "date_format": "%Y-%m-%d",       // 日期格式
    "time_format": "%H:%M:%S",       // 时间格式
    "show_weekday": true             // 显示星期
  }
}
```

### 天气模块

**功能**：显示天气信息

**配置选项**：
```json
{
  "id": "weather",
  "enabled": true,
  "config": {
    "city": "北京",                  // 城市名称
    "api_key": "",                   // 天气 API 密钥
    "refresh_interval": 3600,        // 刷新间隔（秒）
    "show_temperature": true,        // 显示温度
    "show_humidity": true,           // 显示湿度
    "show_wind": true,               // 显示风力
    "show_forecast": true,           // 显示预报
    "temperature_unit": "celsius",    // 温度单位（celsius/fahrenheit）
    "language": "zh"                // 语言设置
  }
}
```

**注意**：需要配置天气 API 密钥才能正常使用。

### 待办事项模块

**功能**：任务管理和待办事项

**配置选项**：
```json
{
  "id": "todo",
  "enabled": true,
  "config": {
    "max_items": 10,                 // 最大项目数
    "auto_save": true,               // 自动保存
    "show_completed": true,          // 显示已完成项目
    "show_timestamp": true,          // 显示时间戳
    "allow_priority": true,          // 允许设置优先级
    "allow_categories": true,        // 允许分类
    "sort_by": "priority"            // 排序方式（priority/date/created）
  }
}
```

**使用场景**：
- 个人任务管理
- 工作待办事项
- 项目任务跟踪

### 版本发布模块

**功能**：监控软件版本发布

**配置选项**：
```json
{
  "id": "releases",
  "enabled": true,
  "config": {
    "refresh_interval": 1800,        // 刷新间隔（秒）
    "repositories": [               // 监控的仓库
      "torvalds/linux",
      "gitlab:gitlab-org/gitlab-runner",
      "codeberg:forgejo/forgejo",
      "docker:library/postgres"
    ],
    "max_releases": 3,              // 显示版本数
    "show_pre_release": false,      // 显示预发布版本
    "show_release_notes": true,     // 显示发布说明
    "filter_by_tag": true           // 按标签过滤
  }
}
```

**仓库格式支持**：
- GitHub: `owner/repo`
- GitLab: `gitlab:owner/repo`
- Codeberg: `codeberg:owner/repo`
- Docker: `docker:image/name`

### 网站监控模块

**功能**：监控网站可用性

**配置选项**：
```json
{
  "id": "monitor",
  "enabled": true,
  "config": {
    "timeout": 15,                   // 超时时间（秒）
    "interval": 60,                  // 检查间隔（秒）
    "sites": [                       // 监控的网站
      {
        "name": "Google",
        "url": "https://www.google.com",
        "expected_status": 200
      },
      {
        "name": "GitHub",
        "url": "https://www.github.com",
        "expected_status": 200
      }
    ],
    "show_response_time": true,       // 显示响应时间
    "show_status_code": true,        // 显示状态码
    "alert_on_failure": true         // 失败时提醒
  }
}
```

### 动物图片模块

**功能**：显示随机动物图片

**配置选项**：
```json
{
  "id": "animals",
  "enabled": true,
  "config": {
    "animal_type": "cat",            // 动物类型
    "height": 200,                   // 图片高度
    "auto_refresh": false,           // 自动刷新
    "refresh_interval": 30,          // 刷新间隔（秒）
    "show_title": true,              // 显示标题
    "border_radius": 8,              // 圆角大小
    "show_refresh_button": true      // 显示刷新按钮
  }
}
```

**支持的动物类型**：
- `cat` - 猫
- `dog` - 狗
- `fox` - 狐狸
- `panda` - 熊猫
- `random` - 随机动物

## 🔧 模块配置技巧

### 性能优化

#### 合理设置刷新间隔
```json
{
  "config": {
    "refresh_interval": 3600  // 根据需要调整，避免过于频繁
  }
}
```

#### 限制显示数量
```json
{
  "config": {
    "max_results": 5,        // 限制显示数量提高性能
    "show_limit": 3          // 主视图显示更少
  }
}
```

### 网络优化

#### 使用缓存
```json
{
  "config": {
    "refresh_interval": 1800,  // 设置合理的缓存时间
    "timeout": 30             // 设置适当的超时时间
  }
}
```

#### 失败处理
```json
{
  "config": {
    "retry_count": 3,         // 失败重试次数
    "fallback_to_cache": true  // 失败时使用缓存
  }
}
```

## 🎯 模块组合示例

### 开发者工作台
```json
{
  "layout": {
    "columns": 2,
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
    {"id": "weather", "enabled": true}
  ]
}
```

### 信息阅读中心
```json
{
  "layout": {
    "columns": 1,
    "column_config": [
      {
        "width": "normal",
        "modules": ["rss", "arxiv", "animals"]
      }
    ]
  },
  "modules": [
    {"id": "rss", "enabled": true},
    {"id": "arxiv", "enabled": true},
    {"id": "animals", "enabled": true}
  ]
}
```

## 🆘 常见问题

### 模块不显示数据
1. 检查模块是否启用（`enabled: true`）
2. 确认网络连接正常
3. 验证 API 密钥配置
4. 查看应用日志排查错误

### 数据更新缓慢
1. 调整 `refresh_interval` 设置
2. 检查网络延迟
3. 考虑启用缓存
4. 减少显示的数据量

### 模块显示异常
1. 检查配置格式是否正确
2. 确认模块在布局配置中被引用
3. 尝试重置为默认配置
4. 查看浏览器控制台错误

---

通过合理配置和组合模块，您可以创建一个完全个性化的仪表盘，满足不同场景下的使用需求。