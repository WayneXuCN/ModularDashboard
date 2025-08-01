#!/usr/bin/env python3
"""
Package the Research Dashboard as a standalone application.
"""

import os
import shutil
import sys
from pathlib import Path


def create_app_bundle():
    """Create a macOS application bundle."""
    # Create the app bundle structure
    app_name = "ResearchDashboard.app"
    app_dir = Path("dist") / app_name
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"

    # Remove existing app bundle
    if app_dir.exists():
        shutil.rmtree(app_dir)

    # Create directories
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    # Create Info.plist
    info_plist = contents_dir / "Info.plist"
    info_plist.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleExecutable</key>
    <string>ResearchDashboard</string>
    <key>CFBundleGetInfoString</key>
    <string>Research Dashboard</string>
    <key>CFBundleIconFile</key>
    <string>app.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.researchdashboard.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Research Dashboard</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.0</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>0.1.0</string>
    <key>NSAppleScriptEnabled</key>
    <string>YES</string>
    <key>NSMainNibFile</key>
    <string>MainMenu</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
""")

    # Copy the Python script as the executable
    executable = macos_dir / "ResearchDashboard"
    shutil.copy("src/research_dashboard/main.py", executable)

    # Make it executable
    os.chmod(executable, 0o755)

    # Create a simple launcher script
    launcher_script = macos_dir / "ResearchDashboard"
    launcher_script.write_text("""#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_PATH="$(which python3)"
if [ -z "$PYTHON_PATH" ]; then
    PYTHON_PATH="/usr/bin/python3"
fi

# Set the working directory to the Resources folder
cd "$DIR/../Resources"

# Run the main application with native flag
"$PYTHON_PATH" "$DIR/../Resources/main.py" --native
""")

    # Make launcher executable
    os.chmod(launcher_script, 0o755)

    # Copy the source code to Resources
    shutil.copytree("src", resources_dir / "src")
    shutil.copy("pyproject.toml", resources_dir)
    shutil.copy("README.md", resources_dir)

    # Create a basic icon file (in a real app, you'd use a proper .icns file)
    # For now, we'll just create an empty file
    (resources_dir / "app.icns").touch()

    print(f"Created app bundle at {app_dir}")


def main():
    """Main function."""
    try:
        create_app_bundle()
        print("Successfully created macOS application bundle!")
    except Exception as e:
        print(f"Error creating app bundle: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
