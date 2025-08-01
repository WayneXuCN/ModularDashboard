# GitHub Activity

**ID**: `github`

**Icon**: 🐙

**Description**: Your recent GitHub activity

## Data Format

This module provides data in the following standardized format:

```json
{
  "title": "string",
  "summary": "string",
  "link": "string (URL)",
  "published": "string (ISO8601)",
  "tags": "List[string]",
  "extra": "Dict (optional additional fields)"
}
```

## Example Data

Here's an example of the data provided by this module:

```json
{
  "title": "New commit in research-dashboard",
  "summary": "Added support for native desktop app mode",
  "link": "https://github.com/WayneXuCN/ResearchDashboard/commit/abc123",
  "published": "2025-07-30T15:30:00Z",
  "tags": [
    "commit",
    "research-dashboard"
  ],
  "extra": {
    "author": "dev-user"
  }
}
```
