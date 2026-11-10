"""Generate static academic pages from shared bibliography and project records."""
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parents[1]

def link(text, url):
    extra = ' target="_blank" rel="noopener noreferrer"' if url.startswith('https:') or url.endswith('.pdf') else ''
    return f'<a href="{escape(url, quote=True)}"{extra}>{escape(text)}</a>'

papers = [
 ('Research Papers', 'Fast Geometric Spanners via Approximate Nearest Neighbor Search', ['Alexandr Andoni','Manuel Paez','Krish Singal','Tian Zhang'], 'Innovations in Theoretical Computer Science (ITCS), 2027. Accepted.', [('arXiv','https://arxiv.org/abs/2609.26934')]),
 ('Research Papers', 'Asymmetric Similarity Matching: A Normative Framework for Predictive Neural Computation', ['Xuehao Ding','Marco Zenari','Manuel Paez','Dmitri B. Chklovskii'], 'Submitted to Neural Computation, 2026.', []),
 # Preserve agreed website order until the HiLD manuscript author order is confirmed.
 ('Workshop Publications', 'Rank-One Spectral Normalization Accelerates Projected Feature Learning', ['Chryseis Xinyi Liu','Manuel Paez'], 'ICML 2026 Workshop on High-Dimensional Learning Dynamics (HiLD), 2026.', [('Paper','https://openreview.net/forum?id=ufLJLAUCO6'),('Code','https://github.com/Chryseisliu/spectral_normalization_accelerates_feature_learning')]),
 ('Manuscripts in Preparation', 'Low-Dimensional Embeddings of Ising Disagreement Metrics via Functional Inequalities', ['Manuel Paez','Alexandr Andoni'], 'Manuscript in preparation, 2026.', [])
]
# Optional slides field links only verified presentation PDFs.
projects = [
 ('Upper Bound Energy Barriers for Simulated Annealing in Spherical Spin Glasses', 'Manuel Paez · IEOR 8100: Log-Concave Probability · Spring 2026 · Course report', 'IEOR8100_Upper_Bound_Energy_Barriers_Spherical_Spin_Glasses_Paez_2026.pdf', None, 'projects/IEOR8100_Energy_Simulated_Annealing_Pure_Spherical_Spin_Slides_Paez_2026.pdf'),
 ('Provably Learning the Softmax Kernel of an Attention Head via the Method of Moments', 'CS 6998: Theoretical Foundations of LLMs · Course report', 'COMS6998_TheoreticalFoundationsLLMs_manuelpaez_finalproject.pdf', 'https://www.cs.columbia.edu/~djhsu/coms6998-s25/', None),
 ('Survey and Extensions for Sketching Algorithms for Earth-Mover Distance and Chamfer Distance', 'Algorithms for Massive Data · Course report', 'COMSE9886_Algorithms_for_Massive_Data_PaezGuoMckelvie.pdf', 'https://www.cs.columbia.edu/~andoni/algoF23/index.html', None),
 ('Uncovering User Information from Obfuscated K-Clustering', 'Unsupervised Learning · Course report', 'COMSW4774_ClusterPackage_ColemanEyrePaez.pdf', None, None),
 ('Spectral Sparsification', 'Advanced Algorithms · Course report', 'COMS4232_Advanced_Algorithms_finalproject_paezcunninghamnatan.pdf', None, None),
 ('Knowledge Distillation for Efficient Tiny Masked Autoencoders for Medical Imaging', 'CS 6998: Advanced Topics in Deep Learning · Course report', 'COMS6998_AdvancedTopicDL_projectreport_paezdassumlibrandi.pdf', 'https://www.advtopicsindeeplearning.com/', None)
]
notes = [
 ('Inductive Biases and Variable Creation in Self-Attention Mechanisms', 'Theoretical Foundations of LLMs · Scribed lecture notes', 'COMS6998_TheoreticalFoundationsLLMs_Edelmanscribe_paezdevaul.pdf', 'https://www.cs.columbia.edu/~djhsu/coms6998-s25/', None),
 ('Streaming for Graphs: Distance and Triangle Counting', 'Algorithms for Massive Data · Scribed lecture notes', 'COMSE6998_Algorithms_for_Massive_Data_Scribe_Lecture_2_manuelpaez.pdf', 'https://www.cs.columbia.edu/~andoni/algoF23/index.html', None),
 ('Sparse Fourier Transform', 'Algorithms for Massive Data · Scribed lecture notes', 'COMSE6998_Algorithms_for_Massive_Data_Scribe_Lecture_12_manuelpaez.pdf', 'https://www.cs.columbia.edu/~andoni/algoF23/index.html', None)
]

def paper(p):
    _, title, authors, status, links = p
    names = ', '.join('<strong>Manuel Paez</strong>' if a == 'Manuel Paez' else escape(a) for a in authors)
    status_html = escape(status)
    for venue in ['Innovations in Theoretical Computer Science (ITCS)', 'Neural Computation', 'ICML 2026 Workshop on High-Dimensional Learning Dynamics (HiLD)']:
        status_html = status_html.replace(escape(venue), '<em>'+escape(venue)+'</em>')
    return f'<li class="entry"><h3>{escape(title)}</h3><p class="authors">{names}</p><p class="metadata">{status_html}</p><p class="entry-links">'+ ' '.join(link('['+label+']',url) for label,url in links)+'</p></li>'

def project(p):
    title, meta, pdf, course, slides = p
    links = link('[Report]' if 'Course report' in meta else '[PDF]', 'projects/'+pdf)
    if course: links += ' ' + link('[Course]',course)
    if slides: links += ' ' + link('[Slides]',slides)
    return f'<li class="entry"><h3>{escape(title)}</h3><p class="metadata">{escape(meta)}</p><p class="entry-links">{links}</p></li>'

def listing(items, renderer): return '<ul class="bibliography">'+ '\n'.join(renderer(p) for p in items)+'</ul>'

def page(filename, title, description, body, home=False, redirect=None):
    nav = ' '.join(f'<a href="{url}"'+(' aria-current="page"' if filename==url else '')+f'>{name}</a>' for name,url in [('Home','index.html'),('Publications','publications.html'),('Projects','projects.html'),('Code','code.html'),('CV','manuelpaez_curriculum_vitae.pdf')])
    canonical = 'https://manuelpaeza.github.io/'+filename
    refresh = f'<meta http-equiv="refresh" content="0; url={redirect}">' if redirect else ''
    result=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&amp;family=Source+Serif+4:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="styles.css?v=20261109-source-fonts">
{refresh}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
<header class="site-header"><h1><a href="index.html">Manuel Paez</a></h1><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main" class="{'home-grid' if home else ('page-content projects-page' if filename == 'projects.html' else 'page-content')}">
{body}
</main>
</div>
</body>
</html>
'''
    (ROOT/filename).write_text(result)

def main():
    bio = f'''<section aria-labelledby="introduction"><h2 id="introduction">Introduction</h2>
    <p>Hello! I am a final-year M.S. student in Computer Science at Columbia University, where I am advised by {link('Alexandr Andoni','https://www.cs.columbia.edu/~andoni/')} and {link('Dmitri “Mitya” Chklovskii','https://neural-circuits-and-algorithms.github.io/')}. I previously earned B.A. degrees in Computer Science and Mathematics from {link('Columbia University','https://www.columbia.edu/')}.</p>
    <p>My research interests lie at the intersection of theoretical computer science, high-dimensional probability, statistical mechanics, and machine learning. I am particularly interested in high-dimensional randomized optimization, Markov chain mixing, and algorithms for sampling and inference in complex probabilistic models. More broadly, I seek to understand how the geometric and probabilistic structure of high-dimensional systems shapes computational complexity and the limits of efficient algorithms.</p></section>'''
    contacts = [('CV','manuelpaez_curriculum_vitae.pdf'),('Résumé','manuelpaez_resume_mlre.pdf'),('Google Scholar','https://scholar.google.com/citations?user=C5Fel-sAAAAJ&hl=en'),('GitHub','https://github.com/manuelpaeza'),('LinkedIn','https://www.linkedin.com/in/manuelpaeza/'),('X','https://x.com/manuel_paeza')]
    home = '<div class="main-column">'+bio+'<section><h2>Selected Publications</h2>'+listing(papers,paper)+'<p>'+link('All publications →','publications.html')+'</p></section>'
    home += '<section><h2>Teaching</h2><ul class="teaching"><li>Course Assistant, CS 6998: Algorithms for Massive Data · '+link('Fall 2025','https://www.cs.columbia.edu/~andoni/algoF25/index.html')+'</li><li>Course Assistant, CS 4995: Randomized Algorithms · Fall 2024</li></ul></section>'
    home += '<section><h2>Selected Course Projects</h2>'+listing(projects[:3],project)+'<p>'+link('All projects and lecture notes →','projects.html')+'</p></section>'
    home += '<section><h2>Personal Interests</h2><p>Outside of research, I enjoy reading novels and publications such as Bloomberg, the Financial Times, and The Economist. I also enjoy ballet, opera, and orchestral performances, visiting art galleries and coffee shops, cooking, and staying active through squash, fencing, soccer, running, and tennis.</p></section></div>'
    home += '<aside class="profile-panel" aria-label="Profile and contact"><img class="profile-photo" src="manuelpaez_profilepic_november2025.jpg" alt="Portrait of Manuel Paez"><div class="contact-links">'+' '.join(link(t,u) for t,u in contacts)+'</div><p class="contact-email">'+link('manuel.paez@columbia.edu','mailto:manuel.paez@columbia.edu')+'</p></aside>'
    page('index.html','Manuel Paez — Computer Science Research','Manuel Paez: theoretical computer science, high-dimensional probability, statistical mechanics, and machine learning.',home,True)
    pubs=''
    for category in dict.fromkeys(p[0] for p in papers): pubs+='<section><h2>'+category+'</h2>'+listing([p for p in papers if p[0]==category],paper)+'</section>'
    page('publications.html','Publications — Manuel Paez','Research papers, workshop publications, and manuscripts in preparation by Manuel Paez.',pubs)
    page('projects.html','Course Projects and Lecture Notes — Manuel Paez','Course reports and scribed lecture notes in algorithms, probability, and machine learning.','<section><h2>Course Projects</h2>'+listing(projects,project)+'</section><section><h2>Lecture Notes</h2>'+listing(notes,project)+'</section>')
    code_entries=[
     ('CaImAn: Calcium and Voltage Imaging Analysis','Migrated deep-learning training, inference, and pretrained weights from TensorFlow to PyTorch. Reintegrated scalable calcium- and voltage-imaging analysis workflows and evaluated models using HPC infrastructure.', [('Code','https://github.com/flatironinstitute/CaImAn'),('Documentation','https://caiman.readthedocs.io/en/latest/'),('Release','https://github.com/flatironinstitute/CaImAn/releases/tag/v1.13.0'),('Fork','https://github.com/manuelpaeza/CaImAn')]),
     ('NeuTorch: Neuron Boundary Segmentation','Extended NeuTorch with a supervised IsoRSUNet architecture for electron-microscopy connectome segmentation. Evaluated the model on 2.1 billion annotated voxels from three wasp specimens, reducing Rand-based split error by up to 52% relative to baseline.', [('Code','https://github.com/image-infomatics/neutorch'),('Fork','https://github.com/manuelpaeza/neutorch')]),
     ('Medical Masked Autoencoder Knowledge Distillation','Implemented PyTorch knowledge-distillation pipelines to compress masked autoencoders into tiny architectures for medical image analysis. Joint course work included training, fine-tuning, and evaluation workflows.', [('Code','https://github.com/manuelpaeza/AdvTopicsDL-Project'),('Report','projects/COMS6998_AdvancedTopicDL_projectreport_paezdassumlibrandi.pdf')]),
     ('Assembly Calculus / Assemblies','Simulated project, associate, and merge operations on neuronal populations with Hebbian plasticity and inhibition. The experiments follow Papadimitriou et al.’s “Brain computation by assemblies of neurons” (PNAS, 2020).', [('Code','https://github.com/manuelpaeza/assemblies'),('Original paper','https://www.pnas.org/content/117/25/15603')]),
     ('Quantum Pattern Detection in Gravitational-Wave Data','Developed Python/Qiskit circuits using amplitude encoding and quantum-based signal-to-noise ratio estimators. Evaluated quantum and classical estimators on gravitational-wave data.', [('Code','https://github.com/manuelpaeza/quantum_pattern_algorithm')])
    ]
    code='<section><h2>Code</h2>'
    for title,desc,links in code_entries: code+='<article class="code-entry"><h3>'+escape(title)+'</h3><p>'+escape(desc)+'</p><p class="entry-links">'+' '.join(link('['+t+']',u) for t,u in links)+'</p></article>'
    page('code.html','Code — Manuel Paez','Research software and computational projects by Manuel Paez.',code+'</section>')
    page('cv.html','Curriculum Vitae — Manuel Paez','Download Manuel Paez’s current curriculum vitae.','<section><h2>Curriculum Vitae</h2><p>Continue to '+link('the current CV (PDF)','manuelpaez_curriculum_vitae.pdf')+'.</p></section>',redirect='manuelpaez_curriculum_vitae.pdf')
    page('blog.html','Writing — Manuel Paez','Writing by Manuel Paez.','<section><h2>Writing</h2><p>Read my writing on '+link('Substack','https://substack.com/@manuelpaez')+'.</p></section>',redirect='https://substack.com/@manuelpaez')
    print('Generated six static pages.')

if __name__ == "__main__":
    main()
