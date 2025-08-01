# RSS Feeds

**ID**: `rss`

**Icon**: 📡

**Description**: Latest items from your RSS feeds

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
  "title": "Python 3.13 Release Candidate",
  "summary": "The Python development team has announced the first release candidate for Python 3.13.",
  "link": "https://example.com/python-313-rc1",
  "published": "2025-07-30T12:00:00Z",
  "tags": [
    "python",
    "release"
  ],
  "extra": {
    "source": "Python Insider"
  }
}
```
