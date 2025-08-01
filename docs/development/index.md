# Development Guide

This guide provides information for developers working on the Research Dashboard.

## Project Structure

```
research-dashboard/
│
├── pyproject.toml             # Project configuration
├── README.md                  # Project overview
├── LICENSE                    # License information
├── .gitignore                 # Git ignore patterns
│
├── src/
│   └── research_dashboard/    # Main source code
│       ├── __init__.py
│       ├── __main__.py        # Entry point
│       ├── main.py            # Main application logic
│       │
│       ├── config/            # Configuration system
│       ├── modules/           # Module system
│       ├── ui/                # User interface components
│       ├── static/            # Static assets
│       ├── utils/             # Utility functions
│       └── assets/            # Application assets
│
├── config/                    # User configuration
├── scripts/                   # Utility scripts
├── tests/                     # Test suite
└── docs/                      # Documentation
```

## Getting Started

1. Install dependencies:
   ```bash
   uv pip install -e .
   ```

2. Run the application:
   ```bash
   uv run -m research_dashboard
   ```

3. Run as native desktop app:
   ```bash
   uv run -m research_dashboard --native
   ```
