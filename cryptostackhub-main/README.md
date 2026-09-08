# CryptoStackHub — Premium Web3 Blog Website

A complete, hand-crafted static blog covering four niches: **DeFi & Crypto Education**, **Blockchain Development**, **Crypto Tax & Compliance**, and **Web3 Gaming & NFTs** — 55 pages, zero dependencies, pure HTML/CSS/JS.

## Run on Replit

1. Create a new Repl → **Import from ZIP** (or upload the zip contents into an "HTML, CSS, JS" Repl).
2. Press **Run**. The `.replit` config starts a static server on port 8000 automatically.
3. Open the webview — everything works: navigation, hubs, articles, live search, glossary, forms (demo handlers).

> Note: opening `index.html` directly as a local file works for browsing, but the live search needs the site served over HTTP (Replit does this by default).

## Structure

```
/
├── index.html                  # Home
├── search/                     # Live client-side search (assets/search-index.json)
├── defi/                       # DeFi & Crypto Education hub (10 articles)
├── developers/                 # Blockchain Development hub (10 articles)
├── tax-compliance/             # Crypto Tax & Compliance hub (10 articles)
├── gaming-nfts/                # Web3 Gaming & NFTs hub (10 articles)
├── articles/<slug>/            # 40 full articles w/ sticky TOC, share, prev/next
├── about/  contact/  write-for-us/  advertise/
├── privacy-policy/  terms/  disclaimer/
├── resources/  glossary/
├── assets/css/style.css        # Complete design system
├── assets/js/main.js           # Nav, progress bar, TOC spy, search, forms
├── sitemap.xml  robots.txt
└── build.py                    # Site generator — edit content, run `python3 build.py`
```

## Customizing

- **Edit content**: everything lives in `build.py` (articles, pages, glossary, resources). Run `python3 build.py` to regenerate.
- **Edit design**: `assets/css/style.css` — category colors are CSS variables (`--defi`, `--dev`, `--tax`, `--gaming`).
- **Forms**: contact/write/advertise forms are demo handlers in `assets/js/main.js` — wire them to Formspree/Basin for production.

Educational content only — the site carries disclaimers; keep them if you publish.

## Run locally

From the website folder, run a local static server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser. This keeps search and all root-relative links working correctly.

