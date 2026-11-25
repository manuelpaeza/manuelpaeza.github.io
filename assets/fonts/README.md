# Local IBM Plex fonts

Unmodified complete WOFF2 files from IBM's official packages:

- IBM Plex Sans: `@ibm/plex-sans` 2.0.0 — https://registry.npmjs.org/@ibm/plex-sans/-/plex-sans-2.0.0.tgz
- IBM Plex Mono: `@ibm/plex-mono` 2.5.0 — https://registry.npmjs.org/@ibm/plex-mono/-/plex-mono-2.5.0.tgz
- Upstream: https://github.com/IBM/plex

Both archive SHA-512 digests were verified against the npm registry integrity
metadata. The original SIL Open Font Licenses are included alongside the fonts.
The packages are asset sources only, not runtime or build dependencies.

`src/styles.css` declares Sans 300/400/500/600 and Mono 400/600, with true italics
for every included weight. Complete character sets preserve accented names,
Greek/Cyrillic text, and supported technical symbols without custom subsetting.
MathJax retains its own math fonts.

Only matching faces load on demand. The shared HTML template preloads Sans
Regular and Light, used by the body and navigation on every page. `font-display: swap`
keeps text readable while loading; fonts are served from the same site, without
requests to an external font service. Existing fallback families are retained.

To update, replace the selected unmodified files and licenses from a verified
IBM package, update the provenance and hashes here, and revise the stylesheet
cache version in `scripts/build_site.py`. Rebuild and run `npm run check`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `IBMPlexSans-Light.woff2` | 68,412 | `8229894b1dccb86baaa832e3c0bb106c49d68265a9d6ee0fdfc7ba7d41c9631b` |
| `IBMPlexSans-Regular.woff2` | 65,080 | `78efbe80177406a1b80d5925e706e3366290bf0d5309d7b0bd2d7f0d607f3c4c` |
| `IBMPlexSans-Medium.woff2` | 69,148 | `0497fab52b9c10f9efbec00be509b16d449a1e277098f03af929ef1e7cbddb54` |
| `IBMPlexSans-SemiBold.woff2` | 69,388 | `0fe2655c3c88b0b4c578b0046333fde7fb60d18419b9d07b4a1e115ac893e7f6` |
| `IBMPlexSans-LightItalic.woff2` | 73,176 | `d90d37e121a19bf04eaf2a78a437abe8db64fbb7bbcbb17e5200aa96865d50da` |
| `IBMPlexSans-Italic.woff2` | 69,544 | `5eeffbe5e6de923ce1ae2d1fa4d3986cfeb2433770b3cb44ad31fdbaf6443c62` |
| `IBMPlexSans-MediumItalic.woff2` | 73,876 | `4092a67809b112e68a616f33b6f3cbc0943d5a09b8e1328fb08e7552187a3ee1` |
| `IBMPlexSans-SemiBoldItalic.woff2` | 73,056 | `9967b1df279cf40d1b3adbeb92c0c82b056930f5eebeb50e9cf8b10d93268385` |
| `IBMPlexMono-Regular.woff2` | 49,248 | `ba204497f16b6d334cee9d1e963a831b73e3a56e1d6300a8489d18df7214b350` |
| `IBMPlexMono-Italic.woff2` | 53,408 | `2024bf2b08027dcd6d09091385756e327744bbe26b782c411381dffc40ffc622` |
| `IBMPlexMono-SemiBold.woff2` | 50,600 | `6a825b4824c01cbb401e829e5a066a1818411bcb3538b5a5792c5ca9b82343c3` |
| `IBMPlexMono-SemiBoldItalic.woff2` | 54,784 | `67ad8975ad3cea95517f9dfe6d67fb3e4d87ca7bc4b51fa80e797e375c0cbe71` |
