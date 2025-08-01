#!/usr/bin/env python3
"""
Cross-platform packaging script for Research Dashboard using Briefcase.
Creates installable packages for macOS, Windows, and Linux.
"""

import platform
import subprocess
import sys


def package_for_platform(target_platform=None):
    """Package the application for the specified platform."""
    if target_platform is None:
        target_platform = platform.system().lower()

    print(f"Packaging for {target_platform}...")

    # Map platform names to Briefcase commands
    platform_commands = {"darwin": "macOS", "windows": "windows", "linux": "linux"}

    if target_platform not in platform_commands:
        print(f"Unsupported platform: {target_platform}")
        return False

    briefcase_platform = platform_commands[target_platform]

    try:
        # Create the application package
        subprocess.run(
            [sys.executable, "-m", "briefcase", "create", briefcase_platform],
            check=True,
        )

        # Build the installer
        subprocess.run(
            [sys.executable, "-m", "briefcase", "build", briefcase_platform], check=True
        )

        # Package the installer
        subprocess.run(
            [sys.executable, "-m", "briefcase", "package", briefcase_platform],
            check=True,
        )

        print(f"Successfully created package for {target_platform}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during packaging: {e}")
        return False


def package_all_platforms():
    """Package for all platforms."""
    platforms = ["darwin", "windows", "linux"]
    for plat in platforms:
        print(f"\n--- Packaging for {plat} ---")
        if not package_for_platform(plat):
            print(f"Failed to package for {plat}")
            return False
    return True


def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
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


if __name__ == "__main__":
    main()
