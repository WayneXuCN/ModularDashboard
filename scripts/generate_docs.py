"""Command-line interface for documentation generation."""

import argparse
import os
import sys

# Add src to path so we can import from modular_dashboard
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.modular_dashboard.docs.generator import generate_documentation


def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation for Modular Dashboard"
    )
    parser.add_argument(
        "--output", "-o", default="docs", help="Output directory for documentation"
    )

    args = parser.parse_args()

    try:
        generate_documentation()
        print(f"Documentation generated successfully in {args.output}/")
    except Exception as e:
        print(f"Error generating documentation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
