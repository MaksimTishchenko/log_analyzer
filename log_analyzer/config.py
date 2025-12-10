import json
from pathlib import Path

DEFAULT_CONFIG = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./logs",
}


def load_config(config_path: str | None = None) -> dict:
    """Load config from file and merge it with default config."""
    config = DEFAULT_CONFIG.copy()

    if not config_path:
        return config

    config_file = Path(config_path)
    if not config_file.exists():
        print(
            f"Warning: Config file not found: {config_path}. "
            f"Using default config."
        )
        return config

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            file_config = json.load(file)
        config.update(file_config)
    except json.JSONDecodeError:
        print(
            f"Warning: Invalid JSON in config file: {config_path}. "
            f"Using default config."
        )

    return config
