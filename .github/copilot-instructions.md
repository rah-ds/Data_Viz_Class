# Copilot Instructions — Data Viz Class (SARC 5400)

## Commands

```bash
make install       # Bootstrap uv + install all Python packages
make fmt-py        # Auto-format Python (ruff)
make fmt-md        # Auto-format Markdown (prettier)
make lint          # Proselint on markdown write-ups
make clean         # Remove .DS_Store & __pycache__
```

**Dev servers** (each assignment has its own):

```bash
make serve-vda     # Assignment 03 — port 8000
make serve-btw     # Assignment 04 — port 8080
make serve-lg      # Assignment 05 Observable Framework — port 3000
make serve-wiki    # Assignment 06 (final) — port 8888, opens browser
```

**Data prep** (run from repo root):

```bash
make prepare-vda   # Assignment 03 data pipeline
# For 04, run directly: uv run python assignments/04_between_things/scripts/prepare_d3_data.py
```

**Python runtime**: always `uv run python ...` — never activate the venv manually or use `pip` directly. All Python linting/formatting goes through `ruff`.

## Architecture

Each assignment is self-contained under `assignments/NN_name/`:
```
NN_name/
  data/        # local raw + processed data
  scripts/     # Python: prepare_*.py (data prep) + serve*.py (HTTP server)
  viz/         # D3 HTML files (or index.html for Observable)
  writeup/     # Written analysis
```

**Data flow**: Python `scripts/prepare_*.py` → JSON files → D3 HTML loads via `d3.json()`.

**Two viz stacks in use**:
- **D3.js** (assignments 03, 04, 06): Self-contained HTML files with inline CSS + JS. Data loaded via relative `d3.json()` paths. Served by a Python `http.server.SimpleHTTPRequestHandler`.
- **Observable Framework** (assignment 05): `npm run dev` via `assignments/05_land_guzzlers/`.

**Shared/root data** lives in `data/raw/` and `data/processed/`. Assignment-specific data that's small enough to commit goes in the assignment's own `data/` folder.

## Key Conventions

### Serve script pattern
Every assignment has its own `scripts/serve.py`. They all `os.chdir()` to set the server root before starting — this is intentional, because `d3.json()` paths in the HTML are relative to the server root. **The root must be chosen carefully**:
- Assignments 03 and 04 serve from inside `viz/` (data is co-located with HTML)
- Assignment 06 serves from the assignment root so `../data/processed/d3/` resolves correctly

### Python path navigation
Scripts use `Path(__file__).resolve().parents[N]` to navigate up to the project root — avoid hardcoding absolute paths.

### Data size limit
A pre-commit hook **blocks any file > 10 MB**. Large files must be `.gitignore`d before staging. To bypass: `git commit --no-verify`. The `.gitignore` explicitly names the large Spotify source files that were purged from history.

### D3 HTML structure
D3 visualizations are single-file HTML: inline `<style>`, inline `<script>`, and one or more `d3.json(relPath)` calls to load pre-built JSON. No bundler, no npm imports — just a CDN `<script src="https://d3js.org/d3.v7.min.js">`.

### Python script headers
Data prep scripts document their expected working directory in the module docstring and use `Path(__file__).resolve()` for all file references so they can be run from any directory.

### JSON as D3 data format
All data passed to D3 visualizations is pre-processed into compact JSON by Python scripts. Avoid loading raw CSVs in the browser.
