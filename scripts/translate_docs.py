#!/usr/bin/env python3
"""
Script to translate documentation from Chinese to English using AI translation.
This is a placeholder implementation - in a real scenario, you would integrate
with a translation API like Google Translate, DeepL, or OpenAI.
"""

import os

# Dictionary mapping Chinese terms to English translations
translations = {
    "Research Dashboard 文档": "Modular Dashboard Documentation",
    "欢迎阅读 Research Dashboard 文档。本指南将帮助您了解如何安装、配置和使用 Research Dashboard 应用程序。": "Welcome to the Modular Dashboard documentation. This guide will help you understand how to install, configure, and use the Modular Dashboard application.",
    "目录": "Table of Contents",
    "概述": "Overview",
    "安装": "Installation",
    "快速开始": "Getting Started",
    "配置": "Configuration",
    "布局系统": "Layout System",
    "打包": "Packaging",
    "模块": "Modules",
    "ArXiv 论文": "ArXiv Papers",
    "GitHub 活动": "GitHub Activity",
    "RSS 订阅": "RSS Feeds",
    "API 参考": "API Reference",
    "模块基类": "Module Base",
    "开发": "Development",
    "项目结构": "Project Structure",
    "贡献": "Contributing",
    "关于 Research Dashboard": "About Modular Dashboard",
    "Research Dashboard 是一个为研究人员设计的可定制信息聚合仪表盘。它提供了一个统一的界面来查看和管理来自多个来源的信息，包括：": "Modular Dashboard is a customizable information aggregation dashboard. It provides a unified interface to view and manage information from multiple sources including:",
    "基于您研究兴趣的 ArXiv 论文": "ArXiv papers",
    "您的 GitHub 活动": "Your GitHub activity",
    "您最喜欢的来源的 RSS 订阅": "RSS feeds from your favorite sources",
    "仪表盘具有灵活的基于列的布局系统，允许您以最适合您工作流程的方式组织信息。": "The dashboard features a flexible column-based layout system that allows you to organize information in a way that best suits your workflow.",
    "功能特性": "Features",
    "多源信息聚合": "Multi-source Information Aggregation",
    "从 ArXiv、GitHub 和 RSS 订阅收集和显示信息": "Collect and display information from ArXiv, GitHub, and RSS feeds",
    "灵活的布局系统": "Flexible Layout System",
    "配置 1-3 列布局，可自定义列宽": "Configure 1-3 column layouts with customizable column widths",
    "基于模块的架构": "Module-based Architecture",
    "可扩展的系统，用于添加新的信息来源": "Extensible system for adding new information sources",
    "响应式设计": "Responsive Design",
    "在桌面和移动设备上都能正常工作": "Works on desktop and mobile devices",
    "浅色/深色主题": "Light/Dark Theme",
    "在浅色和深色配色方案之间切换": "Toggle between light and dark color schemes",
    "原生桌面支持": "Native Desktop Support",
    "作为原生桌面应用程序运行": "Run as a native desktop application",
    "获取帮助": "Getting Help",
    "如果您需要 Research Dashboard 方面的帮助，您可以：": "If you need help with Modular Dashboard, you can:",
    "查看本指南中的文档": "Check the documentation in this guide",
    "在 [GitHub 仓库](https://github.com/WayneXuCN/ModularDashboard) 上报告问题": "Report issues on the [GitHub repository](https://github.com/WayneXuCN/ModularDashboard)",
    "提交功能请求或建议": "Submit feature requests or suggestions",
    "有关开发相关的问题，请参阅 [开发](./development/index.md) 部分。": "For development-related questions, see the [Development](./development/index.md) section.",
}


def translate_file(file_path):
    """Translate a single file from Chinese to English."""
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Simple replacement-based translation
    for chinese, english in translations.items():
        content = content.replace(chinese, english)

    # Write translated content to the English directory
    en_file_path = file_path.replace("/docs/", "/docs/en/")
    os.makedirs(os.path.dirname(en_file_path), exist_ok=True)

    with open(en_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Translated {file_path} -> {en_file_path}")


def main():
    """Main function to translate all documentation files."""
    docs_dir = "/Volumes/Work/DevSpace/01_APP/ModularDashboard/docs"

    # Skip the 'en' directory itself
    for root, _dirs, files in os.walk(docs_dir):
        if "/docs/en/" in root:
            continue

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                translate_file(file_path)


if __name__ == "__main__":
    main()
