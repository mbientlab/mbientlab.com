# mbientlab.com

Static Jekyll site for [mbientlab.com](https://mbientlab.com), deployed with GitHub Pages
through GitHub Actions. It uses a small custom theme that lives in this repo (no theme gem).

The developer documentation lives at [docs.mbientlab.com](https://docs.mbientlab.com), which is its own site and is not part of this repo.

## Local development

```sh
bundle install
bundle exec jekyll serve
```

The site is served at http://localhost:4000.

## Layout

| Path | Contents |
| --- | --- |
| `_layouts/` | `default` (shell), `page` (long-form prose), `post` (research entry), `product` (sensor pages) |
| `_includes/` | Header, footer, hero, CTA, cards and the inline SVG icon set (`icon.html`) |
| `_sass/` | `_tokens.scss` (colors, type, spacing, dark mode), `_base.scss`, `_components.scss` |
| `assets/css/main.scss`, `assets/js/main.js` | Stylesheet entry point; mobile menu, dropdowns, TOC highlighting |
| `_data/products.yml` | All MMRL and MMS content and specs; product pages render from it |
| `_data/navigation.yml` | Header and footer navigation |
| `_pages/` | Pages. Home, About, Troubleshooting and Getting started keep their content in front matter |
| `_posts/` | Research entries (`year`, `authors`, `venue`, `paper_url` in front matter), listed at `/blog/` |
| `assets/img/` | Images |
| `docs/` | Legacy datasheet PDFs, kept so old `/docs/*.pdf` links keep working |

## Theme

- Brand colors come from the original site: cyan `#01C1CB` and teal `#00ABB3`, on near-black `#14171C`.
  Text-safe darker teals (`--brand-600`/`--brand-700`) are used for links and buttons to keep WCAG AA contrast.
- Type is Inter, with JetBrains Mono for small labels, loaded from Google Fonts.
- Light and dark modes follow the visitor's system setting.
- To add a sensor, add an entry to `_data/products.yml` and a page with `layout: product` and `product: <key>`.

## Deployment

Pushes to `main` build and publish the site through `.github/workflows/pages.yml`.
Pull requests run a build check only.
