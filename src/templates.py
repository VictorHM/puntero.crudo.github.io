from typing import List, Dict


def render_nav(site_name: str, nav_items: List[Dict]) -> str:
    """Render navigation header."""
    links = "\n".join(
        f'      <a href="{item["href"]}">{item["label"]}</a>'
        for item in nav_items
    )
    return f"""  <header>
    <h1>{site_name}</h1>
    <nav>
{links}
    </nav>
  </header>"""


def render_footer(author: str, year: int) -> str:
    """Render page footer."""
    return f"""  <footer>
    <p>&copy; {year} {author}</p>
    <p>Style and Design: <a href="https://owickstrom.github.io/the-monospace-web">Monospace Web</a> by Oskar Wickström (@owickstrom)</p>
  </footer>"""


def render_page(title: str, main_content: str, nav_html: str, footer_html: str) -> str:
    """Render complete HTML page."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="/css/mono-reset.css">
  <link rel="stylesheet" href="/css/mono.css">
</head>
<body>
{nav_html}

  <main>
{main_content}
  </main>

{footer_html}
</body>
</html>
"""
