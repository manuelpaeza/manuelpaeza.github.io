"""Validate generated HTML nesting, local targets, metadata, and bibliography parity."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
class Check(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True); self.path=path; self.stack=[]; self.ids=set(); self.fragments=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in VOID: self.stack.append(tag)
        if tag=='h1': self.h1+=1
        if 'id' in a:
            assert a['id'] not in self.ids, (self.path,'duplicate id'); self.ids.add(a['id'])
        if tag=='a':
            assert a.get('href'), (self.path,'empty href')
            if a.get('target')=='_blank': assert {'noopener','noreferrer'} <= set(a.get('rel','').split())
        for attr in ['href','src']:
            if attr not in a: continue
            u=urlsplit(a[attr])
            if not u.scheme and not u.netloc:
                if u.path: assert (ROOT/unquote(u.path).lstrip('/')).is_file(), (self.path,a[attr])
                elif u.fragment: self.fragments.append(u.fragment)
    def handle_endtag(self,tag):
        assert self.stack and self.stack.pop()==tag, (self.path,tag,'incorrect nesting')
for path in sorted(ROOT.glob('*.html')):
    p=Check(path.name); s=path.read_text(); p.feed(s); p.close()
    assert not p.stack and p.h1==1, path
    assert all(f in p.ids for f in p.fragments),path
    assert '<title>' in s and 'name="description"' in s and 'rel="canonical"' in s
    assert 'polyfill.io' not in s and 'font-[Open_Sans]' not in s
    print('PASS',path.name)
import build_site
for record in build_site.papers:
    entry=build_site.paper(record)
    assert entry in (ROOT/'index.html').read_text() and entry in (ROOT/'publications.html').read_text()
assert '[Slides]' not in (ROOT/'projects.html').read_text()
print('PASS publication parity, all local links, HTML nesting, and draft exclusion')
