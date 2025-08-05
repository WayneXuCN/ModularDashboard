"""Memory configuration example for the dashboard."""

from src.modular_dashboard.config.memory_config import MemoryConfig

# Example memory configuration for production use
PRODUCTION_MEMORY_CONFIG = MemoryConfig(
    max_cache_size=1000,  # Maximum 1000 cached items
    cache_ttl_seconds=3600,  # Cache expires after 1 hour
    max_memory_mb=512,  # Maximum 512MB memory usage
    compression_enabled=True,  # Enable compression for large objects
    compression_threshold_kb=100,  # Compress objects >100KB
    cleanup_interval_seconds=300,  # Clean up every 5 minutes
    enable_memory_monitoring=True,  # Enable memory monitoring
    enable_weak_references=True,  # Use weak references for cache
    memory_warning_threshold_mb=400,  # Warning at 400MB usage
    memory_error_threshold_mb=450,  # Error at 450MB usage
)

# Example memory configuration for development use
DEVELOPMENT_MEMORY_CONFIG = MemoryConfig(
    max_cache_size=100,  # Smaller cache for development
    cache_ttl_seconds=300,  # Shorter TTL for testing
    max_memory_mb=128,  # Lower memory limit
    compression_enabled=False,  # Disable compression for easier debugging
    compression_threshold_kb=1000,  # Higher threshold
    cleanup_interval_seconds=60,  # More frequent cleanup
    enable_memory_monitoring=True,
    enable_weak_references=True,
    memory_warning_threshold_mb=100,
    memory_error_threshold_mb=120,
)

# Example memory configuration for testing (minimal)
TEST_MEMORY_CONFIG = MemoryConfig(
    max_cache_size=10,
    cache_ttl_seconds=30,
    max_memory_mb=32,
    compression_enabled=False,
    compression_threshold_kb=1000,
    cleanup_interval_seconds=10,
    enable_memory_monitoring=True,
    enable_weak_references=False,  # Disable weak references for testing
    memory_warning_threshold_mb=25,
    memory_error_threshold_mb=30,
)

# Usage example in config.yaml:
# memory:
#   max_cache_size: 1000
#   cache_ttl_seconds: 3600
#   max_memory_mb: 512
#   compression_enabled: true
#   compression_threshold_kb: 100
#   cleanup_interval_seconds: 300
#   enable_memory_monitoring: true
#   enable_weak_references: true
#   memory_warning_threshold_mb: 400
#   memory_error_threshold_mb: 450