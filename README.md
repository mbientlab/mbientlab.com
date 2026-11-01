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
| `_pages/` | Site pages (home, store, about, documentation, ...) |
| `_posts/` | Research and publication entries, listed at `/blog/` |
| `_data/navigation.yml` | Top navigation |
| `assets/img/` | Images |
| `docs/` | Product datasheet PDFs |
| `tools/convert.py` | One-off WordPress/Elementor export converter used for the initial import |
| `.github/workflows/` | `pages.yml` deploys `main`; `build.yml` checks pull requests |

## Deployment

Pushes to `main` build and publish the site through `.github/workflows/pages.yml`.
Pull requests run a build check only.

## Known gaps from the WordPress site

The old site ran WooCommerce. Cart, checkout, accounts and per-product pages have no static
equivalent, so product links point to `/store/` until a replacement checkout is chosen.
