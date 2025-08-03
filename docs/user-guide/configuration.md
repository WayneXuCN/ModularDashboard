# 配置

Research Dashboard 通过位于系统配置目录中的 JSON 文件进行配置：

- **Windows**: `%APPDATA%\ModularDashboard\config.json`
- **macOS/Linux**: `~/.config/ModularDashboard/config.json`

首次运行时，Research Dashboard 会根据 `src/modular_dashboard/assets/default-config.json` 中的模板创建默认配置文件。

## 配置结构

配置文件具有以下结构：

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
        "width": "narrow",
        "modules": ["arxiv"]
      },
      {
        "width": "normal",
        "modules": ["github"]
      },
      {
        "width": "narrow",
        "modules": ["rss"]
      }
    ]
  },
  "modules": [
    {
      "id": "arxiv",
      "enabled": true,
      "collapsed": false,
      "config": {
        "refresh_interval": 3600,
        "keywords": [
          "machine learning",
          "artificial intelligence",
          "quantum computing"
        ]
      }
    },
    {
      "id": "github",
      "enabled": true,
      "collapsed": false,
      "config": {
        "refresh_interval": 3600,
        "username": "wayneXuCN",
        "repositories": [
          "ModularDashboard",
          "nicegui"
        ]
      }
    },
    {
      "id": "rss",
      "enabled": true,
      "collapsed": false,
      "config": {
        "refresh_interval": 3600,
        "feed_urls": [
          "https://sspai.com/feed",
          "https://waynexucn.github.io/feed.xml"
        ],
        "fetch_limit": 10,
        "show_limit": 5,
        "show_author": true,
        "show_description": true,
        "show_date": true,
        "show_image": true
      }
    }
  ]
}
```

## 主题配置

- `theme`: 可以是 "light" 或 "dark"

## 布局配置

布局配置控制整体仪表盘布局：

- `columns`: 列数 (1-3)
- `width`: 页面宽度 ("default", "narrow", 或 "wide")
- `show_nav`: 是否显示导航栏
- `column_config`: 列配置数组

每个列配置包含：

- `width`: 列宽度 ("narrow" 或 "normal")
- `modules`: 要在此列中显示的模块 ID 数组（顺序决定显示顺序）

注意：列内模块的显示顺序由列配置中 `modules` 数组的顺序决定，而不是模块配置中的单独位置字段。

## 模块配置

每个模块具有以下配置选项：

- `id`: 模块的唯一标识符
- `enabled`: 模块是否启用
- `collapsed`: 模块是否初始折叠
- `config`: 模块特定的配置选项

### ArXiv 模块配置

ArXiv 模块支持以下配置选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `keywords`: 要搜索的关键词数组

### GitHub 模块配置

GitHub 模块支持以下配置选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `username`: 要跟踪的 GitHub 用户名
- `repositories`: 要跟踪的仓库名称数组

### RSS 模块配置

RSS 模块支持以下配置选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `feed_urls`: 要跟踪的 RSS 订阅 URL 数组
- `fetch_limit`: 每个订阅获取的最大项目数
- `show_limit`: 在主视图中显示的最大项目数
- `show_author`: 是否显示作者
- `show_description`: 是否显示描述
- `show_date`: 是否显示发布日期
- `show_image`: 当可用时是否显示图片

## 配置示例

### 三列布局（默认）

```json
{
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "narrow",
        "modules": ["arxiv"]
      },
      {
        "width": "normal",
        "modules": ["github"]
      },
      {
        "width": "narrow",
        "modules": ["rss"]
      }
    ]
  }
}
```

这种布局将焦点信息源放在两侧，主要内容放在中间。

### 两列布局

```json
{
  "layout": {
    "columns": 2,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "normal",
        "modules": ["github"]
      },
      {
        "width": "normal",
        "modules": ["arxiv", "rss"]
      }
    ]
  }
}
```

这种布局将主要模块放在左侧，将次要模块组合在右侧。

### 单列布局

```json
{
  "layout": {
    "columns": 1,
    "width": "default",
    "show_nav": true,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "github", "rss"]
      }
    ]
  }
}
```

这种布局将所有模块堆叠在一列中，非常适合移动设备或专注的工作流程。