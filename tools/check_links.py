#!/usr/bin/env python3
"""Offline link checker for ./public using Cloudflare Pages URL rules.

Reports broken internal links and missing assets. Links to documents (PDF etc.)
that point at the files subdomain are skipped; local document links are listed separately.
"""
import os, re, sys, html, collections, posixpath
from urllib.parse import urlsplit, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public'))
OWN = {'www.africa-laws.org', 'africa-laws.org'}
DOC = re.compile(r'\.(pdf|docx?|xlsx?|pptx?|zip|rar|odt)$', re.I)
ATTR = re.compile(r'(?<![\w-])(?:href|src|data-setbg|data-src|poster)\s*=\s*(["\'])(.*?)\1', re.S | re.I)
CSSURL = re.compile(r'url\(\s*["\']?([^)"\']+)["\']?\s*\)', re.I)
ID = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.I)

def exists(path):
    p = os.path.join(ROOT, path.lstrip('/'))
    if path.endswith('/'): return os.path.isfile(os.path.join(p, 'index.html'))
    return os.path.isfile(p) or os.path.isfile(p + '.html') or os.path.isfile(os.path.join(p, 'index.html'))

def redirects():
    r = set()
    f = os.path.join(ROOT, '_redirects')
    if os.path.exists(f):
        for l in open(f, encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#'): r.add(unquote(l.split()[0]))
    return r
RED = redirects()

broken, docs, anchors, checked = collections.defaultdict(set), collections.defaultdict(set), [], 0
ids_cache = {}
def page_ids(path):
    if path not in ids_cache:
        for cand in (path + '.html', path, posixpath.join(path, 'index.html')):
            fp = os.path.join(ROOT, cand.lstrip('/'))
            if os.path.isfile(fp) and fp.endswith('.html'):
                ids_cache[path] = set(ID.findall(re.sub(r'<!--.*?-->', '', open(fp, encoding='utf-8', errors='replace').read(), flags=re.S))); break
        else: ids_cache[path] = None
    return ids_cache[path]

def check(src, ref):
    global checked
    ref = html.unescape(ref).strip()
    if not ref or ref.startswith(('mailto:', 'tel:', 'javascript:', 'data:')) : return
    sp = urlsplit(ref.replace('\\', '/'))
    if sp.scheme in ('http', 'https') or ref.startswith('//'):
        if sp.netloc.lower() not in OWN: return
        path = sp.path or '/'
    else:
        path = sp.path
    if path == '': 
        if sp.fragment:
            ids = page_ids('/' + src[:-5] if src != 'index.html' else '/index')
            if ids is not None and sp.fragment not in ids: anchors.append((src, '#' + sp.fragment))
        return
    path = unquote(path)
    if not path.startswith('/'):
        path = posixpath.normpath(posixpath.join('/' + posixpath.dirname(src), path))
    checked += 1
    if DOC.search(path): 
        if not exists(path): docs[path].add(src)
        return
    if path in RED or exists(path): return
    broken[path].add(src)

for dp, _, fs in os.walk(ROOT):
    for f in fs:
        fp = os.path.join(dp, f); rel = os.path.relpath(fp, ROOT).replace(os.sep, '/')
        if f.endswith('.html'):
            t = re.sub(r'<!--.*?-->', '', open(fp, encoding='utf-8', errors='replace').read(), flags=re.S)
            for _, v in ATTR.findall(t): check(rel, v)
            for v in CSSURL.findall(t): check(rel, v)
        elif f.endswith('.css'):
            for v in CSSURL.findall(open(fp, encoding='utf-8', errors='replace').read()):
                if v.startswith(('data:', '#', 'http:', 'https:', '//')): continue
                base = posixpath.dirname(rel)
                v = v.split('#')[0].split('?')[0]
                path = posixpath.normpath(posixpath.join('/' + base, v)) if not v.startswith('/') else v
                if not exists(path): broken[path].add(rel)

print(f'checked {checked} internal references')
print(f'\nBROKEN INTERNAL LINKS / MISSING ASSETS: {len(broken)}')
for p, srcs in sorted(broken.items(), key=lambda x: (-len(x[1]), x[0])):
    print(f'  {len(srcs):4}x {p}   (e.g. {sorted(srcs)[0]})')
print(f'\nLOCAL DOCUMENT LINKS NOT IN public/ (expected until Phase 4 rewrites them): {len(docs)}')
print(f'ANCHORS WITH NO TARGET ID: {len(anchors)}')
for a in anchors[:10]: print('  ', a)
sys.exit(1 if broken else 0)
