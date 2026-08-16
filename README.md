# Mother Powers — Preview Site

A static demo site for **Mother Powers**, Spiritual Healer, Reader & Numerologist
(Tallahassee, FL). Built by 60 Minute Sites ahead of the sales call.

**Plain HTML, CSS and JavaScript.** No build step is required to deploy — push the
folder to any static host (GitHub Pages, Netlify, Cloudflare Pages, Railway).

## What's here

```
index.html              Home
about.html              About Mother Powers
readings.html           All readings & works, grouped by category
readings/*.html         14 individual reading pages
lucky-numbers.html      Numerology / lucky numbers
how-it-works.html       The call → reading → offering process
testimonials.html       Client words
dream-books.html        Her printed dream-book ads (lightbox gallery)
faq.html                Questions
contact.html            Phone, mail, Cash App
privacy.html terms.html Draft legal pages
robots.txt              Disallow — this is a preview, do not index

assets/css/site.css     The whole design system (one file)
assets/js/site.js       Nav, reveals, accordion, lightbox (no dependencies)
assets/img/             Site imagery + gold ornaments (transparent PNG)
assets/photos/          Her dream-book ads, deskewed and enhanced
existing-photos(sent)/  The originals she sent, rotation-corrected in place
_build/                 Optional page generator (see below)
```

## The one rule this site is built around

**There are no forms anywhere, and no checkout.** Mother Powers asked for this
explicitly: her callers do not want to type their problems into a web page. Every
call-to-action on every page is a `tel:` link. Payment is discussed on the phone
(Cash App `$motherpowers`, Apple Pay, money order) and never collected here.

Please keep it that way unless she asks otherwise.

## Editing

The HTML files are complete and readable — edit them directly if you want.

If you'd rather change something once and have it apply everywhere (the phone
number, the nav, the footer, the preview banner), edit `_build/` and re-run:

```bash
python3 _build/build.py
```

- `_build/shell.py` — header, footer, banner, phone numbers, nav
- `_build/content.py` — all copy: readings, prices, testimonials, FAQ
- `_build/build.py` — page layouts

`_build/` is not part of the deployed site; it is safe to leave in or delete.

## Local preview

```bash
python3 -m http.server 5063
```

Then open <http://localhost:5063>.

## Secrets

No API keys, tokens or credentials are in this repository, and none belong here.
`.gitignore` blocks the usual filenames as a safety net.
