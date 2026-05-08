# SARC 5400 — Data Visualization

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![D3.js](https://img.shields.io/badge/D3.js-v7-F9A03C?logo=d3dotjs&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=astral&logoColor=white)
![Ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?logo=ruff&logoColor=black)
![Prettier](https://img.shields.io/badge/markdown-prettier-F7B93E?logo=prettier&logoColor=black)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

> UVA · Spring 2026 · [Syllabus](https://web.arch.virginia.edu/arch547/syllabus.html)

Coursework and visualizations for SARC 5400 at the University of Virginia. Each assignment lives in its own directory with self-contained data, scripts, and write-ups.

---

## URL
* [Old class viz](https://web.arch.virginia.edu/arch547/Archive/)

## Quick Start

```bash
# 1. Clone
git clone https://github.com/rah-ds/Data_Viz_Class.git
cd Data_Viz_Class

# 2. Install all dependencies (bootstraps uv if needed)
make install

# 3. See available commands
make help
```

## Toolchain

| Tool | Purpose |
|------|---------|
| **[uv](https://docs.astral.sh/uv/)** | Fast Python package management & virtual envs |
| **[Ruff](https://docs.astral.sh/ruff/)** | Python linting & formatting |
| **[Prettier](https://prettier.io/)** | Markdown formatting |
| **[D3.js](https://d3js.org/)** | Interactive browser visualizations |
| **[Plotly](https://plotly.com/python/)** / **[Seaborn](https://seaborn.pydata.org/)** / **[Matplotlib](https://matplotlib.org/)** | Python plotting |
| **[Jupyter](https://jupyter.org/)** | Notebook-based exploration |

## Project Layout

```bash
├── assignments/
│   ├── 01_good_bad_ugly/        # Critique of good, bad & ugly visualizations
│   ├── 02_me_graphically/       # Personal data self-portrait
│   ├── 03_visual_data_analysis/ # D3 explorations + SVG exports
│   └── 04_between_things/       # Spotify listening-data deep dive (D3)
├── data/
│   ├── raw/                     # Untouched source data (gitignored if >10 MB)
│   └── processed/               # Cleaned / derived datasets
├── docs/                        # Course notes & guides
├── homeworks/                   # Smaller homework exercises
├── scripts/                     # Shared utility scripts
├── Makefile                     # Dev commands (see below)
├── pyproject.toml               # Python deps & project metadata
└── package.json                 # Node/npm config for D3 scripts
```

## Make Targets

```bash
make install       # Bootstrap uv + install all Python packages
make serve-vda     # Dev server for assignment 03 D3 visualizations
make serve-btw     # Dev server for assignment 04 D3 visualizations
make export-svgs   # Render D3 vizs → SVG files
make prepare-vda   # Run data-prep pipeline for assignment 03
make notebook      # Launch Jupyter Notebook
make fmt-py        # Auto-format Python (ruff)
make fmt-md        # Auto-format Markdown (prettier)
make lint          # Proselint on all markdown write-ups
make clean         # Remove .DS_Store & __pycache__
```

## Data Notes

Raw data files larger than **10 MB** are excluded from version control (see `.gitignore`). A pre-commit hook prevents accidentally staging oversized files. If you need the full datasets, see the data source links in each assignment's README.

## License

MIT — see [LICENSE](LICENSE) for details.
