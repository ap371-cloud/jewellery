# Jewellery — Fine Jewellery, Indore

Static marketing + lead-generation site for a jewellery showroom. No build step,
no framework, no runtime dependencies.

## Files

```
index.html              Landing page — markup only
privacy.html            DPDP Act 2023 compliant privacy policy
terms.html              Terms of sale, hallmarking, returns
manifest.webmanifest    PWA manifest
robots.txt              Crawler directives
sitemap.xml             Search sitemap
vercel.json             Security headers and cache policy for Vercel
_headers                The same headers for Netlify and Cloudflare Pages

assets/
  css/
    base.css            Design tokens, reset, reveal and focus rules
    site.css            Everything specific to the landing page
    legal.css           Privacy and terms page layout
  js/
    reveal.js           Scroll reveal, shared by the page and the catalogue
    pieces.js           The product data — the catalogue's only source of truth
    catalogue.js        Grid, filters, search, sort, detail dialog, ItemList
    site.js             Header, nav, carousel, FAQ, enquiry form
  hero.jpg              1920x1080 hero background
  og.jpg                1200x630 social share card
  atelier.jpg           Workbench scene for the story block
  product-*.jpg         18 product images, 800x1000
  look-*.jpg            6 lookbook tiles, 800x1067
  favicon.svg           Brand mark

tools/                  Asset tooling, never shipped to the browser
  slugs.py              Paths and the slug contract
  palette.py            Colour, light and backdrop helpers
  primitives.py         Gems, bands, claws, chains, coins
  products.py           One painter per catalogue piece
  editorial.py          Hero, social card, workbench, lookbook tiles
  build_images.py       Draws everything from code
  fetch_ai_images.py    Optional photographic alternative
```

Scripts are loaded as plain `<script src>` with `defer`, not as ES modules,
because modules are blocked over `file://` and this site is meant to open by
double-clicking `index.html`.

## The catalogue

`assets/js/pieces.js` is the single source of truth. Adding a piece means adding
one object to `window.JEWELLERY.pieces`; the grid, the category chips, the search
index, the detail dialog and the `ItemList` structured data all read from that
array, so they cannot drift apart.

```js
{
  id: "solitaire",           // slug, also used as the SKU suffix
  name: "Signature Solitaire",
  cat: "ring",               // must exist in JEWELLERY.categories
  added: 2026,               // drives the "newest first" sort
  flag: "new",               // optional badge text, null for none
  metal: "18k Yellow Gold",
  detail: "1.24 ct",         // short spec shown under the name
  price: 148000,             // whole rupees, GST inclusive
  was: null,                 // set to show a strike-through price
  img: "assets/product-solitaire.jpg",
  blurb: "One line for the detail dialog.",
  specs: [["Centre stone", "1.24 ct round brilliant"], ...]
}
```

What the section gives you: category chips with counts-free filtering, a text
search across name, metal and description, five sort orders, a live result
tally, six-at-a-time paging, and a detail dialog with the full spec table. The
**Enquire** button on any card writes that piece into the booking form and
scrolls you down to it, so the phone call already knows what it is about.

Prices are static. There is no cart and no checkout — this is a lead-generation
site, and every path ends in a phone call or a WhatsApp message.

## Run locally

Double-click `index.html`. No server is needed — there are no `fetch` calls, no
CDN dependencies and no ES modules, so `file://` works.

To test on localhost instead:

```powershell
python -m http.server 5173
# open http://127.0.0.1:5173
```

## Regenerate artwork

All images are drawn from code, not sourced externally. Run the tools as modules
from the repository root:

```powershell
python -m tools.build_images                             # everything
python -m tools.build_images --only product-coin         # one file
python -m tools.build_images --only product-rani --only product-bangles
```

Requires `pillow` and `numpy`. Without `--only` this rewrites `assets/`
completely, including `hero.jpg`, `og.jpg` and `atelier.jpg` — pass `--only` if
you want to keep the photographic versions of those.

`build_images.py` refuses to run if the painters, `tools/slugs.py` and the `img`
fields in `pieces.js` ever disagree about which product images exist, so adding
a product to the site without artwork fails loudly instead of shipping a broken
image.

The HTML references fixed paths, so to swap in real product photography just
drop files with the same names into `assets/`. Nothing else needs to change.

### Photographic alternative

`tools/fetch_ai_images.py` pulls proper studio photography from the free
Pollinations API instead of drawing it. No key and no account.

```powershell
python -m tools.fetch_ai_images
python -m tools.fetch_ai_images --only product-lehenga
```

The anonymous tier is rate-limited and returns HTTP 402 once the daily quota is
spent, in which case the script keeps whatever image was already on disk. Twelve
of the eighteen product images are currently procedural artwork rather than
photography; run this once the quota resets and they will all match the rest.

## Security headers

`vercel.json` and `_headers` ship the same policy to Vercel and to
Netlify/Cloudflare. The interesting part is the CSP:

```
default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:;
connect-src 'none'; form-action 'none'; frame-src https://www.openstreetmap.org;
object-src 'none'; base-uri 'none'; frame-ancestors 'none'
```

There is no `'unsafe-inline'` anywhere, and that is only true because all the CSS
lives in `assets/css` and all the JS in `assets/js`. If you add an inline
`<style>`, a `style="..."` attribute or an `onclick=` handler, the browser will
block it. Move the code into a file instead of adding `'unsafe-inline'` back.

`connect-src 'none'` means no script on the page can make a network request, so
an injected script has nowhere to send data. `form-action 'none'` means the
enquiry form cannot post anywhere until you deliberately wire it up.

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
| Coordinates | `22.7535, 75.8937` | JSON-LD `geo`, map iframe |
| Instagram | `jewelleryjewellery` | JSON-LD `sameAs` |
| Privacy contact | `privacy@jewellery.example.in` | `privacy.html` |
| Catalogue | 18 invented pieces and prices | `pieces.js` |

The shop name itself, the founder's name, the review quotes, the opening hours
and the "11,400 pieces delivered" figure are all invented too. They read as
real, so replace them before this goes in front of a customer.

## Forms

The enquiry form validates client-side and then shows a success message without
sending anything. To make it live, wire the submit handler at the bottom of
`assets/js/site.js` to a backend, Formspree, or a Google Apps Script endpoint.
Keep the existing `name`/`id` attributes so the wiring stays trivial.

Whatever you point it at, put the receiving key on a serverless function rather
than in the page. `connect-src 'none'` will block the browser from posting
anywhere until you widen that directive deliberately — which is the right moment
to think about where customer details are being sent.

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