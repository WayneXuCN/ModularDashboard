# API 参考

本节提供 Research Dashboard API 的详细文档。

## 概述

Research Dashboard API 由几个组件组成：

1. [模块基类](./module-base.md) - 所有模块的基类
2. [配置](./configuration.md) - 配置管理系统

## 架构

Research Dashboard 遵循模块化架构，每个信息源都作为一个独立的模块实现。核心应用程序处理：

- 配置管理
- UI 渲染
- 模块注册
- 路由

模块负责：

- 从各自的来源获取数据
- 渲染 UI 组件
- 管理自己的状态和缓存

## 关键组件

### 应用

主应用程序逻辑在 `src/modular_dashboard/app.py` 中。它处理：

- 加载配置
- 设置路由
- 初始化 UI
- 运行应用程序

### 配置

`src/modular_dashboard/config/` 中的配置系统处理：

- 加载默认和用户配置
- 管理配置文件
- 提供类型安全的配置对象

### 模块

`src/modular_dashboard/modules/` 中的模块系统提供：

- 可用模块的注册表
- 实现新模块的基类
- ArXiv、GitHub 和 RSS 模块的实现

### UI

`src/modular_dashboard/ui/` 中的 UI 组件处理：

- 渲染主仪表盘
- 渲染模块详细视图
- 实现基于列的布局系统

## 扩展 Research Dashboard

要使用新模块扩展 Research Dashboard：

1. 创建继承自基础 `Module` 类的新模块类
2. 实现所有必需的方法
3. 在 `src/modular_dashboard/modules/registry.py` 中注册模块
4. 在 `src/modular_dashboard/assets/default-config.json` 中添加默认配置
5. 在 docs 目录中记录模块

有关实现新模块的详细信息，请参阅[模块基类](./module-base.md)文档。
