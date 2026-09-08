# CryptoStackHub

## Running on Replit

This is a dependency-free static HTML/CSS/JS site. The configured `Start application` workflow serves the project root with:

```bash
python3 -m http.server 5000 --bind 0.0.0.0
```

Open the Replit Preview to browse the site. Live search requires the site to be served over HTTP.

## Regenerating pages

The content generator lives in `build.py`. After editing its content, regenerate the static pages with:

```bash
python3 build.py
```