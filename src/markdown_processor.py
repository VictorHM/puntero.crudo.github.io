import markdown
import re
from typing import Tuple, Dict, Any


def process_markdown(md_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Process markdown file and extract HTML content and metadata.

    Returns:
        Tuple of (html_content, metadata_dict)
    """
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    md = markdown.Markdown(
        extensions=[
            "meta",
            "extra",
            "codehilite",
            "fenced_code",
        ]
    )
    html_content = md.convert(md_content)
    metadata = getattr(md, "Meta", {})

    return html_content, metadata


def extract_title_excerpt(html: str) -> Tuple[str, str]:
    """
    Extract title (first h1) and excerpt (first paragraph) from HTML.

    Returns:
        Tuple of (title, excerpt) or (None, None) if not found
    """
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    para_match = re.search(r"<p[^>]*>([\s\S]*?)</p>", html, re.IGNORECASE | re.DOTALL)

    if not title_match or not para_match:
        return None, None

    # Remove img tags from excerpt
    excerpt = re.sub(r"<img\b[^>]*>", "", para_match.group(1), flags=re.IGNORECASE)

    return title_match.group(1).strip(), excerpt.strip()


def get_metadata_field(metadata: Dict, key: str, default: str = "") -> str:
    """
    Get a metadata field, handling the format where metadata values are lists.
    """
    if key in metadata:
        value = metadata[key]
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return str(value) if value else default
    return default
