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
