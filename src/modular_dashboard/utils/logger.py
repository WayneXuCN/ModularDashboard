"""Logger utility."""

import structlog


def get_logger(name: str):
    """Get a configured logger instance."""
    return structlog.get_logger(name)
