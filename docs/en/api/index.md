# API Reference

本节提供 Research Dashboard API 的详细文档。

## Overview

Research Dashboard API 由几个组件组成：

1. [Modules基类](./module-base.md) - 所有Modules的基类
2. [Configuration](./configuration.md) - Configuration管理系统

## 架构

Research Dashboard 遵循Modules化架构，每个信息源都作为一个独立的Modules实现。核心应用程序处理：

- Configuration管理
- UI 渲染
- Modules注册
- 路由

Modules负责：

- 从各自的来源获取数据
- 渲染 UI 组件
- 管理自己的状态和缓存

## 关键组件

### 应用

主应用程序逻辑在 `src/modular_dashboard/app.py` 中。它处理：

- 加载Configuration
- 设置路由
- 初始化 UI
- 运行应用程序

### Configuration

`src/modular_dashboard/config/` 中的Configuration系统处理：

- 加载默认和用户Configuration
- 管理Configuration文件
- 提供类型安全的Configuration对象

### Modules

`src/modular_dashboard/modules/` 中的Modules系统提供：

- 可用Modules的注册表
- 实现新Modules的基类
- ArXiv、GitHub 和 RSS Modules的实现

### UI

`src/modular_dashboard/ui/` 中的 UI 组件处理：

- 渲染主仪表盘
- 渲染Modules详细视图
- 实现基于列的Layout System

## 扩展 Research Dashboard

要使用新Modules扩展 Research Dashboard：

1. 创建继承自基础 `Module` 类的新Modules类
2. 实现所有必需的方法
3. 在 `src/modular_dashboard/modules/registry.py` 中注册Modules
4. 在 `src/modular_dashboard/assets/default-config.json` 中添加默认Configuration
5. 在 docs Table of Contents中记录Modules

有关实现新Modules的详细信息，请参阅[Modules基类](./module-base.md)文档。
