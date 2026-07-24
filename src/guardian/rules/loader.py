from __future__ import annotations
from pathlib import Path


def load_rules(paths: list[str] | None = None) -> list[dict]:
    """Load rule definitions from YAML files."""
    import yaml
    rules = []

    search = paths or []
    presets_dir = Path(__file__).parent / "presets"
    if presets_dir.exists():
        search.extend(str(f) for f in presets_dir.glob("*.yaml"))

    for p in search:
        fpath = Path(p)
        if fpath.exists():
            with open(fpath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data and "rules" in data:
                rules.extend(data["rules"])
    return rules
