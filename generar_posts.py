import os
import json
import markdown
import re
from datetime import datetime

MD_DIR = "posts_md"
HTML_DIR = "blog"
OUTPUT_FILE = os.path.join(HTML_DIR, "posts.json")

def md_to_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)
    return html_content

def extract_title_excerpt(html):
    title_match = re.search(r"<h1.*?>(.*?)</h1>", html, re.IGNORECASE)
    para_match = re.search(r"<p>(.*?)</p>", html, re.IGNORECASE)
    if not title_match or not para_match:
        return None, None
    return title_match.group(1).strip(), para_match.group(1).strip()

def main():
    posts = []

    for file in os.listdir(MD_DIR):
        if file.endswith(".md"):
            md_path = os.path.join(MD_DIR, file)
            base_name = os.path.splitext(file)[0]
            html_path = os.path.join(HTML_DIR, base_name + ".html")

            html_content = md_to_html(md_path)
            title, excerpt = extract_title_excerpt(html_content)
            if not title or not excerpt:
                print(f"⚠️  Error en '{file}', sin título o párrafo.")
                continue

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(
                    f"""<!DOCTYPE html>
            <html lang="es">
            <head>
              <meta charset="UTF-8">
              <title>{title}</title>
            </head>
            <body>
            {html_content}
            <hr>
            <p><a href="index.html">← Volver al blog</a></p>
            </body>
            </html>
            """)

            timestamp = os.path.getmtime(md_path)
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

            posts.append({
                "title": title,
                "date": date,
                "url": base_name + ".html",
                "excerpt": excerpt
            })

    posts.sort(key=lambda x: x["date"], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"✅ Generados {len(posts)} artículos y actualizado '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()

