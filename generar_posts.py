import os
import json
import markdown
import re
from datetime import datetime

MD_DIR = "posts_md"
HTML_DIR = "blog"
OUTPUT_FILE = os.path.join(HTML_DIR, "posts.json")

def md_to_html_and_meta(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    md = markdown.Markdown(extensions=[
        'meta',
        'extra',            # añade tablas, listas de definición, notes...
        'codehilite',       # opcional: resaltado de código
        'fenced_code',      # soporte a ```bloques de código```
    ])
    html_content = md.convert(md_content)
    meta = getattr(md, 'Meta', {})
    print("=== DEBUG HTML ===")
    print(html_content[:400])
    print("==================")
    return html_content, meta

def extract_title_excerpt(html):
    # title_match = re.search(r"<h1.*?>(.*?)</h1>", html, re.IGNORECASE)
    # para_match = re.search(r"<p>(.*?)</p>", html, re.IGNORECASE)
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    para_match  = re.search(r"<p[^>]*>([\s\S]*?)</p>", html, re.IGNORECASE | re.DOTALL)
    if not title_match or not para_match:
        return None, None
    return title_match.group(1).strip(), para_match.group(1).strip()

def load_projects():
    projects = []

    for file in sorted(os.listdir("proyectos_md/")):
        if not file.endswith(".md"):
            continue

        path = os.path.join("proyectos_md", file)

        with open(path, encoding="utf-8") as f:
            md_text = f.read()

        html, meta = md_to_html_and_meta(md_text)

        projects.append({
            "title": meta.get("title", [""])[0],
            "link": meta.get("link", [""])[0],
            "image": meta.get("image", [""])[0],
            "description": html
        })

    return projects

def generate_projects_page(projects):

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

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Proyectos interesantes</title>
<link rel="stylesheet" href="/css/mono-reset.css">
<link rel="stylesheet" href="/css/mono.css">
<link rel="stylesheet" href="/css/projects.css">
</head>
<body>

<header>PUNTERO CRUDO*</header>

<main>
<h2>Proyectos interesantes</h2>
{blocks}
<br><br>
</main>

<footer>
    <p>&copy; 2025 Puntero Crudo</p>
    <p>Style and Design: <a
                             href="https://owickstrom.github.io/the-monospace-web">Monospace
                             Web</a> by Oskar Wickström (@owickstrom)</p>
</footer>

</body>
</html>
"""

    os.makedirs("proyectos", exist_ok=True)

    with open("proyectos/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    posts = []

    for file in os.listdir(MD_DIR):
        if file.endswith(".md"):
            md_path = os.path.join(MD_DIR, file)
            base_name = os.path.splitext(file)[0]
            html_path = os.path.join(HTML_DIR, base_name + ".html")

            html_content, meta = md_to_html_and_meta(md_path)
            title, excerpt = extract_title_excerpt(html_content)

            # Tomar la fecha del meta; si no hay, usar la de modificación
            date_str = None
            if meta and 'date' in meta:
                # md.Meta devuelve listas de valores; cogemos el primero
                date_str = meta['date'][0]
            if not date_str:
                timestamp = os.path.getmtime(md_path)
                date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            if not title or not excerpt:
                print(f"⚠️  Error en '{file}', sin título o párrafo.")
                continue
# TODO el siguiente bloque hardcode estilo y estructura HTML. Probablemente 
# querre cambiar esto y que lea el patron de algun sitio.
# TODO despues del titulo, define el css que vamos a usar. Mejor cambiar esto a
# algo variable o algo asi.
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
                     <html lang="es">
                     <head>
                         <meta charset="UTF-8">
                         <meta name="viewport" content="width=device-width, initial-scale=1">
                         <title>{title}</title>
                         <link rel="stylesheet" href="/css/mono-reset.css">
                         <link rel="stylesheet" href="/css/mono.css">
                     </head>
                     <body>
                         <section class="post">
                     {html_content}
                         <hr>
                         <p><a href="/blog/">← Volver al blog</a> · <a href="/">Inicio</a></p>
                         </section>
                     </body>
                     </html>
                     """)
            # Esto crea el set de titulo y resumen de la entrada con el link.
            posts.append({
                "title": title,
                "date": date_str,
                "url": base_name + ".html",
                "excerpt": excerpt
            })
    # Esto ordena esa lista por fecha de creacion original (en el encabezado del
    # post markdown. De esta forma, se presenta el ultimo escrito el primero en
    # la pagina.
    posts.sort(key=lambda x: x["date"], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"✅ Generados {len(posts)} artículos y actualizado '{OUTPUT_FILE}'.")

    projects = load_projects()
    generate_projects_page(projects)

if __name__ == "__main__":
    main()

