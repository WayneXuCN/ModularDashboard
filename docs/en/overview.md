# Overview

Research Dashboard 是一个为研究人员设计的可定制信息聚合仪表盘。它提供了一个统一的界面来查看和管理来自多个来源的信息，包括 ArXiv Papers、GitHub Activity和 RSS Feeds。

## 目的

Research Dashboard 的主要目的是为研究人员提供一个"日常工作的第一站"，通过高度可定制的卡片式布局聚合来自多个来源的信息。这使得研究人员能够快速掌握动态信息。

## 主要功能

### 信息来源

Research Dashboard 目前支持三个主要的信息来源：

1. **ArXiv Papers**：基于您关键词的最新 ArXiv Papers
2. **GitHub Activity**：您最近的 GitHub Activity，包括提交、问题和拉取请求
3. **RSS Feeds**：您 RSS Feeds的最新项目

每个信息来源都作为一个Modules实现，可以独立启用、禁用和Configuration。

### 灵活的Layout System

Research Dashboard 具有灵活的基于列的Layout System，允许您以最适合您工作流程的方式组织信息：

- Configuration 1-3 列，具有不同的宽度（窄或正常）
- 将Modules放置在任何列中的任何顺序
- 自定义整体页面宽度（窄、默认或宽）
- 选择是否显示导航元素
- 垂直居中内容以获得更清晰的外观

### 自定义

Research Dashboard 提供了广泛的自定义选项：

- **主题**：Toggle between light and dark color schemes
- **ModulesConfiguration**：独立Configuration每个Modules及其特定设置
- **布局**：使用基于列的系统自定义仪表盘布局
- **Native Desktop Support**：Run as a native desktop application，获得更集成的体验

### 技术特性

- **Responsive Design**：Works on desktop and mobile devices
- **实时更新**：基于可Configuration的时间间隔自动刷新信息
- **可扩展架构**：基于Modules的系统，可以轻松添加新的信息来源
- **现代化 UI**：美观的玻璃态效果界面，带有流畅的动画