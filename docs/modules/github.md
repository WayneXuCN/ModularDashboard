# GitHub 模块

GitHub 模块显示您最近的 GitHub 活动，包括提交、问题和拉取请求。

## 概述

GitHub 模块获取并显示您在 GitHub 上的最近活动。这包括您仓库的提交、您已开启或评论的问题，以及您已创建或合并的拉取请求。

## 配置

GitHub 模模块支持以下配置选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位，默认值：3600）
- `username`: 要跟踪的 GitHub 用户名
- `repositories`: 要跟踪的仓库名称数组

配置示例：

```json
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
}
```

## 显示

在主仪表盘视图中，GitHub 模块显示您最近的活动。在详细视图中，它显示最近活动的列表。

每个活动显示包括：

- 带有活动链接的标题
- 简要摘要
- 发布日期
- 标签
- 作者

## 实现细节

GitHub 模块使用 GitHub API 获取活动数据。它实现了缓存以避免过多的 API 调用并减少加载时间。

该模块遵循标准模块接口，实现所有必需的方法：

- `id`: 返回 "github"
- `name`: 返回 "GitHub 活动"
- `icon`: 返回章鱼表情符号 (🐙)
- `description`: 返回 "您的最近 GitHub 活动"
- `fetch`: 从 GitHub API 获取活动
- `render`: 渲染主视图 UI
- `render_detail`: 渲染详细视图 UI

注意：当前实现使用占位符数据。在生产环境中，它将连接到 GitHub API 以获取真实数据。