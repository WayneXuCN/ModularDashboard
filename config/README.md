# Research Dashboard 配置样例

这个目录包含了不同布局模式的配置样例文件。

## 配置文件说明

### 1. user-config-1column.json
- **列数**: 1列
- **宽度模式**: default (全宽)
- **布局**: 所有模块在单列中垂直排列
- **适用场景**: 简单布局、移动设备、专注模式

### 2. user-config-2column.json
- **列数**: 2列
- **宽度模式**: default (全宽)
- **布局**: 左右两列分布
- **适用场景**: 标准桌面布局、平衡的内容分布

### 3. user-config-3column.json
- **列数**: 3列
- **宽度模式**: default (全宽)
- **布局**: 三列并排显示
- **适用场景**: 宽屏显示器、需要同时查看多个模块

### 4. user-config-slim.json
- **列数**: 3列
- **宽度模式**: slim (居中限制宽度)
- **布局**: 三列居中显示，最大宽度限制
- **适用场景**: 大屏幕、专注阅读、减少视觉干扰

## 如何使用

1. 备份当前配置文件：
   ```bash
   cp ~/.config/ModularDashboard/config.json ~/.config/ModularDashboard/config.json.backup
   ```

2. 复制想要的配置样例：
   ```bash
   # 例如使用3列布局
   cp config/user-config-3column.json ~/.config/ModularDashboard/config.json
   ```

3. 重启应用程序

## 响应式行为

所有配置都支持响应式布局：

- **小屏幕 (<640px)**: 单列显示
- **中小屏幕 (640px-767px)**: 两列显示
- **中屏幕 (768px-1023px)**: 三列显示（如果是3列配置）
- **大屏幕 (≥1024px)**: 完整列数显示

## 宽度模式说明

- **default**: 全宽显示，左右有适当内边距
- **slim**: 内容居中，最大宽度限制（约1152px）
- **wide**: 全宽显示，更大的左右内边距

## 自定义配置

你可以基于这些样例创建自己的配置：
1. 修改 `columns` 数值（1-3）
2. 调整 `width` 模式
3. 在 `column_config` 中重新分配模块到不同列
4. 启用/禁用特定模块