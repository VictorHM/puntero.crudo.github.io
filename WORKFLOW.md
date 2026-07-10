# Blog Build & Deployment Workflow

## Overview

```
Local Development                Server (punterocrudo.com)
┌─────────────────────┐          ┌──────────────────────┐
│ Source Code         │          │ /var/www/punterocrudo│
│ ├── posts_md/       │  build   │ ├── blog/            │
│ ├── proyectos_md/   │─────────>│ ├── css/             │
│ ├── src/            │  deploy  │ ├── js/              │
│ ├── css/            │─────────>│ ├── assets/          │
│ └── build.py        │  (rsync) │ └── index.html       │
└─────────────────────┘          └──────────────────────┘
```

## Daily Workflow

### 1. Write Content
Create markdown files in source folders:
```
posts_md/my-new-article.md
proyectos_md/interesting-project.md
```

### 2. Build Locally (Generate HTML)
```bash
python3 build.py
```

This generates:
```
output/
├── blog/
│   ├── index.html (listing page)
│   ├── my-new-article.html
│   └── posts.json (metadata)
└── proyectos/
    └── index.html
```

**Key points:**
- Source code NOT modified (only generated files)
- All output goes to `output/` folder
- Safe to run multiple times
- Can be committed to git separately or kept gitignored

### 3. Test Locally (Optional)
```bash
cd output
python3 -m http.server 8000
# Visit http://localhost:8000/blog/
```

### 4. Deploy to Server
```bash
./deploy.sh
```

This:
1. Runs `python3 build.py` again
2. Syncs `output/`, `css/`, `js/`, `assets/`, `index.html` to server
3. Preserves folder structure on server

---

## File Organization

### Source Files (Committed to Git)
```
.
├── config.yaml              # Site configuration
├── build.py                 # Build entry point
├── deploy.sh                # Deploy script
├── requirements.txt         # Python dependencies
├── src/                     # Generation code
│   ├── config.py
│   ├── generator.py
│   ├── markdown_processor.py
│   ├── models.py
│   ├── templates.py
│   └── generators/
│       ├── base.py
│       ├── blog.py
│       └── projects.py
├── posts_md/                # Blog article source
├── proyectos_md/            # Projects source
├── css/                     # Static stylesheets
├── js/                      # Static scripts
├── assets/                  # Images, etc
└── index.html               # Homepage (static)
```

### Generated Files (Gitignored)
```
output/                      # Everything here is generated
├── blog/
│   ├── *.html              # Individual posts
│   ├── index.html          # Blog listing
│   └── posts.json          # Post metadata
└── proyectos/
    └── index.html
```

### What Gets Deployed to Server
On server: `/var/www/punterocrudo/`
```
/var/www/punterocrudo/
├── blog/                    # From output/blog/
├── proyectos/               # From output/proyectos/
├── css/                     # From ./css/
├── js/                      # From ./js/
├── assets/                  # From ./assets/
└── index.html               # Homepage
```

---

## Configuration: `config.yaml`

Change site settings here (not in Python code):
```yaml
site:
  name: "Puntero Crudo*"
  author: "PunteroCrudo"
  year: 2025

navigation:
  - label: "Inicio"
    href: "/"
  - label: "Blog"
    href: "/blog/"

sections:
  - name: "Blog"
    path: "blog"
    input_dir: "posts_md"
    output_dir: "blog"
    type: "blog"
```

---

## Build Process Details

When you run `python3 build.py`:

1. **Load Config** → `src/config.py` reads `config.yaml`
2. **Process Sections** → For each section in config:
   - **Blog Section** → `src/generators/blog.py`
     - Reads all `.md` files from `posts_md/`
     - Extracts metadata (title, date, excerpt)
     - Converts markdown to HTML
     - Generates individual post pages: `output/blog/*.html`
     - Generates index: `output/blog/index.html`
     - Creates metadata: `output/blog/posts.json`
   
   - **Projects Section** → `src/generators/projects.py`
     - Reads all `.md` files from `proyectos_md/`
     - Generates project cards
     - Creates index: `output/proyectos/index.html`

3. **Error Handling** → Collects all errors and reports at end:
   ```
   ⚠️  Blog generation encountered 2 issue(s):
      - Skipping 'draft.md': missing title
      - Error rendering 'bad.md': Invalid YAML
   ```

---

## Adding New Sections (Future)

To add a "Mi CV" section:

1. Create input folder: `cv_md/`
2. Add to `config.yaml`:
   ```yaml
   - name: "Mi CV"
     path: "cv"
     input_dir: "cv_md"
     output_dir: "cv"
     type: "cv"
   ```
3. Create `src/generators/cv.py`:
   ```python
   from .base import SectionGenerator
   
   class CVGenerator(SectionGenerator):
       def generate(self):
           # Your logic here
   ```
4. Register in `src/generators/__init__.py` and `src/generator.py`
5. Run `python3 build.py` → generates `output/cv/`

---

## Troubleshooting

**Problem:** `python3 build.py` fails with "Module not found"
```bash
pip install -r requirements.txt
```

**Problem:** Old files still on server after deploy
```bash
# deploy.sh uses --delete to remove old files
# Make sure ssh key is set up for passwordless login
ssh-keygen -t ed25519
ssh-copy-id -i ~/.ssh/id_ed25519.pub bloguser@punterocrudo
```

**Problem:** Want to preview changes before deploying
```bash
python3 build.py
cd output && python3 -m http.server 8000
# Open http://localhost:8000/blog/
```

---

## Git Workflow

### What to commit:
```bash
git add config.yaml src/ build.py deploy.sh BLOG_REVISION_PROPOSAL.md
git commit -m "refactor: modularize blog generation"
```

### What's gitignored (don't commit):
```
output/          # Generated files
.idea/           # IDE
borradores_md/   # Drafts
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Build blog | `python3 build.py` |
| Preview locally | `python3 build.py && cd output && python3 -m http.server 8000` |
| Deploy to server | `./deploy.sh` |
| Check what changed | `git status` |
| View configuration | `cat config.yaml` |

