#!/usr/bin/env python3
"""Simple HTTP server for the Wikipedia edit-conflict visualization.

Serves from the assignment root so that relative paths like
../data/processed/d3/ in the HTML files resolve correctly.

Usage (from any directory):
    python scripts/serve.py [PORT]
Or via make:
    make serve-wiki
Then open http://localhost:8888/viz/dashboard.html
"""
import http.server
import os
import sys
import webbrowser
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8888

# Serve from the assignment root (parent of scripts/)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(root)

url = f"http://localhost:{PORT}/viz/dashboard.html"
print(f"Serving Wikipedia edit-conflict viz at {url}")
print("Press Ctrl+C to stop.\n")

# Open browser after a short delay
threading.Timer(0.5, lambda: webbrowser.open(url)).start()

http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
