# Configuration

Research Dashboard is configured through a JSON file located at `config/user-config.json`. 

## Configuration Structure

The configuration file has the following structure:

```json
{
  "version": "0.1.0",
  "theme": "light",
  "layout": {
    "columns": 3,
    "view": "grid",
    "card_size": "medium"
  },
  "modules": [
    {
      "id": "arxiv",
      "enabled": true,
      "position": 1,
      "collapsed": false,
      "refresh_interval": 3600,
      "config": {}
    }
  ]
}
```

## Theme Configuration

- `theme`: Can be either "light" or "dark"

## Layout Configuration

- `columns`: Number of columns in the grid (1-4)
- `view`: Display view ("grid" or "list")
- `card_size`: Size of cards ("small", "medium", "large")

## Module Configuration

Each module has the following configuration options:

- `id`: Unique identifier for the module
- `enabled`: Whether the module is enabled
- `position`: Position in the grid (lower numbers appear first)
- `collapsed`: Whether the module is initially collapsed
- `refresh_interval`: Refresh interval in seconds
- `config`: Module-specific configuration options

## Example Configuration

Here's an example configuration with all default modules enabled:

```json
{
  "version": "0.1.0",
  "theme": "light",
  "layout": {
    "columns": 3,
    "view": "grid",
    "card_size": "medium"
  },
  "modules": [
    {
      "id": "arxiv",
      "enabled": true,
      "position": 1,
      "collapsed": false,
      "refresh_interval": 3600,
      "config": {}
    },
    {
      "id": "github",
      "enabled": true,
      "position": 2,
      "collapsed": false,
      "refresh_interval": 3600,
      "config": {}
    },
    {
      "id": "rss",
      "enabled": true,
      "position": 3,
      "collapsed": false,
      "refresh_interval": 3600,
      "config": {}
    }
  ]
}
```