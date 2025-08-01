# Packaging

Research Dashboard can be packaged as installable desktop applications for macOS, Windows, and Linux using PyInstaller with enhancements. The packaging script creates platform-specific distributable packages with installer-like features.

## Prerequisites

Before packaging, ensure you have the required dependencies installed:

```bash
uv pip install -e ".[packaging]"
```

## Packaging Script

The project includes an enhanced packaging script that automatically creates distributable packages:

```bash
# Package for the current platform
./scripts/package.sh

# The script will automatically detect the platform and create the appropriate package
```

## Platform-Specific Packages

The packaging script creates the following platform-specific distributable packages in the `dist/` directory:

- **macOS**: DMG installer with application bundle
- **Windows**: ZIP archive containing executable and assets
- **Linux**: TAR.GZ archive containing executable and assets (AppImage if tools available)

## Package Contents

Each package includes:
- The main executable/bundle
- All required assets and static files
- README and LICENSE files
- Platform-specific packaging format for easy distribution

## Customizing the Packaging Process

You can customize the packaging process by modifying the `scripts/package.sh` script.

## Distribution

After packaging, you can distribute the platform-specific packages directly to users. While not as full-featured as OS-specific installers, these packages provide a good balance between ease of distribution and user experience.