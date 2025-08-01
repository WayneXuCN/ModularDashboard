# Installation

This guide will help you install Research Dashboard on your system.

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation with uv (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/WayneXuCN/ResearchDashboard.git
   cd research-dashboard
   ```

2. Install dependencies:
   ```bash
   uv pip install -e .
   ```

## Installation with pip

1. Clone the repository:
   ```bash
   git clone https://github.com/WayneXuCN/ResearchDashboard.git
   cd research-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```