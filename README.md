# Website Source

`docs/` is the canonical source of truth for the Pinr marketing site and hosted legal pages.

## What lives here

- `index.html`: live landing page source for `https://getpinr.com`
- `privacy-policy.html`, `terms-of-service.html`, `faq.html`: public legal/support pages
- `assets/`, `slides/`, `.well-known/`, `CNAME`, `.nojekyll`: static website assets and hosting metadata

## Deployment model

- This repo is private, and GitHub Pages cannot be hosted from it on the current plan.
- Because of that, a public mirror repo (`builtbylee/pinr-website`) is used only as the deployment target.
- The source of truth remains here in `docs/`.
- Mirror automation lives in `/Users/lee/Projects/primal-singularity/.github/workflows/sync-website-mirror.yml`.

## Editing rule

If you need to change the website, edit `docs/` here first. Do not treat `pinr-website` as the canonical editing location.

## Home page (Souvenir design, Nov 2026)

- `index.html` is generated: edit `tools/home.html` (the page) and run `python3 tools/build.py`. `tools/frags.json` holds the
  approved board X8's scenes (pin positions on the globe pictures) cut from the Souvenir design reference page.
- `assets/v2/`: styles (`site.css`), script (`site.js`), self-hosted fonts (Bricolage Grotesque, Spline Sans Mono; OFL),
  images (WebP) and the two globe loops. Each loop has a transparent HEVC `.mov` (Safari and every iPhone browser) and a
  transparent VP9 `.webm` (Chrome, Firefox, Android); `site.js` picks one. `-sm` is the smaller hero loop for phones.
- The globe loops are frame-exact renders of the real clay globe from the design reference page (30 s turn, 11 s horizon).
- The hero phone shows real captures of the 1.1.0 app (demo account); the Lisbon photo is CC0 from Wikimedia Commons.
- FAQ, privacy and terms use the same stylesheet; their wording is unchanged from before the redesign.
