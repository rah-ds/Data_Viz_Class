#!/usr/bin/env python3
"""
Simple HTTP server to serve the D3 visualizations in hw3/viz/
Run from anywhere — it always serves the viz/ directory.

Usage:
    python scripts/serve.py           # default port 8000
    python scripts/serve.py 8080      # custom port
"""

import http.server
import socketserver
import os
import sys
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Always serve the viz/ directory relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VIZ_DIR = os.path.join(SCRIPT_DIR, "..", "viz", "raw")

os.chdir(VIZ_DIR)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving hw3/viz/raw/ at {url}")
    print(f"Press Ctrl+C to stop.\n")
    webbrowser.open(url)
    httpd.serve_forever()
