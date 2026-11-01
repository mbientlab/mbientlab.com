# mbientlab.com

Static Jekyll site for [mbientlab.com](https://mbientlab.com), built on the
[Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme and deployed
with GitHub Pages through GitHub Actions.

The developer documentation lives in its own site and is not part of this repo.

## Local development

```sh
bundle install
bundle exec jekyll serve
```

The site is served at http://localhost:4000.

## Layout

| Path | Contents |
| --- | --- |
| `_pages/` | Site pages (home, about, documentation, product pages, ...) |
| `_posts/` | Research and publication entries, listed at `/blog/` |
| `_data/navigation.yml` | Top navigation |
| `assets/img/` | Images |
| `docs/` | Product datasheet PDFs |
| `tools/convert.py` | One-off WordPress/Elementor export converter used for the initial import |
| `.github/workflows/` | `pages.yml` deploys `main`; `build.yml` checks pull requests |

## Deployment

Pushes to `main` build and publish the site through `.github/workflows/pages.yml`.
Pull requests run a build check only.

## Scope

The old WordPress site also ran a WooCommerce store. Store, pricing, cart, checkout and account
pages are intentionally not part of this site.
