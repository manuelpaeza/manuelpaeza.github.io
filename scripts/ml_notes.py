"""ML notebook content and article rendering; no additional build dependencies."""
import json
import re
from datetime import date
from html import escape

CATEGORIES = {
    'pretraining': 'Pretraining and Scaling Laws',
    'optimization': 'Optimization and Learning Dynamics',
    'architectures': 'Model Architectures and Algorithms',
    'generalization': 'Generalization and Feature Learning',
    'inference-and-sampling': 'Statistical Inference and Sampling',
    'ml-systems': 'ML Systems and Computational Efficiency',
    'reinforcement-learning': 'Post-Training and Reinforcement Learning',
}
DIRECTIONS = [
    'Multimode Optimization Across Neural Network Architectures',
    'Optimization Dynamics and Feature Learning',
    'Hyperparameter Transfer Across Model Scales',
    'Statistical and Algorithmic Generalization in Transformers',
    'Sampling Efficiency in Generative and Reasoning Models',
]

def load_entries(root):
    entries = json.loads((root / 'ml-notes/entries.json').read_text())
    paths, report_ids = set(), set()
    for entry in entries:
        assert entry['category'] in {*CATEGORIES, 'training-reports', 'research'}
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', entry['slug'])
        assert entry['title'].strip() and entry['description'].strip()
        assert date.fromisoformat(entry['updated']) >= date.fromisoformat(entry['published'])
        assert isinstance(entry['topics'], list)
        if entry['category'] == 'training-reports':
            assert re.fullmatch(r'TR-\d{3,}', entry['report_id'])
            assert entry['report_id'] not in report_ids
            report_ids.add(entry['report_id'])
        path = article_path(entry)
        assert path not in paths, f'Duplicate article: {path}'
        paths.add(path)
        assert (root / source_path(entry)).is_file(), f'Missing article body: {source_path(entry)}'
    return entries

def article_path(entry):
    return f"ml-notes/{entry['category']}/{entry['slug']}.html"

def source_path(entry):
    return f"ml-notes/_articles/{entry['category']}/{entry['slug']}.html"

def dates(entry):
    return (f'Published <time datetime="{entry["published"]}">{entry["published"]}</time>'
            f' · Updated <time datetime="{entry["updated"]}">{entry["updated"]}</time>')

def entry_links(entry, link, prefix=''):
    return ' '.join(link('[' + label + ']', url if ':' in url or url.startswith('/') else prefix + url)
                    for label, url in entry.get('links', []))

def listing(entries, category, link):
    selected = sorted((e for e in entries if e['category'] == category), key=lambda e: e['published'], reverse=True)
    if not selected:
        return ''
    items = []
    for e in selected:
        label = (e.get('report_id', '') + ' · ' if e.get('report_id') else '') + e['title']
        items.append(f'<li class="entry"><h4>{link(label, article_path(e))}</h4>'
                     f'<p class="metadata">{dates(e)}</p><p>{escape(e["description"])}</p>'
                     f'<p class="metadata">Topics: {escape(", ".join(e["topics"]))}</p>'
                     f'<p class="entry-links">{entry_links(e, link)}</p></li>')
    return '<ul class="bibliography">' + '\n'.join(items) + '</ul>'

def load_resources(root):
    groups = json.loads((root / 'ml-notes/resources.json').read_text())
    urls = set()
    def validate(group):
        assert group['title'].strip()
        assert ('resources' in group) != ('sections' in group)
        if 'sections' in group:
            assert group['sections']
            for section in group['sections']:
                validate(section)
        else:
            assert group['resources']
            for resource in group['resources']:
                assert resource['title'].strip()
                url = resource['url']
                assert url.startswith(('https://', 'http://'))
                assert url not in urls, f'Duplicate resource URL: {url}'
                urls.add(url)
    for group in groups:
        validate(group)
    return groups

def resource_count(group):
    if 'resources' in group:
        return len(group['resources'])
    return sum(resource_count(section) for section in group['sections'])

def resource_group(group, link, level=4):
    count = resource_count(group)
    parts = [f'<details class="resource-group"><summary><h{level}>{escape(group["title"])} '
             f'<span class="metadata">({count} {"resource" if count == 1 else "resources"})</span></h{level}></summary>']
    if 'sections' in group:
        parts.extend(resource_group(section, link, level + 1) for section in group['sections'])
    else:
        parts.append('<ul class="notebook-list">')
        for resource in group['resources']:
            attribution = (f' <span class="metadata">— {escape(resource["attribution"])}</span>'
                           if resource.get('attribution') else '')
            parts.append(f'<li>{link(resource["title"], resource["url"])}{attribution}</li>')
        parts.append('</ul>')
    parts.append('</details>')
    return '\n'.join(parts)

def landing(entries, resources, link):
    parts = ['''<div class="ml-notebook">
<header class="notebook-intro"><h2>ML Research Notes</h2>
<p>This page contains a collection of mathematical notes, training reports, and research investigations into the foundations of modern deep learning, with an emphasis on language model pretraining, optimization and learning dynamics, model architectures, and generalization.</p>
<p>I am particularly interested in understanding these topics through the lens of algorithms, high-dimensional probability, random optimization, and statistical inference, combining mathematical analysis with controlled empirical experiments.</p></header>
<section aria-labelledby="training-reports"><h3 id="training-reports">I. Training Reports &amp; Experiments</h3>
<p>A collection of empirical investigations into language model training, including training configurations, optimization experiments, architectural ablations, scaling behavior, and reproducible results.</p>''']
    parts.append(listing(entries, 'training-reports', link) or '<p class="metadata">No training reports published yet.</p>')
    parts.append('''</section><section aria-labelledby="technical-notes"><h3 id="technical-notes">II. Mathematical &amp; Technical Notes</h3>
<p>The notes will include mathematical derivations, algorithmic analysis, implementation details, literature discussions, and empirical observations.</p>''')
    if not any(e['category'] in CATEGORIES for e in entries):
        parts.append('<p class="metadata">No technical notes published yet. Future notes will be organized by the following topics.</p>')
    for slug, title in CATEGORIES.items():
        parts.append(f'<div class="note-category"><h4 id="{slug}">{escape(title)}</h4>{listing(entries, slug, link)}</div>')
    parts.append('''</section><section aria-labelledby="research"><h3 id="research">III. Research Investigations</h3>
<p>A section dedicated to ongoing independent theoretical and empirical research projects in modern machine learning.</p>''')
    parts.append(listing(entries, 'research', link))
    parts.append('<p>Prospective research directions include the following. These are potential future investigations, not completed research or published results.</p><ul class="notebook-list">')
    parts.extend(f'<li>{escape(title)}</li>' for title in DIRECTIONS)
    parts.append('''</ul></section><section aria-labelledby="resources"><h3 id="resources">IV. Selected Resources</h3>
<p>An evolving collection of courses, lecture notes, monographs, research papers, technical reports, and implementations on the mathematical, algorithmic, and empirical foundations of modern deep learning.</p>''')
    parts.extend(resource_group(group, link) for group in resources)
    parts.append('</section></div>')
    return '\n'.join(parts)

def article(entry, body, link):
    label = entry.get('report_id') or CATEGORIES.get(entry['category'], 'Research Investigation')
    return (f'<article class="ml-article"><p>{link("Back to ML Research Notes", "../../ml-notes.html")}</p>'
            f'<header class="article-heading"><p class="metadata">{escape(label)}</p>'
            f'<h2>{escape(entry["title"])}</h2><p class="metadata">{dates(entry)}</p>'
            f'<p>{escape(entry["description"])}</p><p class="metadata">Topics: {escape(", ".join(entry["topics"]))}</p>'
            f'<p class="entry-links">{entry_links(entry, link, "../../")}</p></header>{body}</article>')

ARTICLE_SCRIPTS = '''<script src="../../ml-notes/article.js?v=20261124" defer></script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js" defer></script>'''

def build(root, page, link, preview=False):
    entries = load_entries(root)
    page('ml-notes.html', 'ML Research Notes — Manuel Paez',
         'Mathematical notes, training reports, and research investigations into modern deep learning.', landing(entries, load_resources(root), link))
    for e in entries:
        page(article_path(e), e['title'] + ' — Manuel Paez', e['description'],
             article(e, (root / source_path(e)).read_text(), link), extra_head=ARTICLE_SCRIPTS)
    if preview:
        e = json.loads((root / 'ml-notes/_templates/entry.json').read_text())
        page('ml-notes/_preview/article.html', e['title'] + ' — Manuel Paez', e['description'],
             article(e, (root / 'ml-notes/_templates/article.html').read_text(), link),
             extra_head='<meta name="robots" content="noindex">\n' + ARTICLE_SCRIPTS)
