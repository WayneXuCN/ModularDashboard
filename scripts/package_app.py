#!/usr/bin/env python3
"""
Cross-platform packaging script for Research Dashboard.
Supports macOS, Windows, and Linux.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def get_platform():
    """Get the current platform."""
    return platform.system().lower()

def create_spec_file():
    """Create a PyInstaller spec file for the application."""
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# Add the src directory to the path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

block_cipher = None

a = Analysis(
    ['src/research_dashboard/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/research_dashboard/static', 'static'),
        ('src/research_dashboard/assets', 'assets'),
    ],
    hiddenimports=[
        'nicegui',
        'requests',
        'feedparser',
        'arxiv',
        'APScheduler',
        'structlog',
        'research_dashboard',
        'research_dashboard.config',
        'research_dashboard.modules',
        'research_dashboard.modules.arxiv',
        'research_dashboard.modules.github',
        'research_dashboard.modules.rss',
        'research_dashboard.ui',
        'research_dashboard.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='research-dashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/research_dashboard/assets/app.iconset/icon_256x256.png' if sys.platform == 'darwin' else None,
)
'''
    
    with open('research-dashboard.spec', 'w') as f:
        f.write(spec_content)
    
    print("Created research-dashboard.spec")

def package_for_platform(target_platform=None):
    """Package the application for the specified platform."""
    if target_platform is None:
        target_platform = get_platform()
    
    print(f"Packing for {target_platform}...")
    
    # Create spec file if it doesn't exist
    if not os.path.exists('research-dashboard.spec'):
        create_spec_file()
    
    # Run PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'research-dashboard.spec'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully created package for {target_platform}")
        
        # Move the output to a platform-specific directory
        dist_dir = Path('dist')
        platform_dir = dist_dir / target_platform
        platform_dir.mkdir(exist_ok=True)
        
        # Move the built application
        if target_platform == 'darwin':  # macOS
            app_name = 'research-dashboard.app'
            if (dist_dir / app_name).exists():
                shutil.move(str(dist_dir / app_name), str(platform_dir / app_name))
        else:  # Windows or Linux
            exe_name = 'research-dashboard.exe' if target_platform == 'windows' else 'research-dashboard'
            if (dist_dir / exe_name).exists():
                shutil.move(str(dist_dir / exe_name), str(platform_dir / exe_name))
        
        print(f"Package moved to dist/{target_platform}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during packaging: {e}")
        return False

def package_all_platforms():
    """Package for all platforms."""
    platforms = ['darwin', 'windows', 'linux']
    for plat in platforms:
        print(f"\n--- Packaging for {plat} ---")
        if not package_for_platform(plat):
            print(f"Failed to package for {plat}")
            return False
    return True

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            success = package_all_platforms()
        else:
            success = package_for_platform(sys.argv[1])
    else:
        success = package_for_platform()
    
    if success:
        print("\nPackaging completed successfully!")
        print("Find your packages in the 'dist' directory.")
    else:
        print("\nPackaging failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()