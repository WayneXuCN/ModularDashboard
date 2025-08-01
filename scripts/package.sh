#!/bin/bash
# Enhanced packaging script for Research Dashboard using PyInstaller
# Creates better cross-platform packages with installer-like features

set -e  # Exit on any error

echo "Research Dashboard Packaging Script (Enhanced)"
echo "============================================="

# Detect platform
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')

# Clean dist directory
echo "Cleaning dist directory..."
rm -rf dist

# Create dist directory
mkdir -p dist

# Function to package for macOS
package_macos() {
    echo "Packaging for macOS..."
    
    # Use PyInstaller to create app bundle
    uv run pyinstaller \
        --windowed \
        --name "Research Dashboard" \
        --icon src/research_dashboard/assets/app.iconset/icon_256x256.png \
        --add-data "src/research_dashboard/static:static" \
        --add-data "src/research_dashboard/assets:assets" \
        --hidden-import nicegui \
        --hidden-import requests \
        --hidden-import feedparser \
        --hidden-import arxiv \
        --hidden-import apscheduler \
        --hidden-import structlog \
        --hidden-import apscheduler.schedulers.asyncio \
        --hidden-import apscheduler.schedulers.background \
        --hidden-import apscheduler.jobstores.memory \
        --hidden-import apscheduler.executors.pool \
        src/research_dashboard/main.py
    
    # Create a distributable DMG for macOS
    if command -v hdiutil &> /dev/null; then
        echo "Creating DMG installer..."
        # Create temporary directory for DMG contents
        mkdir -p dist/dmg
        cp -r dist/"Research Dashboard.app" dist/dmg/
        
        # Create DMG
        hdiutil create -volname "Research Dashboard" \
            -srcfolder dist/dmg \
            -ov \
            -format UDZO \
            dist/research-dashboard-macos.dmg
        
        # Clean up
        rm -rf dist/dmg
        echo "macOS DMG installer created: dist/research-dashboard-macos.dmg"
    else
        # Just move the app bundle
        mv dist/"Research Dashboard.app" dist/research-dashboard-macos.app
        echo "macOS app bundle created: dist/research-dashboard-macos.app"
    fi
}

# Function to package for Linux
package_linux() {
    echo "Packaging for Linux..."
    
    # Use PyInstaller to create executable
    uv run pyinstaller \
        --windowed \
        --name "research-dashboard" \
        --add-data "src/research_dashboard/static:static" \
        --add-data "src/research_dashboard/assets:assets" \
        --hidden-import nicegui \
        --hidden-import requests \
        --hidden-import feedparser \
        --hidden-import arxiv \
        --hidden-import apscheduler \
        --hidden-import structlog \
        --hidden-import apscheduler.schedulers.asyncio \
        --hidden-import apscheduler.schedulers.background \
        --hidden-import apscheduler.jobstores.memory \
        --hidden-import apscheduler.executors.pool \
        src/research_dashboard/main.py
    
    # Create AppImage for Linux if tools are available
    if command -v appimagetool &> /dev/null; then
        echo "Creating AppImage..."
        # Create AppDir structure
        mkdir -p dist/AppDir/usr/bin
        mkdir -p dist/AppDir/usr/share/icons
        mkdir -p dist/AppDir/usr/share/applications
        
        # Copy executable
        cp dist/research-dashboard dist/AppDir/usr/bin/
        
        # Copy assets
        cp -r src/research_dashboard/assets dist/AppDir/usr/share/
        cp -r src/research_dashboard/static dist/AppDir/usr/share/
        
        # Create desktop entry
        cat > dist/AppDir/usr/share/applications/research-dashboard.desktop << EOF
[Desktop Entry]
Name=Research Dashboard
Exec=research-dashboard
Icon=research-dashboard
Type=Application
Categories=Utility;
EOF
        
        # Create AppImage
        appimagetool dist/AppDir dist/research-dashboard-linux.AppImage
        echo "Linux AppImage created: dist/research-dashboard-linux.AppImage"
        
        # Clean up
        rm -rf dist/AppDir
    else
        # Create a tar.gz package
        echo "Creating tar.gz package..."
        # Create package directory
        mkdir -p dist/research-dashboard-linux
        cp dist/research-dashboard dist/research-dashboard-linux/
        cp -r src/research_dashboard/assets dist/research-dashboard-linux/
        cp -r src/research_dashboard/static dist/research-dashboard-linux/
        cp README.md dist/research-dashboard-linux/
        cp LICENSE dist/research-dashboard-linux/
        
        # Create tar.gz
        tar -czf dist/research-dashboard-linux.tar.gz -C dist research-dashboard-linux
        
        # Clean up
        rm -rf dist/research-dashboard-linux
        echo "Linux tar.gz package created: dist/research-dashboard-linux.tar.gz"
    fi
}

# Function to package for Windows
package_windows() {
    echo "Packaging for Windows..."
    
    # Use PyInstaller to create executable
    uv run pyinstaller \
        --windowed \
        --name "research-dashboard" \
        --icon src/research_dashboard/assets/app.iconset/icon_256x256.png \
        --add-data "src/research_dashboard/static;static" \
        --add-data "src/research_dashboard/assets;assets" \
        --hidden-import nicegui \
        --hidden-import requests \
        --hidden-import feedparser \
        --hidden-import arxiv \
        --hidden-import apscheduler \
        --hidden-import structlog \
        --hidden-import apscheduler.schedulers.asyncio \
        --hidden-import apscheduler.schedulers.background \
        --hidden-import apscheduler.jobstores.memory \
        --hidden-import apscheduler.executors.pool \
        src/research_dashboard/main.py
    
    # Create a zip package for Windows
    echo "Creating zip package..."
    # Create package directory
    mkdir -p dist/research-dashboard-windows
    cp dist/research-dashboard.exe dist/research-dashboard-windows/
    cp -r src/research_dashboard/assets dist/research-dashboard-windows/
    cp -r src/research_dashboard/static dist/research-dashboard-windows/
    cp README.md dist/research-dashboard-windows/
    cp LICENSE dist/research-dashboard-windows/
    
    # Create zip
    (cd dist && zip -r research-dashboard-windows.zip research-dashboard-windows)
    
    # Clean up
    rm -rf dist/research-dashboard-windows
    echo "Windows zip package created: dist/research-dashboard-windows.zip"
}

# Main logic
case $PLATFORM in
    darwin)
        package_macos
        ;;
    linux)
        package_linux
        ;;
    mingw*|cygwin*|msys*)
        package_windows
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

echo "Packaging completed successfully!"