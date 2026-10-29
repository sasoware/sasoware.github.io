from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit

root = Path(sys.argv[1]).resolve()
required = {'index.html', 'danbi/index.html', 'danbi/privacy/index.html', 'style.css', '404.html', 'robots.txt', '.nojekyll', 'app-ads.txt'}
if {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} != required:
    raise SystemExit('File set differs from the approved static site.')
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set(); self.viewport=False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get('id'): self.ids.add(d['id'])
        if tag == 'meta' and d.get('name') == 'viewport': self.viewport=True
        self.links += [d[k] for k in ('href','src') if d.get(k)]
pages = {}
for p in root.rglob('*.html'):
    obj = Page(); obj.feed(p.read_text(encoding='utf-8')); pages[p] = obj
    if not obj.viewport: raise SystemExit('Missing viewport.')
    text = p.read_text(encoding='utf-8')
    if 'name="robots" content="noindex"' in text or 'data-review-only' in text:
        raise SystemExit('Private-review restriction remained in approved page.')
for p, obj in pages.items():
    for link in obj.links:
        if link.startswith(('https://', 'mailto:')): continue
        parts=urlsplit(link)
        if parts.netloc or parts.scheme or parts.query or '..' in parts.path: raise SystemExit('Unsafe link.')
        target=(root / parts.path.lstrip('/')) if parts.path else p
        if target.is_dir(): target=target/'index.html'
        if not target.is_file(): raise SystemExit('Missing linked file.')
        if parts.fragment and (target not in pages or parts.fragment not in pages[target].ids): raise SystemExit('Missing anchor.')
policy=pages[root/'danbi/privacy/index.html']
if not {'en','delete-ko','delete-en'} <= policy.ids: raise SystemExit('Missing language or deletion anchors.')
if (root/'app-ads.txt').read_text(encoding='utf-8').strip() != 'google.com, pub-4831992621629556, DIRECT, f08c47fec0942fa0': raise SystemExit('Unexpected app-ads.txt.')
print('Static routes, policy anchors, files and viewport: PASS')
