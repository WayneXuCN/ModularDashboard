# ArXiv Papers

**ID**: `arxiv`

**Icon**: 📚

**Description**: Latest papers from ArXiv based on your keywords

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
  "title": "Quantum Computing Advances",
  "summary": "Recent breakthroughs in quantum computing algorithms and hardware implementations.",
  "link": "https://arxiv.org/example1",
  "published": "2025-07-30T10:00:00Z",
  "tags": [
    "quantum",
    "computing"
  ],
  "extra": {
    "authors": [
      "Alice Johnson",
      "Bob Smith"
    ]
  }
}
```
