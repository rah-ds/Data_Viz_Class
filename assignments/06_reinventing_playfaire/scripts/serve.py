#!/usr/bin/env python3
"""Simple HTTP server for the Wikipedia edit-conflict visualization.

Serves from the assignment root so that relative paths like
../data/processed/d3/ in the HTML files resolve correctly.

Usage (from any directory):
    python scripts/serve.py [PORT] [--open viz/ideas2.html]
Or via make:
    make serve-wiki
    make serve-wiki-ideas2
Then open http://localhost:8888/viz/dashboard.html
"""
import http.server
import os
import sys
import webbrowser
import threading

args = sys.argv[1:]
PORT = 8888
open_path = "viz/dashboard.html"
for i, a in enumerate(args):
    if a == "--open" and i+1 < len(args):
        open_path = args[i+1]
    elif a.isdigit():
        PORT = int(a)

# Serve from the assignment root (parent of scripts/)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(root)

url = f"http://localhost:{PORT}/{open_path}"
print(f"Serving Wikipedia edit-conflict viz at http://localhost:{PORT}/")
print(f"Opening: {url}")
print("Press Ctrl+C to stop.\n")

# Open browser after a short delay
threading.Timer(0.5, lambda: webbrowser.open(url)).start()

http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
