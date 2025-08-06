# ArXiv 模块

ArXiv 模块根据您的关键词显示最新的 ArXiv 论文。

## 概述

ArXiv 模块获取并显示与您指定关键词匹配的 ArXiv 数据库中的论文。这对于希望跟上领域内最新出版物的研究人员特别有用。

## 配置

ArXiv 模块支持以下配置选项：

- `refresh_interval`: 刷新数据的频率（以秒为单位，默认值：3600）
- `keywords`: 要搜索的关键词数组

配置示例：

```json
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
```

## 显示

在主仪表盘视图中，ArXiv 模块显示与您关键词匹配的最新论文。在详细视图中，它显示最近论文的列表。

每个论文显示包括：

- 带有论文链接的标题
- 简要摘要（在主视图中截断）
- 发布日期
- 标签

## 实现细节

ArXiv 模块使用 ArXiv API 获取论文。它实现了缓存以避免过多的 API 调用并减少加载时间。

该模块遵循标准模块接口，实现所有必需的方法：

- `id`: 返回 "arxiv"
- `name`: 返回 "ArXiv 论文"
- `icon`: 返回书籍表情符号 (📚)
- `description`: 返回 "基于您关键词的最新 ArXiv 论文"
- `fetch`: 从 ArXiv API 获取论文
- `render`: 渲染主视图 UI
- `render_detail`: 渲染详细视图 UI
