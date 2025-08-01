# API Documentation

This section documents the internal APIs of the Research Dashboard.

## Configuration API

The configuration system is managed through the following components:

- `config.manager` - Functions for loading and saving configuration
- `config.schema` - Data classes defining the configuration structure

## Module API

Modules implement a standardized interface defined in `modules.base.Module`:

```python
class Module(ABC):
    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def icon(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def render(self) -> None: ...

    def render_detail(self) -> None: ...
```
