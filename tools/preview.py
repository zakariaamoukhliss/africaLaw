#!/usr/bin/env python3
"""Local preview that mimics Cloudflare Pages: clean URLs (/Laws -> Laws.html), _redirects, 404.html.

Usage: python3 tools/preview.py [port]   (serves ./public)
"""
import http.server, os, sys, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
ROOT = os.path.abspath(ROOT)

def load_redirects():
    rules = {}
    path = os.path.join(ROOT, '_redirects')
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                rules[urllib.parse.unquote(parts[0])] = (parts[1], int(parts[2]) if len(parts) > 2 else 301)
    return rules

REDIRECTS = load_redirects()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if path in REDIRECTS:
            dest, code = REDIRECTS[path]
            self.send_response(code); self.send_header('Location', dest); self.end_headers(); return
        fs = os.path.join(ROOT, path.lstrip('/'))
        if path.endswith('/') or path == '':
            fs = os.path.join(fs, 'index.html')
        if os.path.isfile(fs):
            return super().do_GET()
        if os.path.isfile(fs + '.html'):
            self.path = urllib.parse.quote(path) + '.html'
            return super().do_GET()
        if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, 'index.html')):
            self.send_response(308); self.send_header('Location', path.rstrip('/') + '/'); self.end_headers(); return
        body = open(os.path.join(ROOT, '404.html'), 'rb').read() if os.path.exists(os.path.join(ROOT, '404.html')) else b'Not found'
        self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f'Serving {ROOT} on http://localhost:{port}')
    http.server.ThreadingHTTPServer(('', port), Handler).serve_forever()
