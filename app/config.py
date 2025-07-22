import os
import yaml
from functools import lru_cache


_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")


@lru_cache()
def load_config(path: str = _CONFIG_PATH) -> dict:
    """Load YAML configuration from ``config.yml`` once."""
    with open(path, "r") as fh:
        return yaml.safe_load(fh)
