# Getting Started

This guide will help you get started with Research Dashboard.

## Running the Application

After installation, you can run the application in two modes:

### Web Application Mode

```bash
uv run -m research_dashboard
```

This will start a web server and open the dashboard in your default browser.

### Native Desktop Application Mode

```bash
uv run -m research_dashboard --native
```

This will run the application as a native desktop app.

## Packaging the Application

To create standalone executables for macOS, Windows, and Linux, you can use the packaging script:

```bash
# Package for the current platform
./scripts/package.sh

# Or use the Python packaging script
uv run scripts/package_app.py
```

The packaged applications will be located in the `dist/` directory.

## Initial Configuration

On first run, the application will create a default configuration file at `config/user-config.json`. You can modify this file to customize your dashboard.

## Default Modules

The default configuration includes the following modules:

- **ArXiv Papers**: Latest papers from ArXiv based on your keywords
- **GitHub Activity**: Your recent GitHub activity
- **RSS Feeds**: Latest items from your RSS feeds

Each module can be enabled/disabled and configured independently.