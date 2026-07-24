from __future__ import annotations
from pathlib import Path
from guardian.config.settings import Settings


def load_config(path: str | None = None) -> Settings:
    """Load config from YAML file, falling back to defaults."""
    import yaml

    settings = Settings()

    search_paths = [
        Path(path) if path else None,
        Path.cwd() / ".guardian.yaml",
        Path.cwd() / ".guardian.yml",
    ]

    for p in filter(None, search_paths):
        if p and p.exists():
            with open(p, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                for key, val in data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, val)
            break

    return settings
