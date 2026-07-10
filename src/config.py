import yaml
import os
from .models import SiteConfig, Section


def load_config(config_path: str = "config.yaml", output_base: str = "output") -> SiteConfig:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    site_data = raw_config.get("site", {})
    navigation = raw_config.get("navigation", [])
    sections_data = raw_config.get("sections", [])

    sections = [
        Section(
            name=s.get("name"),
            path=s.get("path"),
            input_dir=s.get("input_dir"),
            output_dir=os.path.join(output_base, s.get("output_dir")),
            type=s.get("type"),
            description=s.get("description", ""),
        )
        for s in sections_data
    ]

    return SiteConfig(
        name=site_data.get("name"),
        description=site_data.get("description", ""),
        author=site_data.get("author"),
        year=site_data.get("year"),
        navigation=navigation,
        sections=sections,
    )
