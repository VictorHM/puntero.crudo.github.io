"""Main orchestrator for blog generation."""
import os
import shutil
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


def copy_static_files(output_base: str = "output"):
    """Copy static files (css, js, assets, index.html) to output folder."""
    os.makedirs(output_base, exist_ok=True)

    static_files = ["index.html"]
    static_dirs = ["css", "js", "assets"]

    # Copy static files
    for file in static_files:
        if os.path.exists(file):
            dest = os.path.join(output_base, file)
            shutil.copy2(file, dest)

    # Copy static directories
    for dir_name in static_dirs:
        if os.path.exists(dir_name):
            dest = os.path.join(output_base, dir_name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(dir_name, dest)


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

    # Copy static files to output
    print(f"📋 Copying static files...")
    copy_static_files(output_base)

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
