#!/bin/bash
# Cross-platform packaging script for Research Dashboard using Briefcase

set -e  # Exit on any error

echo "Research Dashboard Packaging Script (Briefcase)"
echo "=============================================="

# Detect platform
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')

# Function to package for macOS
package_macos() {
    echo "Packaging for macOS..."
    uv run briefcase create macOS
    uv run briefcase build macOS
    uv run briefcase package macOS
    echo "macOS package created in dist/ directory"
}

# Function to package for Linux
package_linux() {
    echo "Packaging for Linux..."
    uv run briefcase create linux
    uv run briefcase build linux
    uv run briefcase package linux
    echo "Linux package created in dist/ directory"
}

# Function to package for Windows (must be run on Windows)
package_windows() {
    echo "Packaging for Windows..."
    uv run briefcase create windows
    uv run briefcase build windows
    uv run briefcase package windows
    echo "Windows package created in dist/ directory"
}

# Package for all platforms
package_all() {
    echo "Packaging for all platforms..."
    package_macos
    package_linux
    # Note: Windows packaging must be done on Windows
    echo "Note: Windows packaging must be done on a Windows machine"
}

# Main logic
if [ "$1" = "--all" ]; then
    package_all
elif [ "$1" = "macos" ]; then
    package_macos
elif [ "$1" = "linux" ]; then
    package_linux
elif [ "$1" = "windows" ]; then
    package_windows
else
    # Package for current platform
    case $PLATFORM in
        darwin)
            package_macos
            ;;
        linux)
            package_linux
            ;;
        *)
            echo "Unsupported platform: $PLATFORM"
            exit 1
            ;;
    esac
fi

echo "Packaging completed successfully!"