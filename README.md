# Jewellery — Fine Jewellery, Indore

Static marketing + lead-generation site for a jewellery showroom. No build step,
no framework, no runtime dependencies.

## Files

```
index.html            Landing page (all sections)
privacy.html          DPDP Act 2023 compliant privacy policy
terms.html            Terms of sale, hallmarking, returns
manifest.webmanifest  PWA manifest
robots.txt            Crawler directives
sitemap.xml           Search sitemap
generate_images.py    Procedural artwork generator (Pillow + numpy)
assets/
  hero.jpg            1920x1080 hero background
  og.jpg              1200x630 social share card
  atelier.jpg         Workbench scene for the story block
  product-*.jpg       6 product images, 800x1000
  look-*.jpg          6 lookbook tiles, 800x1067
  favicon.svg         Brand mark
```

## Run locally

Double-click `index.html`. No server is needed — there are no `fetch` calls, no
CDN dependencies and no ES modules, so `file://` works.

To test on localhost instead:

```powershell
python -m http.server 5173
# open http://127.0.0.1:5173
```

## Regenerate artwork

All images are drawn from code, not sourced externally.

```powershell
python generate_images.py
```

Requires `pillow` and `numpy`. Re-running overwrites `assets/`. To use real
product photography, drop files with the same names into `assets/` — the HTML
references fixed paths so nothing else needs to change.

## Deploy

### Vercel

```powershell
npm i -g vercel
vercel --prod
```

No framework preset is required. If prompted, use **Other** and keep the output
directory as the project root.

### Netlify

Drag the folder onto <https://app.netlify.com/drop>, or:

```powershell
netlify deploy --prod --dir .
```

### GitHub Pages

Push to a repo and enable Pages on the branch root. All asset paths are
relative, so it works from a subpath without edits.

## Before going live

These are placeholders and **must** be replaced with the shop's real details:

| Item | Placeholder value | Where |
|---|---|---|
| Domain | `https://jewellery.example.com/` | `index.html` canonical + JSON-LD, `sitemap.xml`, `robots.txt` |
| Phone | `+91 731 400 2200` | header, stores, footer, sticky CTA, JSON-LD |
| WhatsApp | `917314001200` | floating button + sticky CTA |
| Email | `hello@jewellery.example.in` | footer, legal pages, JSON-LD |
| GSTIN | `23AABCR0000A1Z5` | footer, legal pages |
| Coordinates | `22.7196, 75.8577` | JSON-LD `geo`, map iframe |
| Instagram | `jewelleryjewellery` | JSON-LD `sameAs` |
| Privacy contact | `privacy@jewellery.example.in` | `privacy.html` |

## Forms

The enquiry form currently validates client-side and then shows a success
message without sending anything. To make it live, wire the `<form id="form">`
handler in `index.html` to a backend, Formspree, or a Google Apps Script
endpoint. Keep the existing `name`/`id` attributes so the wiring stays trivial.

## Compliance notes

- `privacy.html` is written against the Digital Personal Data Protection Act 2023.
- `terms.html` covers BIS hallmarking obligations (50 g / ₹50,000 thresholds),
  mandatory disclosure that lab-grown stones are lab-grown, and the Indian
  Consumer Protection E-Commerce Rules 2020 return requirements.
- Get a competent CA or lawyer to review both documents before you rely on them
  commercially. They are a solid starting point, not legal advice.

## Browser support

Modern evergreen browsers. Respects `prefers-reduced-motion`, and all animation
is CSS or plain ES2015 JavaScript with no polyfills.