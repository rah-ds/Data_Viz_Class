.PHONY: help install export-svgs serve-vda prepare-vda notebook lint fmt-py fmt-md clean

# Default port for the dev server
PORT ?= 8000

## help: show this help message
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install        Bootstrap uv (if missing) and sync all Python packages"
	@echo "  export-svgs    Export the 3 key D3 vizs to labelled SVGs in viz/to_refine/"
	@echo "  serve-vda      Serve the visual_data_analysis D3 files (viz/raw/) in a browser"
	@echo "  prepare-vda    Run the data-prep script for visual_data_analysis"
	@echo "  notebook       Launch Jupyter Notebook from the notebooks/ directory"
	@echo "  lint           Run proselint on all markdown writeups"
	@echo "  fmt-py         Auto-format all Python files with ruff"
	@echo "  fmt-md         Auto-format all Markdown files with prettier"
	@echo "  clean          Remove .DS_Store files and Python cache dirs"
	@echo ""

## export-svgs: export the three key D3 visualisations to labelled SVG files in viz/to_refine/
export-svgs:
	node assignments/03_visual_data_analysis/scripts/export_svgs/export.mjs

## serve-vda: serve the D3 visualisations for visual_data_analysis
serve-vda:
	uv run python assignments/03_visual_data_analysis/scripts/serve.py $(PORT)

## prepare-vda: run the data preparation script for visual_data_analysis
prepare-vda:
	uv run python assignments/03_visual_data_analysis/scripts/prepare_data.py

## notebook: launch Jupyter Notebook rooted at notebooks/
notebook:
	uv run jupyter notebook --notebook-dir=notebooks

## lint: proselint all markdown writeups
lint:
	@echo "Linting markdown files..."
	@find assignments -name "*.md" | xargs -I{} uv run proselint {}

## install: bootstrap uv (if missing) then sync all Python packages from pyproject.toml
install:
	@echo "→ Checking for uv..."
	@if ! command -v uv > /dev/null 2>&1; then \
		echo "  uv not found — installing via official installer..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "  Reload your shell or run: source $$HOME/.local/bin/env"; \
	else \
		echo "  uv $$(uv --version) already installed."; \
	fi
	@echo "→ Syncing Python packages..."
	uv sync
	@echo "✓ Done. All packages installed."

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
