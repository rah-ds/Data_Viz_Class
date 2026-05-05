.PHONY: help install export-svgs serve-vda serve-btw serve-lg serve-wiki serve-wiki-ideas serve-wiki-ideas2 serve-wiki-politics sync-wiki-cases prepare-vda notebook lint fmt-py fmt-md clean

# ──────────────────────────────────────────────
#  Colors (only when stdout is a terminal)
# ──────────────────────────────────────────────
BOLD   := $(shell tput bold   2>/dev/null || true)
CYAN   := $(shell tput setaf 6 2>/dev/null || true)
GREEN  := $(shell tput setaf 2 2>/dev/null || true)
YELLOW := $(shell tput setaf 3 2>/dev/null || true)
RESET  := $(shell tput sgr0   2>/dev/null || true)

# Default port for the dev server
PORT ?= 8000

## help: show this help message
help:
	@echo ""
	@echo "  $(BOLD)📊 Data Viz Class$(RESET)  —  make targets"
	@echo "  ─────────────────────────────────────────"
	@echo ""
	@echo "  $(CYAN)Setup$(RESET)"
	@echo "    $(GREEN)install$(RESET)        Bootstrap uv, sync packages & install git hooks"
	@echo ""
	@echo "  $(CYAN)Dev Servers$(RESET)"
	@echo "    $(GREEN)serve-vda$(RESET)      Serve assignment 03 D3 visualizations  (port $(PORT))"
	@echo "    $(GREEN)serve-btw$(RESET)      Serve assignment 04 D3 visualizations  (port 8080)"
	@echo "    $(GREEN)serve-lg$(RESET)       Serve assignment 05 Observable Framework (port 3000)"
	@echo "    $(GREEN)serve-wiki$(RESET)     Serve assignment 06 Wikipedia edit-conflict viz (port 8888)"
	@echo "    $(GREEN)serve-wiki-ideas$(RESET)  Open Volume I experimental viz ideas"
	@echo "    $(GREEN)serve-wiki-ideas2$(RESET) Open Volume II experimental viz ideas
    $(GREEN)serve-wiki-politics$(RESET) Open politics cases standalone viz"
	@echo "    $(GREEN)notebook$(RESET)       Launch Jupyter Notebook"
	@echo ""
	@echo "  $(CYAN)Data & Export$(RESET)"
	@echo "    $(GREEN)prepare-vda$(RESET)    Run data-prep pipeline for assignment 03"
	@echo "    $(GREEN)export-svgs$(RESET)    Render D3 vizs → SVG files"
	@echo "    $(GREEN)sync-wiki-cases$(RESET) Export & sync newly-fetched Wikipedia cases"
	@echo ""
	@echo "  $(CYAN)Code Quality$(RESET)"
	@echo "    $(GREEN)fmt-py$(RESET)         Auto-format Python with ruff"
	@echo "    $(GREEN)fmt-md$(RESET)         Auto-format Markdown with prettier"
	@echo "    $(GREEN)lint$(RESET)           Proselint on markdown write-ups"
	@echo ""
	@echo "  $(CYAN)Maintenance$(RESET)"
	@echo "    $(GREEN)clean$(RESET)          Remove .DS_Store & __pycache__"
	@echo ""

## export-svgs: export the three key D3 visualisations to labelled SVG files in viz/to_refine/
export-svgs:
	node assignments/03_visual_data_analysis/scripts/export_svgs/export.mjs

## serve-vda: serve the D3 visualisations for visual_data_analysis
serve-vda:
	uv run python assignments/03_visual_data_analysis/scripts/serve.py $(PORT)

## serve-btw: serve the between_things D3 viz files
serve-btw:
	uv run python assignments/04_between_things/scripts/serve_viz.py

## serve-lg: serve the land_guzzlers Observable Framework project
serve-lg:
	cd assignments/05_land_guzzlers && npm run dev

## serve-wiki: serve the Wikipedia edit-conflict visualization (assignment 06)
serve-wiki:
	uv run python assignments/06_reinventing_playfaire/scripts/serve.py

## serve-wiki-ideas: open Volume I experimental ideas page
serve-wiki-ideas:
	uv run python assignments/06_reinventing_playfaire/scripts/serve.py --open viz/ideas.html

## serve-wiki-ideas2: open Volume II experimental ideas page
serve-wiki-ideas2:
	uv run python assignments/06_reinventing_playfaire/scripts/serve.py --open viz/ideas2.html

## serve-wiki-politics: open politics cases standalone viz
serve-wiki-politics:
	uv run python assignments/06_reinventing_playfaire/scripts/serve.py --open viz/politics.html

## sync-wiki-cases: export newly-fetched raw cases and sync to assignment viz folder
sync-wiki-cases:
	uv run python assignments/06_reinventing_playfaire/scripts/sync_new_cases.py

## prepare-vda: run the data preparation script for visual_data_analysis
prepare-vda:
	uv run python assignments/03_visual_data_analysis/scripts/prepare_data.py

## notebook: launch Jupyter Notebook rooted at notebooks/
notebook:
	uv run jupyter notebook --notebook-dir=notebooks

## lint: proselint markdown files in README.md, assignments/, and docs/
# TODO: this is broken, fix later
lint:
	@echo "Linting markdown files..."
	@[ -f README.md ] && uv run proselint README.md || true
	@find assignments docs -name "*.md" 2>/dev/null | xargs -r -I{} uv run proselint {}

## install: bootstrap uv (if missing) then sync all Python packages from pyproject.toml
install:
	@echo "$(BOLD)→ Checking for uv...$(RESET)"
	@if ! command -v uv > /dev/null 2>&1; then \
		echo "  uv not found — installing via official installer..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "  Reload your shell or run: source $$HOME/.local/bin/env"; \
	else \
		echo "  $(GREEN)✓$(RESET) uv $$(uv --version) already installed."; \
	fi
	@echo "$(BOLD)→ Syncing Python packages...$(RESET)"
	uv sync
	@echo "$(BOLD)→ Installing git hooks...$(RESET)"
	@cp scripts/pre-commit .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "  $(GREEN)✓$(RESET) pre-commit hook installed (blocks files > 10 MB)"
	@echo ""
	@echo "$(GREEN)$(BOLD)✓ All done!$(RESET) Packages synced & hooks installed."

## fmt-py: auto-format all Python files with ruff
fmt-py:
	uv run ruff format .
	uv run ruff check --fix .
	@echo "✓ Python files formatted."

## fmt-md: auto-format all Markdown files with prettier (via npx)
fmt-md:
	npx --yes prettier --write "**/*.md" --parser markdown
	@echo "✓ Markdown files formatted."

## clean: remove .DS_Store files and Python cache dirs
clean:
	find . -name ".DS_Store" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@echo "Clean done."
