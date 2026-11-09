# Manuel Paez — academic website

Static HTML hosted on GitHub Pages. No client-side JavaScript is required.

## Editing and building

Edit `scripts/build_site.py` for biographies, publication records, project records,
code descriptions, and shared headers. It is the single source for all six HTML
pages; do not edit generated HTML directly. Edit `src/styles.css` for styling.

Run `npm ci` when dependencies are absent, then `npm run build` and `npm run check`.
Commit generated HTML and `styles.css` along with their sources. `node_modules/`
is local-only; `package-lock.json` remains tracked. The original CSS-only command,
`npm run build-css`, is also available.

## Research-record notes

- Neural Computation: Xuehao Ding, Marco Zenari, Manuel Paez, Dmitri B. Chklovskii.
  This matches the user's explicit November 9, 2026 confirmation and approved CV.
- HiLD: retain the existing website's Liu, Paez ordering pending manuscript
  verification. The approved CV instead lists Paez, Liu; do not silently reconcile.
- The IEOR course report is a byte-identical copy of the supplied 15-page report.
  It is not a peer-reviewed paper. The separate 11-page draft is not published.
- The IEOR Slides link points to the verified 10-page presentation dated November 9,
  2026. Its bytes are preserved from the supplied presentation. The older 11-page
  article-format draft remains unpublished.
- CV and résumé PDFs must remain unchanged unless replacements are supplied.

`cv.html` redirects to the current CV PDF, and `blog.html` redirects to Substack.

External-link review: the former HiLD Code URL returned public HTTP 404 and
was replaced with the user-confirmed
`https://github.com/Chryseisliu/spectral_normalization_accelerates_feature_learning`.
Columbia, LinkedIn, and PNAS restrict automated requests; their existing
authoritative URLs are retained.
