"""Validate generated HTML nesting, local targets, metadata, and bibliography parity."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
class Check(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True); self.path=path; self.stack=[]; self.ids=set(); self.fragments=[]; self.h1=0; self.meta={}; self.links=[]; self.current=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in VOID: self.stack.append(tag)
        if tag=='h1': self.h1+=1
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link': self.links.append(a)
        if a.get('aria-current')=='page': self.current.append(a.get('href'))
        if tag=='img': assert a.get('alt'), (self.path,'missing image alt')
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
    canonical=[a['href'] for a in p.links if a.get('rel')=='canonical']
    assert canonical==['https://manuelpaeza.github.io/'+path.name]
    assert p.meta['og:url']==canonical[0]
    assert p.meta['og:description']==p.meta['description']
    assert '<title>'+p.meta['og:title']+'</title>' in s
    if path.name in ['index.html','publications.html','projects.html','code.html']:
        assert p.current==[path.name]
    font_links=[a['href'] for a in p.links if a.get('rel')=='stylesheet' and 'fonts.googleapis.com' in a.get('href','')]
    assert font_links==['https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap']
    assert any(a.get('rel')=='preconnect' and a.get('href')=='https://fonts.gstatic.com' and 'crossorigin' in a for a in p.links)
    print('PASS',path.name)
import build_site
for record in build_site.papers:
    entry=build_site.paper(record)
    assert entry in (ROOT/'index.html').read_text() and entry in (ROOT/'publications.html').read_text()
ieor=build_site.projects[0]
assert ieor[4]=='projects/IEOR8100_Energy_Simulated_Annealing_Pure_Spherical_Spin_Slides_Paez_2026.pdf'
for filename in ['index.html','projects.html']:
    html=(ROOT/filename).read_text()
    assert build_site.project(ieor) in html
    assert html.count('[Slides]')==1
assert '[Slides]' not in (ROOT/'publications.html').read_text()
assert (ROOT/ieor[4]).read_bytes().startswith(b'%PDF-')
assert 'simulatedannealing_markovchains_spherical_ham_manuelpaez.pdf' not in ''.join(p.read_text() for p in ROOT.glob('*.html'))
print('PASS publication parity, all local links, HTML nesting, font/metadata parity, IEOR report/slides, and draft exclusion')
