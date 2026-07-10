import os
from typing import List, Dict, Any
from .base import SectionGenerator
from ..markdown_processor import process_markdown, get_metadata_field
from ..templates import render_page, render_nav, render_footer


class ProjectsGenerator(SectionGenerator):
    """Generate projects page from markdown files."""

    def generate(self) -> List[Dict[str, Any]]:
        """Generate projects and return metadata list."""
        self.ensure_output_dir()
        projects = []

        for file in sorted(os.listdir(self.input_dir)):
            if not file.endswith(".md"):
                continue

            path = os.path.join(self.input_dir, file)

            # Process markdown
            html_content, metadata = process_markdown(path)

            title = get_metadata_field(metadata, "title")
            link = get_metadata_field(metadata, "link")
            image = get_metadata_field(metadata, "image")

            if not title or not link:
                print(f"⚠️  Skipping '{file}': missing title or link")
                continue

            projects.append({
                "title": title,
                "link": link,
                "image": image,
                "description": html_content,
            })

        self.generate_index(projects)
        print(f"✅ Generated {len(projects)} projects")
        return projects

    def generate_index(self, projects: List[Dict[str, Any]]):
        """Generate projects index page."""
        blocks = ""
        for p in projects:
            blocks += f"""
        <article class="project-card">
            <img src="{p['image']}" alt="">
            <div>
                <h3><a href="{p['link']}">{p['title']}</a></h3>
                {p['description']}
            </div>
        </article>
        """

        main_content = f"""
        <h2>Proyectos interesantes</h2>
        {blocks}
        <br><br>
    """
        nav_html = render_nav(
            self.site_config["name"],
            self.site_config["navigation"],
        )
        footer_html = render_footer(
            self.site_config["author"],
            self.site_config["year"],
        )
        page_html = render_page("Proyectos", main_content, nav_html, footer_html)

        index_path = os.path.join(self.output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"✅ Generated projects index page")
