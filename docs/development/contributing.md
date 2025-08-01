# Contributing

We welcome contributions to Research Dashboard! This guide will help you get started with contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/research-dashboard.git
   ```
3. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-or-bugfix-name
   ```

## Development Setup

1. Install dependencies:
   ```bash
   uv pip install -e .
   ```

2. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

## Code Style

We use the following tools to ensure code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Before submitting a pull request, please run:

```bash
black src/
flake8 src/
mypy src/
```

## Testing

We use pytest for testing. To run the test suite:

```bash
pytest
```

When adding new features, please include tests to ensure they work correctly.

## Documentation

When adding new features or modifying existing ones, please update the documentation accordingly. Documentation is written in Markdown and built using MkDocs.

To preview documentation changes:

```bash
mkdocs serve
```

## Pull Request Process

1. Ensure your code follows the project's coding standards
2. Add tests for any new functionality
3. Update documentation as needed
4. Submit a pull request with a clear description of your changes

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with as much detail as possible.