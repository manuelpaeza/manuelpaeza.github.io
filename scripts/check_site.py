"""Validate generated HTML nesting, local targets, metadata, and bibliography parity."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())
class Check(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True); self.path=path; self.nav=[]; self.in_nav=False; self.stack=[]; self.ids=set(); self.fragments=[]; self.h1=0; self.meta={}; self.links=[]; self.current=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='nav': self.in_nav=True
        if tag=='a' and self.in_nav: self.nav.append(a.get('href'))
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
                if u.path: assert ((ROOT if u.path.startswith('/') else self.path.parent)/unquote(u.path).lstrip('/')).is_file(), (self.path,a[attr])
                elif u.fragment: self.fragments.append(u.fragment)
    def handle_endtag(self,tag):
        if tag=='nav': self.in_nav=False
        assert self.stack and self.stack.pop()==tag, (self.path,tag,'incorrect nesting')
paths = sorted(ROOT.glob('*.html')) + sorted(p for p in (ROOT/'ml-notes').glob('*/*.html') if p.parent.name not in ['_templates', '_articles'])
for path in paths:
    p=Check(path); s=path.read_text(); p.feed(s); p.close()
    assert not p.stack and p.h1==1, path
    assert all(f in p.ids for f in p.fragments),path
    assert '<title>' in s and 'name="description"' in s and 'rel="canonical"' in s
    assert 'polyfill.io' not in s and 'font-[Open_Sans]' not in s
    canonical=[a['href'] for a in p.links if a.get('rel')=='canonical']
    assert canonical==['https://manuelpaeza.github.io/'+path.relative_to(ROOT).as_posix()]
    assert p.meta['og:url']==canonical[0]
    assert p.meta['og:description']==p.meta['description']
    assert '<title>'+escape(p.meta['og:title'])+'</title>' in s
    if path.parent == ROOT and path.name in ['index.html','publications.html','projects.html','code.html','ml-notes.html']:
        assert p.current==[path.name]
    prefix = '../' * (len(path.relative_to(ROOT).parts) - 1)
    assert p.nav == [prefix + target for target in ['index.html', 'publications.html', 'projects.html', 'ml-notes.html', 'code.html', 'manuelpaez_curriculum_vitae.pdf']], (path, p.nav)
    if prefix: assert p.current == [prefix + 'ml-notes.html']
    assert not any('fonts.googleapis.com' in a.get('href','') or 'fonts.gstatic.com' in a.get('href','') for a in p.links)
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

for css_path in ['src/styles.css', 'styles.css']:
    css=(ROOT/css_path).read_text()
    assert '-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif' in css
    assert 'font-family: "IBM Plex Sans", -apple-system' in css
    assert 'font-family: "IBM Plex Mono", ui-monospace' in css
    assert 'font-display: swap' in css
    assert '#C33A1D' not in css
    for asset in re.findall(r'url\("(assets/fonts/[^"]+\.woff2)"\)', css):
        assert (ROOT/asset).read_bytes().startswith(b'wOF2'), asset
print('PASS local IBM Plex fonts, fallbacks, and no external font imports')

import ml_notes
ml_html = (ROOT/'ml-notes.html').read_text()
resource_groups = ml_notes.load_resources(ROOT)
class Disclosures(HTMLParser):
    def __init__(self):
        super().__init__(); self.details = 0; self.summaries = 0; self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == 'details':
            self.details += 1
            assert not {'open', 'name'} & dict(attrs).keys(), 'Disclosures must start closed and remain independent'
        if tag == 'summary': self.summaries += 1
        if tag == 'a': self.hrefs.append(dict(attrs).get('href'))
        assert tag != 'script', 'Resource library must work without JavaScript'
disclosures = Disclosures()
disclosures.feed(ml_html)
expected = len(resource_groups) + sum(len(g.get('sections', [])) for g in resource_groups)
assert disclosures.details == disclosures.summaries == expected
for group in resource_groups:
    for section in group.get('sections', [group]):
        for resource in section['resources']:
            assert disclosures.hrefs.count(resource['url']) == 1, resource['url']
            assert escape(resource['title']) in ml_html
for category in ml_notes.CATEGORIES:
    assert f'id="{category}"' in ml_html
assert 'not completed research or published results' in ml_html
assert '_templates' not in ml_html and '_preview' not in ml_html
for e in ml_notes.load_entries(ROOT):
    assert ml_notes.article_path(e) in ml_html
    assert (ROOT / ml_notes.article_path(e)).is_file()
print('PASS shared navigation, ML categories, resource links, and published article registry')
