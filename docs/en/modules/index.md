# Modules文档

本节包含 Research Dashboard 中所有Modules的文档。

## 可用Modules

- [ArXiv Papers](./arxiv.md) - 基于您关键词的最新 ArXiv Papers
- [GitHub Activity](./github.md) - 您最近的 GitHub Activity
- [RSS Feeds](./rss.md) - 您 RSS Feeds的最新项目

## Modules架构

Research Dashboard 使用Modules化架构，每个信息源都作为一个独立的Modules实现。这使得扩展和自定义变得容易。

### Modules接口

所有Modules都继承自基础 `Module` 类并实现以下方法：

- `id`: 返回Modules的唯一标识符
- `name`: 返回Modules的人类可读名称
- `icon`: 返回Modules的图标（emoji 或 SVG 路径）
- `description`: 返回Modules功能的描述
- `fetch`: 从源获取数据并返回标准化项目
- `render`: 使用 NiceGUI 组件渲染Modules的 UI
- `render_detail`: 渲染Modules的详细视图页面

### ModulesConfiguration

每个Modules都可以在主Configuration文件中定义自己的Configuration选项。这些选项在Modules实例化时传递给Modules。

### 在仪表盘布局中使用Modules

Modules可以排列在灵活的基于列的布局中。在Configuration文件中，您可以定义最多 3 列并指定每列中显示的Modules。每列中Modules的顺序由该列的 `modules` 数组中的顺序决定。

有关如何Configuration仪表盘布局的详细信息，请参阅[Configuration指南](../user-guide/configuration.md)。