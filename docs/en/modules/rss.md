# RSS Modules

RSS Modules显示您 RSS Feeds的最新项目。

## Overview

RSS Modules获取并显示您Configuration的 RSS Feeds中的最新项目。这允许您在一个地方聚合来自多个来源的内容。

## Configuration

RSS Modules支持以下Configuration选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位，默认值：3600）
- `feed_urls`: 要跟踪的 RSS Feeds URL 数组
- `fetch_limit`: 每个订阅获取的最大项目数
- `show_limit`: 在主视图中显示的最大项目数
- `show_author`: 是否显示作者
- `show_description`: 是否显示描述
- `show_date`: 是否显示发布日期
- `show_image`: 当可用时是否显示图片

Configuration示例：

```json
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
```

## 显示

在主仪表盘视图中，RSS Modules显示您订阅中的最新项目（受 `show_limit` 限制）。在详细视图中，它显示来自所有订阅的项目网格（每个订阅受 `fetch_limit` 限制）。

每个项目显示包括：

- 带有完整文章链接的标题
- 作者（如果 `show_author` 为 true）
- 来源
- 发布日期（如果 `show_date` 为 true）
- 简要描述（如果 `show_description` 为 true）
- 图片（如果 `show_image` 为 true 且可用）

## 实现细节

RSS Modules使用 `feedparser` 库解析 RSS Feeds。它实现了缓存以避免过多的请求并减少加载时间。

该Modules遵循标准Modules接口，实现所有必需的方法：

- `id`: 返回 "rss"
- `name`: 返回 "RSS Feeds"
- `icon`: 返回卫星表情符号 (📡)
- `description`: 返回 "您 RSS Feeds的最新项目"
- `fetch`: 从 RSS Feeds获取项目
- `render`: 渲染主视图 UI
- `render_detail`: 渲染详细视图 UI

## 支持的订阅类型

RSS Modules支持多种订阅格式：

- RSS 0.91, 0.92, 1.0, 2.0
- Atom 0.3, 1.0
- CDF

## 图片支持

当启用 `show_image` 时，Modules会尝试使用以下方法从订阅项目中提取图片：

1. `media:content` 元素
2. `media:thumbnail` 元素
3. `image` 元素

如果找不到图片或 `show_image` 被禁用，则不显示图片。