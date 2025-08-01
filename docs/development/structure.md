# Project Structure

Research Dashboard follows a modular project structure designed for extensibility and maintainability.

## Directory Structure

```
research-dashboard/
│
├── pyproject.toml              # Project configuration
├── README.md                   # Project overview
├── LICENSE                     # License information
├── .gitignore                  # Git ignore patterns
├── mkdocs.yml                  # Documentation configuration
│
├── src/
│   └── research_dashboard/     # Main source code
│       ├── __init__.py
│       ├── __main__.py         # Entry point
│       ├── main.py             # Main application logic
│       │
│       ├── config/             # Configuration system
│       │   ├── __init__.py
│       │   ├── manager.py      # Load/save configuration
│       │   └── schema.py       # Configuration data classes
│       │
│       ├── modules/            # Module system
│       │   ├── __init__.py
│       │   ├── base.py         # Module base class
│       │   ├── registry.py     # Module registry
│       │   │
│       │   ├── arxiv/          # ArXiv module
│       │   │   ├── __init__.py
│       │   │   ├── module.py   # Module implementation
│       │   │   └── fetcher.py  # Data fetching logic
│       │   │
│       │   ├── github/         # GitHub module
│       │   │   ├── __init__.py
│       │   │   ├── module.py
│       │   │   └── fetcher.py
│       │   │
│       │   ├── rss/            # RSS module
│       │   │   ├── __init__.py
│       │   │   ├── module.py
│       │   │   └── fetcher.py
│       │   │
│       │   └── ...             # Other modules
│       │
│       ├── ui/                 # User interface components
│       │   ├── __init__.py
│       │   ├── dashboard.py    # Main dashboard layout
│       │   └── components.py   # Reusable UI components
│       │
│       ├── static/             # Static assets
│       │   ├── css/
│       │   │   └── style.css   # Custom styles
│       │   └── icons/          # SVG icons
│       │
│       ├── utils/              # Utility functions
│       │   ├── __init__.py
│       │   ├── logger.py       # Logging configuration
│       │   └── helpers.py      # Helper functions
│       │
│       ├── assets/             # Application assets
│       │   └── default-config.json  # Default configuration
│       │
│       └── docs/               # Documentation generation
│           └── generator.py    # Documentation generator
│
├── config/                     # User configuration (runtime)
│   └── user-config.json
│
├── scripts/                    # Utility scripts
│   ├── package.py              # Application packaging
│   └── generate_docs.py        # Documentation generation CLI
│
├── tests/                      # Test suite
│   ├── test_config.py
│   └── test_modules.py
│
├── docs/                       # Documentation source
│   ├── index.md                # Documentation home
│   ├── README.md               # Copy of project README
│   ├── user-guide/             # User guides
│   ├── modules/                # Module documentation
│   ├── api/                    # API reference
│   └── development/            # Development documentation
│
└── dist/                       # Build output
```

## Key Directories

### src/research_dashboard/

This is the main source code directory containing all Python modules.

### config/

This directory contains the user's configuration file, which is created on first run and can be modified to customize the dashboard.

### scripts/

This directory contains utility scripts for packaging and documentation generation.

### docs/

This directory contains the source files for the documentation website, which can be built using MkDocs.

### tests/

This directory contains the test suite for the application.