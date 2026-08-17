# -*- coding: utf-8 -*-
"""Shared chrome for the Mother Powers site: head, banner, header, footer, callbar."""

TEL_MAIN     = "8502641337"
TEL_MAIN_FMT = "(850) 264-1337"
TEL_ALT      = "5735871973"
TEL_ALT_FMT  = "(573) 587-1973"
CASHAPP      = "$motherpowers"
PO_BOX       = "P.O. Box 16159, Tallahassee, FL 32317"
SITE_NAME    = "Mother Powers"
TAGLINE      = "Spiritual Healer &amp; Reader"

# Navigation tree. A group with children renders as a dropdown.
#   (label, href_or_None, [ (label, href), ... ])
NAV_TREE = [
    ("About", "about.html", [
        ("Her Story",         "about.html"),
        ("Her Advertisements","dream-books.html"),
        ("Testimonials",      "testimonials.html"),
    ]),
    ("Readings", "readings.html", [
        ("All Readings & Works", "readings.html"),
        ("Love & Marriage",      "readings/love.html"),
        ("Money & Prosperity",   "readings/money.html"),
        ("Luck & Numbers",       "readings/luck.html"),
        ("Protection & Jinx",    "readings/protection.html"),
        ("Cleansing & Peace",    "readings/cleansing.html"),
        ("Reading & Guidance",   "readings/guidance.html"),
    ]),
    ("The Numbers", "lucky-numbers.html", [
        ("Lucky Numbers",     "lucky-numbers.html"),
        ("Numerology",        "numerology.html"),
        ("Dream Dictionary",  "dream-dictionary.html"),
    ]),
    ("The Work", "how-it-works.html", [
        ("How It Works",      "how-it-works.html"),
        ("Candles &amp; Incense","candle-meanings.html"),
        ("Prayers & Psalms",  "prayers.html"),
        ("Questions",         "faq.html"),
    ]),
    ("Contact", "contact.html", []),
]

# Flat list of every page, for the footer and the link checker.
ALL_PAGES = [("Home", "index.html")]
for _lbl, _href, _kids in NAV_TREE:
    if _kids:
        ALL_PAGES += _kids
    elif _href:
        ALL_PAGES.append((_lbl, _href))

ICON = {
 "phone": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 "arrow": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "star":  '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.4l2.9 6 6.6.9-4.8 4.6 1.2 6.5-5.9-3.1-5.9 3.1 1.2-6.5L2.5 9.3l6.6-.9z"/></svg>',
 "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
 "shield":'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
 "moon":  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
 "flame": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2s5 5.2 5 9.5a5 5 0 0 1-10 0C7 9 9 6.5 9 6.5S10 9 11 9c1.2 0 1-4.5 1-7z"/></svg>',
 "cart":  '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3h2.6l2.2 11.2a1.7 1.7 0 0 0 1.7 1.3h8.4a1.7 1.7 0 0 0 1.7-1.3L21 7H6"/></svg>',
 "plus":  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
 "trash": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/></svg>',
 "usa":   '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.6 2.8 4 6 4 9.5s-1.4 6.7-4 9.5c-2.6-2.8-4-6-4-9.5s1.4-6.7 4-9.5z"/></svg>',
}

# The gold seal used as the brand mark.
MARK = '''<svg class="mark" viewBox="0 0 64 64" fill="none" aria-hidden="true">
<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#5f43a0"/><stop offset=".42" stop-color="#f4efcf"/><stop offset="1" stop-color="#b295f0"/>
</linearGradient></defs>
<circle cx="32" cy="32" r="30" stroke="url(#mg)" stroke-width="1"/>
<circle cx="32" cy="32" r="25.5" stroke="url(#mg)" stroke-width=".5" opacity=".55"/>
<path d="M32 9.5a22.5 22.5 0 1 0 15.6 38.7A18 18 0 0 1 32 9.5z" fill="url(#mg)" opacity=".92"/>
<g stroke="url(#mg)" stroke-width=".9" stroke-linecap="round">
<path d="M32 2.5v4M32 57.5v4M2.5 32h4M57.5 32h4"/></g>
<circle cx="44" cy="20" r="1.7" fill="url(#mg)"/>
<circle cx="49" cy="30" r="1.1" fill="url(#mg)"/>
<circle cx="41" cy="42" r="1.3" fill="url(#mg)"/>
</svg>'''

def rule():
    return '<div class="rule"><i></i></div>'

def head(title, desc, base="", page=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} &middot; {SITE_NAME}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="{title} · {SITE_NAME}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/site.css">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
</head>
<body data-page="{page}">'''

def banner():
    return '''<div class="demo-banner" role="status">
  <span class="theme-switch" role="group" aria-label="Colour trial">
    <button type="button" data-theme-set="amethyst" aria-pressed="true">Amethyst</button>
    <button type="button" data-theme-set="burgundy" aria-pressed="false">Burgundy&nbsp;&amp;&nbsp;Gold</button>
  </span>
  <span class="dot" aria-hidden="true"></span>
  <span><b>Preview Site</b> &mdash; Built for Mother Powers by 60 Minute Sites<span class="sep hide-xs">&middot;</span><span class="hide-xs">Sample content &amp; pricing, not yet live</span></span>
  <button class="x" type="button" aria-label="Hide preview notice" data-banner-close>&times;</button>
</div>'''

def _is_on(page, href, kids):
    return page == href or any(page == k[1] for k in kids)

def header(page, base=""):
    items = []
    for label, href, kids in NAV_TREE:
        on = ' on' if _is_on(page, href, kids) else ''
        if kids:
            sub = "".join(
                f'<a href="{base}{k[1]}"{" class=\"on\"" if page == k[1] else ""} role="menuitem">{k[0]}</a>'
                for k in kids)
            items.append(
                f'<div class="nav-item has-sub">'
                f'<a class="nav-top{on}" href="{base}{href}" aria-haspopup="true" aria-expanded="false">'
                f'{label}<svg class="chev" width="9" height="9" viewBox="0 0 12 12" aria-hidden="true">'
                f'<path d="M2 4.2 6 8.2l4-4" fill="none" stroke="currentColor" stroke-width="1.4" '
                f'stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
                f'<div class="sub" role="menu"><div class="sub-in">{sub}</div></div></div>')
        else:
            items.append(f'<div class="nav-item"><a class="nav-top{on}" href="{base}{href}">{label}</a></div>')
    desktop = "".join(items)

    groups = []
    for label, href, kids in NAV_TREE:
        if kids:
            sub = "".join(
                f'<a href="{base}{k[1]}"{" class=\"on\"" if page == k[1] else ""}>{k[0]}</a>'
                for k in kids)
            groups.append(
                f'<div class="dgroup"><button class="dgroup-t" type="button" aria-expanded="false">{label}'
                f'<span class="ic" aria-hidden="true"></span></button>'
                f'<div class="dgroup-b"><div class="dgroup-in">{sub}</div></div></div>')
        else:
            groups.append(
                f'<div class="dgroup"><a class="dgroup-t solo" href="{base}{href}">{label}</a></div>')
    drawer = "".join(groups)

    return f'''<header class="hdr">
  <div class="wrap hdr-in">
    <a class="brand" href="{base}index.html" aria-label="Mother Powers — home">
      {MARK}
      <span class="txt"><span class="n">Mother Powers</span><span class="s">Spiritual Healer</span></span>
    </a>
    <nav class="nav" aria-label="Main">{desktop}</nav>
    <div class="hdr-cta">
      <a class="hdr-tel" href="tel:+1{TEL_MAIN}">
        <span class="l">Call Mother</span><span class="n">{TEL_MAIN_FMT}</span>
      </a>
      <a class="btn btn-solid btn-sm" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call Now</a>
      <button class="cart-btn" type="button" aria-label="Cart" data-cart-open>
        {ICON["cart"]}<span class="cart-count" data-cart-count hidden>0</span>
      </button>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" data-menu>
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="drawer" aria-hidden="true">
  <div class="drawer-in">
    <a class="dhome" href="{base}index.html">Home</a>
    {drawer}
    <a class="btn btn-solid drawer-tel" href="tel:+1{TEL_MAIN}">{ICON["phone"]} {TEL_MAIN_FMT}</a>
  </div>
</div>'''

def callband(base="", heading=None, sub=None):
    heading = heading or 'Help is just a<br><span class="script gold">phone call</span> away.'
    sub = sub or ("Pick up the phone and speak with Mother Powers herself. Your call is private, "
                  "she takes her time with you, and the first blessed reading is free.")
    return f'''<section class="callband pad">
  <div class="callband-bg"><img src="{base}assets/claude-photos/prayer-candle.jpg" alt="" loading="lazy" decoding="async"></div>
  <div class="incense soft" aria-hidden="true">
    <i class="smoke s1"></i><i class="smoke s3"></i>
  </div>
  <div class="wrap narrow center">
    <p class="eyebrow center">Call Day or Night</p>
    <h2 class="d2">{heading}</h2>
    {rule()}
    <p class="lede" style="max-width:56ch;margin:0 auto 2rem">{sub}</p>
    <a class="tel-big" href="tel:+1{TEL_MAIN}">{TEL_MAIN_FMT}</a>
    <div class="btn-row center" style="margin-top:2.2rem">
      <a class="btn btn-solid btn-lg" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call Mother Powers</a>
      <a class="btn btn-ghost btn-lg" href="{base}how-it-works.html">How It Works</a>
    </div>
    <p class="small" style="margin-top:1.8rem">Or her second line: <a href="tel:+1{TEL_ALT}" style="color:var(--halo)">{TEL_ALT_FMT}</a></p>
  </div>
</section>'''

def footer(base=""):
    cols = []
    for _lbl, _href, _kids in NAV_TREE[:4]:
        _items = _kids if _kids else [(_lbl, _href)]
        cols.append((_lbl, "".join(f'<li><a href="{base}{h}">{l}</a></li>' for l, h in _items)))
    return f'''{callband(base)}
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <a class="brand" href="{base}index.html" style="margin-bottom:1.4rem">
          {MARK}
          <span class="txt"><span class="n">Mother Powers</span><span class="s">Spiritual Healer</span></span>
        </a>
        <p style="max-width:34ch">Gifted from God to help. Readings, prayer and spiritual work by
        telephone for people in every state &mdash; privately, and without judgment.</p>
        <p style="margin-top:1.2rem"><a class="tel-big" style="font-size:1.55rem" href="tel:+1{TEL_MAIN}">{TEL_MAIN_FMT}</a></p>
      </div>
      <div><h4>{cols[1][0]}</h4><ul>{cols[1][1]}</ul></div>
      <div><h4>{cols[0][0]}</h4><ul>{cols[0][1]}</ul>
           <h4 style="margin-top:1.8rem">{cols[2][0]}</h4><ul>{cols[2][1]}</ul></div>
      <div>
        <h4>Reach Mother</h4>
        <ul>
          <li><a href="tel:+1{TEL_MAIN}">{TEL_MAIN_FMT}</a></li>
          <li><a href="tel:+1{TEL_ALT}">{TEL_ALT_FMT}</a></li>
          <li>{PO_BOX}</li>
          <li>Cash App &middot; {CASHAPP}</li>
        </ul>
        <p class="tiny" style="margin-top:1.3rem">Serving all 50 states by telephone</p>
        <h4 style="margin-top:1.8rem">{cols[3][0]}</h4><ul>{cols[3][1]}</ul>
      </div>
    </div>
    <div style="margin-top:clamp(34px,4vw,52px)">
      <p class="disclaim"><b style="color:var(--muted)">Please read:</b> Spiritual readings and prayer work are offered
      for personal guidance and comfort. Mother Powers is not a physician, attorney, or licensed financial adviser,
      and nothing offered here is medical, legal, or financial advice, or a substitute for professional care.
      No specific outcome is promised or guaranteed. Services are for adults 18 and over.
      If you are in crisis, call or text <a href="tel:988" style="color:var(--gold-lt)">988</a> in the United States.</p>
    </div>
    <div class="ftr-bot">
      <p>&copy; <span data-year>2026</span> Mother Powers. All rights reserved.</p>
      <p class="ftr-legal"><a href="{base}privacy.html">Privacy</a> &middot;
         <a href="{base}terms.html">Terms</a> &middot;
         <a href="{base}disclaimer.html">Disclaimer</a></p>
      <p>Preview built by 60 Minute Sites</p>
    </div>
  </div>
</footer>
<div class="callbar">
  <a class="a1" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call Mother Now</a>
  <button class="a2" type="button" data-cart-open>{ICON["cart"]} <span data-cart-count-m>Cart</span></button>
</div>

<!-- Cart. Checkout is a phone call, by design — she asked for no online payment. -->
<div class="cart-scrim" data-cart-scrim hidden></div>
<aside class="cart-panel" data-cart-panel aria-hidden="true" aria-label="Cart">
  <div class="cart-head">
    <div>
      <p class="eyebrow" style="margin:0 0 .3rem">Your cart</p>
      <h2 class="d4" style="font-size:1.35rem">Ready to check out</h2>
    </div>
    <button class="cart-x" type="button" aria-label="Close" data-cart-close>&times;</button>
  </div>
  <div class="cart-body" data-cart-body></div>
  <div class="cart-foot" data-cart-foot hidden>
    <div class="cart-total"><span>Total</span><b data-cart-total>$0</b></div>
    <div class="checkout-note">
      <p class="eyebrow" style="margin:0 0 .5rem">To check out</p>
      <p style="margin:0">Call Mother Powers and tell her what is in your cart. She takes it from
      there &mdash; and she will tell you if you need less than you put in.</p>
    </div>
    <a class="btn btn-solid btn-lg cart-go" style="width:100%;margin-top:1rem" href="tel:+1{TEL_MAIN}">
      {ICON["phone"]}<span>Check Out<b>{TEL_MAIN_FMT}</b></span></a>
    <button class="cart-clear" type="button" data-cart-clear>Empty the cart</button>
  </div>
</aside>
<div class="toast" data-toast aria-live="polite"></div>
<script src="{base}assets/js/site.js"></script>
</body>
</html>'''
