import os
import json
from datetime import datetime
from typing import List, Dict, Any
from .base import SectionGenerator
from ..markdown_processor import process_markdown, extract_title_excerpt, get_metadata_field
from ..templates import render_page, render_nav, render_footer


class BlogGenerator(SectionGenerator):
    """Generate blog posts from markdown files."""

    def generate(self) -> List[Dict[str, Any]]:
        """Generate blog posts and return metadata list."""
        self.ensure_output_dir()
        posts = []
        errors = []

        for file in os.listdir(self.input_dir):
            if not file.endswith(".md"):
                continue

            md_path = os.path.join(self.input_dir, file)
            base_name = os.path.splitext(file)[0]
            html_path = os.path.join(self.output_dir, base_name + ".html")

            try:
                # Process markdown
                html_content, metadata = process_markdown(md_path)
                title, excerpt = extract_title_excerpt(html_content)

                # Get date from metadata or file mtime
                date_str = get_metadata_field(metadata, "date")
                if not date_str:
                    timestamp = os.path.getmtime(md_path)
                    date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

                if not title or not excerpt:
                    error_msg = f"Skipping '{file}': missing "
                    if not title:
                        error_msg += "title "
                    if not excerpt:
                        error_msg += "excerpt"
                    errors.append(error_msg.strip())
                    continue

                # Render page
                main_content = f"""    <section class="post">
                {html_content}
                <hr>
                <p><a href="/blog/">&larr; Volver al blog</a> &middot; <a href="/">Inicio</a></p>
                </section>
            """
                nav_html = render_nav(
                    self.site_config["name"],
                    self.site_config["navigation"],
                )
                footer_html = render_footer(
                    self.site_config["author"],
                    self.site_config["year"],
                )
                page_html = render_page(title, main_content, nav_html, footer_html)

                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page_html)

                posts.append({
                    "title": title,
                    "date": date_str,
                    "url": base_name + ".html",
                    "excerpt": excerpt,
                })

            except Exception as e:
                errors.append(f"Error rendering '{file}': {str(e)}")
                continue

        # Report any errors
        if errors:
            print(f"\n⚠️  Blog generation encountered {len(errors)} issue(s):")
            for error in errors:
                print(f"   - {error}")

        # Sort by date descending
        posts.sort(key=lambda x: x["date"], reverse=True)

        # Save posts.json
        output_json = os.path.join(self.output_dir, "posts.json")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f"✅ Generated {len(posts)} blog posts")
        return posts

    def generate_index(self, posts: List[Dict[str, Any]]):
        """Generate blog index page."""
        blocks = ""
        for p in posts:
            blocks += f"""
        <article>
            <h3><a href="/blog/{p['url']}">{p['title']}</a></h3>
            <small>{p['date']}</small>
            <p>{p['excerpt']}</p>
        </article>
        """

        main_content = f"""
        <h2>Artículos recientes</h2>
        {blocks}
    """
        nav_html = render_nav(
            self.site_config["name"],
            self.site_config["navigation"],
        )
        footer_html = render_footer(
            self.site_config["author"],
            self.site_config["year"],
        )
        page_html = render_page("Blog", main_content, nav_html, footer_html)

        index_path = os.path.join(self.output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"✅ Generated blog index page")
