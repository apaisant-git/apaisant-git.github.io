# Apaisant site

The static site for [apaisant.org](https://apaisant.org). Plain HTML, CSS, and a
little Python for the legal pages. No build step, no dependencies, no third-party
calls (no fonts, analytics, or trackers). Hosted on GitHub Pages.

## Structure

```
index.html              Apaisant landing
quietskies/
  index.html            QuietSkies product page
  privacy/index.html    generated from Privacy_Policy.md
  terms/index.html      generated from Terms_of_Use.md
css/style.css           the design system
assets/                 logo, app icon, favicons
build_docs.py           regenerates the privacy/terms pages
CNAME                   apaisant.org
```

## Updating the privacy policy or terms

Edit the source markdown in the QuietSkies project
(`Privacy_Policy.md`, `Terms_of_Use.md`), then regenerate:

```
python build_docs.py
```

It strips the internal draft banner and rebuilds the two HTML pages.

## Local preview

```
python -m http.server 8123
```

then open http://localhost:8123/ (a server is needed so the site-absolute paths
like `/css/style.css` resolve).

## Deployment

GitHub Pages serves the `main` branch at the root. The `CNAME` file points the
site at `apaisant.org`; DNS for the apex domain is set at the registrar (A/AAAA
records to GitHub Pages, plus a `www` CNAME). "Enforce HTTPS" is enabled in the
repo's Pages settings once the certificate is issued.
