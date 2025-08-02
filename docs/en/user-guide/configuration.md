# Configuration

Research Dashboard 通过位于系统ConfigurationTable of Contents中的 JSON 文件进行Configuration：

- **Windows**: `%APPDATA%\ResearchDashboard\config.json`
- **macOS/Linux**: `~/.config/ResearchDashboard/config.json`

首次运行时，Research Dashboard 会根据 `src/research_dashboard/assets/default-config.json` 中的模板创建默认Configuration文件。

## Configuration结构

Configuration文件具有以下结构：

```json
{
  "version": "0.1.0",
  "theme": "light",
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true,
    "center_content": false,
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
          "ResearchDashboard",
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

## 主题Configuration

- `theme`: 可以是 "light" 或 "dark"

## 布局Configuration

布局Configuration控制整体仪表盘布局：

- `columns`: 列数 (1-3)
- `width`: 页面宽度 ("default", "narrow", 或 "wide")
- `show_nav`: 是否显示导航栏
- `center_content`: 是否垂直居中内容
- `column_config`: 列Configuration数组

每个列Configuration包含：

- `width`: 列宽度 ("narrow" 或 "normal")
- `modules`: 要在此列中显示的Modules ID 数组（顺序决定显示顺序）

注意：列内Modules的显示顺序由列Configuration中 `modules` 数组的顺序决定，而不是ModulesConfiguration中的单独位置字段。

## ModulesConfiguration

每个Modules具有以下Configuration选项：

- `id`: Modules的唯一标识符
- `enabled`: Modules是否启用
- `collapsed`: Modules是否初始折叠
- `config`: Modules特定的Configuration选项

### ArXiv ModulesConfiguration

ArXiv Modules支持以下Configuration选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `keywords`: 要搜索的关键词数组

### GitHub ModulesConfiguration

GitHub Modules支持以下Configuration选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `username`: 要跟踪的 GitHub 用户名
- `repositories`: 要跟踪的仓库名称数组

### RSS ModulesConfiguration

RSS Modules支持以下Configuration选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位）
- `feed_urls`: 要跟踪的 RSS Feeds URL 数组
- `fetch_limit`: 每个订阅获取的最大项目数
- `show_limit`: 在主视图中显示的最大项目数
- `show_author`: 是否显示作者
- `show_description`: 是否显示描述
- `show_date`: 是否显示发布日期
- `show_image`: 当可用时是否显示图片

## Configuration示例

### 三列布局（默认）

```json
{
  "layout": {
    "columns": 3,
    "width": "default",
    "show_nav": true,
    "center_content": false,
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
    "center_content": false,
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

这种布局将主要Modules放在左侧，将次要Modules组合在右侧。

### 单列布局

```json
{
  "layout": {
    "columns": 1,
    "width": "default",
    "show_nav": true,
    "center_content": false,
    "column_config": [
      {
        "width": "normal",
        "modules": ["arxiv", "github", "rss"]
      }
    ]
  }
}
```

这种布局将所有Modules堆叠在一列中，非常适合移动设备或专注的工作流程。