#!/usr/bin/env python3
"""Simple HTTP server for the D3 visualizations.
Run from the 04_between_things directory:
    python scripts/serve_viz.py
Then open http://localhost:8080
"""
import http.server
import os

PORT = 8080
os.chdir(os.path.join(os.path.dirname(__file__), "..", "viz"))

print(f"Serving viz/ at http://localhost:{PORT}")
print("Press Ctrl+C to stop.\n")
http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
