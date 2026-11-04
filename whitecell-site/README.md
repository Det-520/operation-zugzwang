# Zugzwang White Cell site

A Jekyll site (theme: [just-the-docs](https://github.com/just-the-docs/just-the-docs) v0.12.0) with every handout, each intelligence product on its own page, the design references, and downloads of the release PDFs. **White cell only:** it shows both sides' secrets.

- Build: `tools/build_site.sh` from the project root. It regenerates the pages from `handouts/`, `RULES.md`, and `LLAB-SETUP.md`, copies `build/` into `downloads/`, and runs `jekyll build` into `_site/`.
- Preview: `tools/build_site.sh serve`, then open http://127.0.0.1:4000.
- Generated (don't edit): `index.html`, `common/`, `redfor/`, `bluefor/`, `whitecell/`, `reference/`, `downloads/`, `tools/`, `assets/img/`.
- Hand-written: `_config.yml`, `_includes/header_custom.html`, `_includes/head_custom.html` (links `favicon.svg`, a 16 x 16 pixel-art king; the theme's `favicon.ico` is removed, and `tools/whitecell-clock.html` carries the same SVG inline), `favicon.svg`, `_sass/custom/setup.scss` (fonts), `_sass/color_schemes/zugzwang.scss` (colours), and `_sass/custom/custom.scss` (everything else). The look follows the "Repo" theme at markdown.style (GitHub's markdown style), with the same accent per audience as the PDFs: green common, red REDFOR, blue BLUEFOR, purple white cell.
- Generated also: `assets/fonts/` (JetBrains Mono, copied from `tools/fonts/`) and the section pages `*.html`. None of the generated files are in git.
- Fetched, not in git: the theme's `_layouts`, `_includes`, `_sass`, `assets` (MIT, `THEME-LICENSE.txt`), and `jekyll-include-cache` in `_plugins/` (MIT). `python3 tools/fetch_third_party.py` copies them in from the v0.12.0 and v0.3.1 releases around the hand-written files, which it never overwrites, so no `bundle install` is needed. `.gitignore` lists which files are the theme's.
