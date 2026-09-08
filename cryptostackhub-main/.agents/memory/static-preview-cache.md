---
name: Static preview cache refresh
description: Replit Preview can retain an older static stylesheet response across workflow restarts.
---

When a static HTML/CSS change is not reflected in the preview even though the server serves the new file, use a cache-busting query on the asset URL before rechecking.

**Why:** Restarting a simple static server does not necessarily clear the preview browser's cached assets.

**How to apply:** For visual changes that appear ignored, verify the served file first, then append a meaningful version query to the changed stylesheet or script reference.