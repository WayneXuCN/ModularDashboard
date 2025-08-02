# 仪表盘布局配置

Research Dashboard 支持灵活的基于列的布局，允许您以最适合您工作流程的方式组织模块。

## 布局概述

仪表盘可以配置为 1-3 列，每列具有可自定义的宽度和模块排列。这使您可以完全控制信息的呈现方式。

## 配置选项

### 页面宽度

控制仪表盘的整体宽度：

- `default` - 标准宽度 (1100px)
- `narrow` - 紧凑宽度 (1000px) 
- `wide` - 扩展宽度 (1600px)

### 列配置

每列可以独立配置：

- `width` - 列宽度 (`narrow` 或 `normal`)
- `modules` - 要在此列中显示的模块 ID 数组（顺序决定显示顺序）

### 导航和定位

- `show_nav` - 切换顶部导航栏的可见性
- `center_content` - 垂直居中仪表盘内容

## 布局示例

### 三列布局（默认）

```
[ ArXiv ]  [ GitHub ]  [ RSS ]
[ Narrow ] [ Normal ] [ Narrow ]
```

这种布局将焦点信息源放在两侧，主要内容放在中间。

### 两列布局

```
[ GitHub ]  [ ArXiv + RSS ]
[ Normal ]  [    Normal    ]
```

这种布局将主要模块放在左侧，将次要模块组合在右侧。

### 单列布局

```
[ ArXiv ]
[ GitHub ]
[  RSS  ]
[Normal ]
```

这种布局将所有模块堆叠在一列中，非常适合移动设备或专注的工作流程。

## 自定义布局

要自定义布局：

1. 打开系统配置目录中的 `config.json`
2. 修改 `layout` 部分：
   - 调整 `columns` 以设置列数 (1-3)
   - 设置 `width` 以控制整体页面宽度
   - 在 `column_config` 中配置每列：
     - 将 `width` 设置为 `narrow` 或 `normal`
     - 在 `modules` 数组中按您希望的显示顺序列出模块 ID

两列布局的配置示例：

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

此配置创建了两列等宽的布局，左侧是 GitHub，右侧是堆叠的 ArXiv/RSS。每列的 `modules` 数组中的模块顺序决定了它们的显示顺序。

注意：与以前的版本不同，模块的显示顺序现在由每列配置中 `modules` 数组的顺序决定，而不是模块配置中的单独位置字段。