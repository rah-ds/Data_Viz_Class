#!/usr/bin/env python3
"""
Sync newly fetched Wikipedia arbitration cases to the assignment viz folder.

Run this after fetch_missing_cases.py has added new raw case files to the
Wikipedia_Dispute_Models pipeline. This script:
  1. Runs export_d3_all.py to produce new case JSON files
  2. Copies any new files from the pipeline's d3/ folder to this assignment's d3/ folder
  3. Copies the regenerated manifest.json

Usage:
    uv run python assignments/06_reinventing_playfaire/scripts/sync_new_cases.py
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ASSIGNMENT_D3 = SCRIPT_DIR.parent / "data" / "processed" / "d3"
PIPELINE_ROOT = Path.home() / "MSDS" / "Wikipedia_Dispute_Models"
PIPELINE_D3 = PIPELINE_ROOT / "data" / "processed" / "d3"
EXPORT_SCRIPT = PIPELINE_ROOT / "scripts" / "export_d3_all.py"


def main() -> int:
    if not PIPELINE_ROOT.exists():
        print(f"ERROR: pipeline root not found: {PIPELINE_ROOT}", file=sys.stderr)
        return 1
    if not EXPORT_SCRIPT.exists():
        print(f"ERROR: export script not found: {EXPORT_SCRIPT}", file=sys.stderr)
        return 1

    # 1. Run the export pipeline
    print("Running export_d3_all.py …")
    result = subprocess.run(
        ["uv", "run", "python", str(EXPORT_SCRIPT)],
        cwd=PIPELINE_ROOT,
        text=True,
    )
    if result.returncode != 0:
        print("Export script failed.", file=sys.stderr)
        return result.returncode

    # 2. Find any new files in pipeline d3/ not yet in assignment d3/
    existing = {p.name for p in ASSIGNMENT_D3.glob("*.json")}
    new_files = [p for p in PIPELINE_D3.glob("*.json") if p.name not in existing]

    if not new_files:
        print("No new case files to copy — assignment folder is already up to date.")
    else:
        print(f"Copying {len(new_files)} new case file(s) …")
        for src in new_files:
            dst = ASSIGNMENT_D3 / src.name
            shutil.copy2(src, dst)
            print(f"  + {src.name}")

    # 3. Copy the manifest (always refresh it)
    src_manifest = PIPELINE_D3 / "manifest.json"
    dst_manifest = ASSIGNMENT_D3 / "manifest.json"
    if src_manifest.exists():
        shutil.copy2(src_manifest, dst_manifest)
        print(f"Updated manifest.json")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
