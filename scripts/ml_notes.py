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
    'reinforcement-learning': 'Post-Training and Reinforcement Learning',
}
RESOURCES = {
    'Language Model Pretraining and Architecture': [
        ('Stanford CS 312 — Deep Learning Alchemy', 'https://cs312.stanford.edu/'),
        ('Stanford CS 336 — Language Modeling from Scratch', 'https://cs336.stanford.edu/'),
        ('Stanford MS&E 319 — Efficient Generative Language Models', 'https://web.stanford.edu/class/msande319/'),
    ],
    'Mathematical Foundations of Deep Learning': [
        ('Theodor Misiakiewicz — Mathematics of Deep Learning', 'https://misiakie.github.io/SDS659.html'),
        ('Matus Telgarsky — Deep Learning Theory', 'https://mjt.cs.illinois.edu/dlt/'),
        ('The Principles of Deep Learning Theory', 'https://deeplearningtheory.com/'),
        ('Francis Bach — Machine Learning Research Blog', 'https://francisbach.com/'),
    ],
    'High-Dimensional Statistics and Statistical Mechanics': [
        ('Song Mei — Mean Field Asymptotics in Statistical Learning', 'https://www.stat.berkeley.edu/~songmei/Teaching/STAT260_Spring2021/index.html'),
        ('Statistical Physics for Optimization and Learning', 'https://idephics.github.io/EPFLDoctoralLecture2023/'),
    ],
    'Industry Pretraining and Training Systems': [
        ('Marin — Open Pretraining Research', 'https://marin.community/'),
        ('The Smol Training Playbook', 'https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook'),
        ('How to Scale Your Model', 'https://jax-ml.github.io/scaling-book/'),
        ('The Ultra-Scale Playbook', 'https://huggingface.co/spaces/nanotron/ultrascale-playbook'),
        ('NanoGPT Speedrun', 'https://github.com/KellerJordan/modded-nanogpt'),
    ],
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

def landing(entries, link):
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
<p>A curated collection of external courses, mathematical lecture notes, monographs, technical reports, and industry research resources.</p>''')
    for title, resources in RESOURCES.items():
        parts.append(f'<div class="resource-group"><h4>{escape(title)}</h4><ul class="notebook-list">')
        parts.extend(f'<li>{link(title, url)}</li>' for title, url in resources)
        parts.append('</ul></div>')
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
         'Mathematical notes, training reports, and research investigations into modern deep learning.', landing(entries, link))
    for e in entries:
        page(article_path(e), e['title'] + ' — Manuel Paez', e['description'],
             article(e, (root / source_path(e)).read_text(), link), extra_head=ARTICLE_SCRIPTS)
    if preview:
        e = json.loads((root / 'ml-notes/_templates/entry.json').read_text())
        page('ml-notes/_preview/article.html', e['title'] + ' — Manuel Paez', e['description'],
             article(e, (root / 'ml-notes/_templates/article.html').read_text(), link),
             extra_head='<meta name="robots" content="noindex">\n' + ARTICLE_SCRIPTS)
