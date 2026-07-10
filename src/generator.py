"""Main orchestrator for blog generation."""
from typing import Dict, Any
from .config import load_config
from .models import SiteConfig, Section
from .generators.blog import BlogGenerator
from .generators.projects import ProjectsGenerator


def get_generator_for_section(section: Section, site_config: Dict[str, Any]):
    """Get the appropriate generator for a section type."""
    generators = {
        "blog": BlogGenerator,
        "projects": ProjectsGenerator,
    }
    generator_class = generators.get(section.type)
    if not generator_class:
        raise ValueError(f"Unknown section type: {section.type}")
    return generator_class(section, site_config)


def generate_all(config_path: str = "config.yaml", output_base: str = "output") -> Dict[str, Any]:
    """Generate all sections."""
    config = load_config(config_path, output_base)

    # Convert config to dict for easier passing to generators
    site_config = {
        "name": config.name,
        "author": config.author,
        "year": config.year,
        "navigation": config.navigation,
    }

    results = {}

    print(f"🚀 Generating blog for {config.name}...")

    for section in config.sections:
        print(f"\n📝 Processing section: {section.name}")
        try:
            generator = get_generator_for_section(section, site_config)
            items = generator.generate()
            results[section.type] = items

            # Generate index page for this section
            if section.type == "blog":
                generator.generate_index(items)
            elif section.type == "projects":
                generator.generate_index(items)

        except Exception as e:
            print(f"❌ Error processing section '{section.name}': {str(e)}")
            raise

    print(f"\n✨ Generation complete!")
    return results
