# -*- coding: utf-8 -*-
"""Static site generator for Mother Powers. Emits plain HTML — no runtime deps."""
import os, sys, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.dirname(HERE)
from shell import (head, banner, header, footer, callband, rule, ICON, MARK,
                   TEL_MAIN, TEL_MAIN_FMT, TEL_ALT, TEL_ALT_FMT, CASHAPP, PO_BOX)
from content import (CATEGORIES, OFFERINGS, TESTIMONIALS, FAQ, DREAM_BOOKS,
                     CANDLES, INCENSE, PRAYERS, DREAM_SIGNS, NUMEROLOGY)

def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)
    print(f"  {path}  ({len(html)//1024}K)")

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&mdash;", "—").replace("&rsquo;", "'")

CAT_NAME = {c[0]: c[1] for c in CATEGORIES}
CAT_IMG  = {c[0]: c[2] for c in CATEGORIES}
BY_SLUG  = {o[0]: o for o in OFFERINGS}

def price_html(p):
    return 'By offering' if p == "Free" else f'<span style="font-size:.55em;vertical-align:.35em">$</span>{p}'

# ---------------------------------------------------------------- components
def offering_card(o, base="", tag=None):
    slug, title, cat, price, lead, img, bullets, body = o
    tag_html = f'<span class="card-tag">{tag}</span>' if tag else \
               f'<span class="card-tag">{CAT_NAME[cat]}</span>'
    price_lbl = "Free of charge" if price == "Free" else f"${price}"
    return f'''<article class="card">
  {tag_html}
  <div class="card-img"><img src="{base}assets/claude-photos/{img}.jpg" alt="{strip_tags(title)}" loading="lazy" decoding="async" width="900" height="675"></div>
  <div class="card-body">
    <h3>{title}</h3>
    <p>{lead}</p>
    <div class="card-foot">
      <span class="card-price">{price_lbl}<small>Offering</small></span>
      <button class="add-btn" type="button" data-add data-id="{slug}"
              data-title="{strip_tags(title)}" data-price="{'' if price == 'Free' else price}"
              data-img="{base}assets/claude-photos/{img}.jpg">
        {ICON["plus"]}<span class="add-lbl">Add to cart</span>
      </button>
    </div>
  </div>
  <a class="stretch" href="{base}readings/{slug}.html" aria-label="{strip_tags(title)}"></a>
</article>'''

def category_tile(c, base="", delay=0):
    key, name, img, blurb = c
    return f'''<article class="card tile rv rv-d{delay}">
  <div class="card-img"><img src="{base}assets/claude-photos/{img}.jpg" alt="{strip_tags(name)}" loading="lazy" decoding="async" width="900" height="900"></div>
  <div class="card-body">
    <h3 class="d4">{name}</h3>
    <p>{blurb}</p>
    <span class="card-go" style="margin-top:.4rem">See the work {ICON["arrow"]}</span>
  </div>
  <a class="stretch" href="{base}readings.html#{key}" aria-label="{strip_tags(name)}"></a>
</article>'''

def quote_block(t, delay=0):
    name, state, text = t
    stars = ICON["star"] * 5
    return f'''<figure class="quote rv rv-d{delay}">
  <div class="stars" aria-label="Five stars">{stars}</div>
  <blockquote>&ldquo;{text}&rdquo;</blockquote>
  <cite><b>{name}</b>{state} &middot; by telephone</cite>
</figure>'''

def acc_block(items):
    rows = "".join(f'''<div class="acc-item">
  <button class="acc-q" type="button" aria-expanded="false">{q}<span class="ic" aria-hidden="true"></span></button>
  <div class="acc-a"><div class="acc-a-in">{a}</div></div>
</div>''' for q, a in items)
    return f'<div class="acc" data-acc>{rows}</div>'

def strip_band():
    items = [("usa","Readings by telephone"),("phone","She answers the phone herself"),
             ("moon","Call day or night"),("shield","Your call stays private"),
             ("flame","Prayer &amp; candle work"),("check","First reading free")]
    row = "".join(f'<span class="strip-item">{ICON[i]}{t}</span>' for i, t in items)
    return f'<div class="strip"><div class="strip-track">{row}{row}</div></div>'

def page_hero(title, sub, img, crumbs, base="", eyebrow=""):
    cr = ' <span>/</span> '.join(crumbs)
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''
    return f'''<section class="phero">
  <div class="phero-bg"><img src="{base}assets/claude-photos/{img}.jpg" alt="" decoding="async"></div>
  <div class="wrap">
    <p class="crumbs">{cr}</p>
    {eb}
    <h1 class="d2">{title}</h1>
    <div class="rule left"><i></i></div>
    <p class="lede" style="max-width:60ch">{sub}</p>
  </div>
</section>'''


def carousel(slides, base="", wide=False, cid="c"):
    """slides: list of (img_path, caption_title, caption_sub)"""
    w = " wide" if wide else ""
    items = "".join(f'''<div class="carousel-slide{w}">
      <figure class="carousel-fig"><img src="{base}{src}" alt="{strip_tags(t)}" loading="lazy" decoding="async"></figure>
      <figcaption class="carousel-cap"><b>{t}</b>{sub}</figcaption>
    </div>''' for src, t, sub in slides)
    return f'''<div class="carousel" data-carousel id="{cid}">
  <div class="carousel-track" aria-label="Gallery">{items}</div>
  <div class="carousel-nav">
    <button class="car-btn" type="button" data-car-prev aria-label="Previous">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
    </button>
    <div class="car-dots"></div>
    <button class="car-btn" type="button" data-car-next aria-label="Next">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
    </button>
  </div>
</div>'''

POSTERS = [
 ("assets/clean-image-gen/01-change-your-luck.jpg",      "Change Your Luck Now",   "Love &middot; Luck &middot; Marriage &middot; Money &middot; Protection"),
 ("assets/clean-image-gen/02-gifted-to-help.jpg",        "I Am Gifted To Help",    "Spiritual healer, reader &amp; advisor"),
 ("assets/clean-image-gen/03-spiritual-readings.jpg",    "Spiritual Readings",     "&ldquo;Peace of mind begins with one call&rdquo;"),
 ("assets/clean-image-gen/07-the-work.jpg",              "The Work",               "Prayer and guidance for the road ahead"),
 ("assets/clean-image-gen/08-turn-your-luck-around.jpg", "Turn Your Luck Around",  "Bad luck &middot; Blocked roads &middot; Money worries"),
 ("assets/clean-image-gen/05-power-of-prayer.jpg",       "God-Given Power of Prayer", "Your first blessed reading is free"),
 ("assets/clean-image-gen/04-call-day-or-night.jpg",     "Call Day or Night",      "&ldquo;I answer my own telephone&rdquo;"),
]

HER_ADS = [
 ("assets/web-gen/ad-change-your-luck.jpg",     "Change Your Luck Now",  "Spiritual healer &amp; numerologist"),
 ("assets/web-gen/ad-spiritual-readings.jpg",   "Spiritual Readings",    "&ldquo;Don&rsquo;t consider me just another reader&rdquo;"),
 ("assets/web-gen/ad-power-of-prayer.jpg",      "God Given Power of Prayer", "Reader &amp; advisor"),
 ("assets/web-gen/ad-success-love-laughter.jpg","Success, Love, Laughter", "&ldquo;I do what others claim to do&rdquo;"),
]


# ---------------------------------------------------------------- pages
def build_home():
    cats = "".join(category_tile(c, delay=i % 6 + 1) for i, c in enumerate(CATEGORIES))
    featured = [BY_SLUG[s] for s in ("reunite-the-separated","jinx-removal","lucky-numbers-reading","money-drawing")]
    feat = "".join(f'<div class="rv rv-d{i+1}">{offering_card(o)}</div>' for i, o in enumerate(featured))
    quotes = "".join(quote_block(t, i % 3 + 1) for i, t in enumerate(TESTIMONIALS[:3]))
    steps = [
      ("Pick up the telephone", "You dial the number and Mother Powers answers it herself. Day or night \u2014 she has taken calls at two in the morning."),
      ("Tell her what is wrong", "In your own words, at your own pace. She has heard it before and she does not judge anybody. This part is free."),
      ("She prays and she reads", "Mother tells you plainly what she sees — whether the trouble is natural or not, and what she would do about it."),
      ("The work is done", "If there is work to be done, she tells you what it takes before anything is paid. Then she calls you back as it moves."),
    ]
    steps_html = "".join(f'''<div class="step rv rv-d{i+1}"><span class="num" aria-hidden="true"></span>
      <h3>{t}</h3><p>{d}</p></div>''' for i, (t, d) in enumerate(steps))

    return head("Spiritual Healer, Reader &amp; Numerologist",
        "Mother Powers — spiritual healer, reader and numerologist. Readings, prayer and spiritual work "
        "by telephone in every state. The first blessed reading is free. Call (850) 264-1337.",
        page="index.html") + banner() + header("index.html") + f'''
<section class="hero">
  <div class="hero-bg">
    <picture>
      <source media="(max-width:700px)" srcset="assets/claude-photos/hero-mobile.jpg">
      <img src="assets/claude-photos/hero-altar.jpg" alt="A candlelit altar with prayer candles, an open book of psalms and dried herbs" fetchpriority="high" decoding="async">
    </picture>
  </div>
  <div class="incense" aria-hidden="true">
    <i class="smoke s1"></i><i class="smoke s2"></i><i class="smoke s3"></i><i class="ember"></i>
  </div>
  <div class="hero-in">
    <div class="wrap">
      <p class="eyebrow rv">Spiritual Healer &middot; Reader &middot; Numerologist</p>
      <h1 class="d1 rv rv-d1">Change your luck<br><span class="script gold flicker">now.</span></h1>
      <p class="lede rv rv-d2">Having bad luck, or been touched by evil hands? Do you need help in love, luck,
      marriage, money &mdash; or even sickness that is not natural? Mother Powers is gifted from God to help,
      and help is just a phone call away.</p>
      <div class="btn-row rv rv-d3">
        <a class="btn btn-solid btn-lg" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call {TEL_MAIN_FMT}</a>
        <a class="btn btn-ghost btn-lg" href="readings.html">See the Readings</a>
      </div>
      <p class="small rv rv-d4 hero-note">Call today &middot; Your first blessed reading is free</p>
    </div>
  </div>
</section>

{strip_band()}

<section class="pad tint">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        <img class="split-img" src="assets/claude-photos/about-altar.jpg" alt="An open Bible, a wooden rosary and a burning candle on a dark table"
             loading="lazy" decoding="async" width="1024" height="1280">
      </div>
      <div class="rv rv-d2">
        <p class="eyebrow">Don&rsquo;t consider me just another reader</p>
        <h2 class="d2">I am gifted<br>to <span class="script gold">help you.</span></h2>
        <div class="rule left"><i></i></div>
        <p class="lede">&ldquo;God himself cannot come down &mdash; but He has gifted people such as me to
        help you, through your time in need, whether it is through love, luck, happiness, sickness,
        marriage, health or business.&rdquo;</p>
        <p style="color:var(--muted)">Mother Powers has been reading and praying for people for a lifetime,
        and her page has run in print for more than thirty years. You may have read it somewhere, or heard
        about her from somebody who called her first. She answers her own telephone, she takes her time with you, and she tells you the truth
        even when the truth is that there is nothing wrong.</p>
        <p style="color:var(--muted)">And I promise that my work is through God. If you are suffering, sick,
        or worried, I want to hear from you. God did not put you here to suffer &mdash; He put you here for
        a purpose. <b class="gold">I can help you.</b></p>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn" href="about.html">About Mother Powers</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="pad">
  <div class="wrap">
    <div class="center rv" style="max-width:640px;margin:0 auto clamp(38px,5vw,60px)">
      <p class="eyebrow center">The Work</p>
      <h2 class="d2">What people call<br>Mother Powers <span class="script gold">for</span></h2>
      {rule()}
      <p style="color:var(--muted)">Every reading begins the same way &mdash; a prayer and a conversation.
      Where it goes from there depends on what she finds.</p>
    </div>
    <div class="grid g3">{cats}</div>
  </div>
</section>

<section class="pad tint-deep">
  <div class="wrap">
    <div class="center rv" style="max-width:620px;margin:0 auto clamp(38px,5vw,60px)">
      <p class="eyebrow center">Most Requested</p>
      <h2 class="d2">Her best-known <span class="script gold">works</span></h2>
      {rule()}
    </div>
    <div class="grid g4">{feat}</div>
    <div class="btn-row center rv" style="margin-top:clamp(34px,4vw,52px)">
      <a class="btn" href="readings.html">View All Readings &amp; Works</a>
    </div>
  </div>
</section>

<section class="pad">
  <div class="wrap">
    <div class="split wide-right top">
      <div class="rv sticky-col">
        <p class="eyebrow">Simple as it sounds</p>
        <h2 class="d2">How it <span class="script gold">works</span></h2>
        <div class="rule left"><i></i></div>
        <p style="color:var(--parchment)">Call today and Mother answers the telephone herself. No secretary,
        no service, nobody in between. It stays between the two of you, and that is how the people who
        call her want it.</p>
        <div class="btn-row" style="margin-top:1.8rem">
          <a class="btn btn-solid" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call Now</a>
        </div>
      </div>
      <div class="steps">{steps_html}</div>
    </div>
  </div>
</section>

<section class="pad tint">
  <div class="wrap">
    <div class="center rv" style="max-width:620px;margin:0 auto clamp(38px,5vw,58px)">
      <p class="eyebrow center">In Their Own Words</p>
      <h2 class="d2">One call will<br><span class="script gold">convince you</span></h2>
      {rule()}
    </div>
    <div class="grid g3">{quotes}</div>
    <div class="btn-row center rv" style="margin-top:clamp(34px,4vw,52px)">
      <a class="btn" href="testimonials.html">Read More</a>
    </div>
  </div>
</section>

<section class="pad tint">
  <div class="wrap">
    <div class="center rv" style="max-width:640px;margin:0 auto clamp(34px,4.5vw,54px)">
      <img src="assets/claude-photos/orn-moonphases.png" alt="" class="orn" style="max-width:300px;margin-bottom:1.8rem" loading="lazy">
      <p class="eyebrow center">Thirty years in print</p>
      <h2 class="d2">You may already<br>know her <span class="script gold">name</span></h2>
      {rule()}
      <p style="color:var(--parchment)">Mother Powers&rsquo; page has run in print for more than thirty
      years. A great many of the people who call her had been reading it a long time before they ever
      picked up the telephone.</p>
    </div>
    <div class="rv">{carousel(POSTERS, cid="posters")}</div>
    <div class="btn-row center rv" style="margin-top:clamp(28px,3.5vw,42px)">
      <a class="btn btn-ghost" href="dream-books.html">See Her Advertisements</a>
    </div>
  </div>
</section>
''' + footer()

def build_about():
    return head("About Mother Powers", "Mother Powers is a spiritual healer, reader and numerologist. "
        "She answers her own telephone and reads for people in every state.",
        page="about.html") + banner() + header("about.html") + \
        page_hero("Gifted from God <span class='script gold'>to help.</span>",
            "&ldquo;I have appeared on television. You have heard me on the radio. You have read about me in "
            "the newspaper. Friends, I urge you to come and see me &mdash; I have been gifted from God to "
            "help people.&rdquo;",
            "about-altar", ['<a href="index.html">Home</a>', 'About'],
            eyebrow="Spiritual Healer &middot; Reader &amp; Advisor") + f'''
<section class="pad">
  <div class="wrap split wide-left top">
    <div class="rv">
      <p class="dropcap" style="color:var(--parchment)">Mother Powers has done this work for a lifetime.
      She was born gifted, and upon reaching womanhood and realizing she had the God-given power to heal,
      she devoted a lifetime to this work. She is a spiritual healer, a reader and advisor, and a
      numerologist, and she works out of the privacy of her own home in Tallahassee, Florida.</p>

      <p>Her advertisement has run in print for over thirty years, and in that time she has prayed for
      people in every state in the country &mdash; most of whom she has never met.</p>

      <p>She does not have a secretary. She does not have anybody who answers the phone for her. When you
      call Mother Powers, Mother Powers is who picks up &mdash; and if she is with somebody else, she will
      get to you as soon as she is finished, because she does not rush people off the telephone.</p>

      <p>Most of the people she reads for she has never met and never will. They call from Texas, from
      Ohio, from California, from towns she has never heard of. Distance does not stop prayer and it does
      not stop what she does. <b class="gold">Don&rsquo;t deny yourself, or other happiness. Don&rsquo;t
      let time or distance stand in your way.</b></p>

      <h3 class="d3" style="margin:2.6rem 0 1rem">What she does</h3>
      <p>She works with prayer, with candles, and with incense &mdash; frankincense above all, and myrrh
      beside it, the way it has been done since scripture.</p>
      <p>There is no problem so great that she can&rsquo;t solve. She tells you how to hold on to your job
      when you have failed, and how to succeed. She tells you your troubles and what to do about them. She
      reunites the separated. She gives lucky days and numbers.</p>
      <p>If you are troubled by conditions that are not natural, she will tell you so &mdash; and she will
      tell you plainly when your trouble is only trouble, and take nothing for saying it. She can call your
      enemies by name. She will tell you if the one you love is true or false. She will warn you gravely,
      and suggest to you wisely, and explain fully.</p>

      <h3 class="d3" style="margin:2.6rem 0 1rem">What she will not do</h3>
      <p>She will not promise you an outcome, and she will tell you to be careful of anybody who does. She
      will not take money for work you do not need. She will not keep you on the telephone running up a
      bill. And she will not discuss you with another living soul.</p>

      <p style="margin-top:2.4rem;font-family:var(--serif);font-size:1.5rem;line-height:1.5;color:var(--bone);font-style:italic">
      &ldquo;What you see and hear, your heart must believe. One visit will satisfy your heart, and you
      will see. I can help you to find happiness, contentment, peace of mind.&rdquo;</p>
      <p class="tiny" style="margin-top:.9rem">&mdash; Mother Powers</p>
    </div>

    <aside class="rv rv-d2">
      <img class="split-img" src="assets/claude-photos/about-detail.jpg" alt="A handwritten ledger of names and dates beside a candle"
           style="margin-bottom:1.6rem" loading="lazy" decoding="async">
      <div class="offer-box">
        <p class="eyebrow">At a glance</p>
        <dl class="spec" style="margin-top:.4rem">
          <div><dt>Practice</dt><dd>Spiritual healing</dd></div>
          <div><dt>Also</dt><dd>Reader &amp; advisor</dd></div>
          <div><dt>Numbers</dt><dd>Numerologist</dd></div>
          <div><dt>Reads for</dt><dd>All 50 states</dd></div>
          <div><dt>How</dt><dd>By telephone</dd></div>
          <div><dt>First reading</dt><dd>Free</dd></div>
          <div><dt>Based</dt><dd>Tallahassee, FL</dd></div>
        </dl>
        <a class="btn btn-solid" style="width:100%;margin-top:1.6rem" href="tel:+1{TEL_MAIN}">{ICON["phone"]} {TEL_MAIN_FMT}</a>
        <p class="small center" style="margin-top:.9rem">Or her second line, {TEL_ALT_FMT}</p>
      </div>
      <img src="assets/claude-photos/orn-hand.png" alt="" style="max-width:190px;margin:2.4rem auto 0;opacity:.8" loading="lazy">
    </aside>
  </div>
</section>

<section class="pad-sm">
  <div class="wrap">
    <div class="split top rv">
      <img class="split-img" src="assets/clean-image-gen/05-power-of-prayer.jpg"
           alt="Mother Powers — God-given power of prayer" loading="lazy" decoding="async">
      <img class="split-img" src="assets/clean-image-gen/02-gifted-to-help.jpg"
           alt="Mother Powers — I am gifted to help" loading="lazy" decoding="async">
    </div>
  </div>
</section>
<section class="pad tint-deep">
  <div class="wrap narrow center rv">
    <p class="eyebrow center">Her words, from the books</p>
    <h2 class="d2">&ldquo;I do what others<br><span class="script gold">claim to do.</span>&rdquo;</h2>
    {rule()}
    <p class="lede">&ldquo;I promise I won&rsquo;t disappoint you. I have helped thousands. During many
    years of practice I have brought together many in marriage, and reunited many who were separated.
    I can help you to succeed where you have failed. Remember &mdash; I am a true spiritualist, born
    gifted with power, and I can help where others have failed.&rdquo;</p>
    <p class="tiny" style="margin-top:1.6rem">God bless &mdash; Mother Powers</p>
  </div>
</section>
''' + footer()

def build_readings():
    sections = ""
    for c in CATEGORIES:
        key, name, img, blurb = c
        items = [o for o in OFFERINGS if o[2] == key]
        cards = "".join(f'<div class="rv rv-d{i%4+1}">{offering_card(o)}</div>' for i, o in enumerate(items))
        sections += f'''<section class="pad-sm" id="{key}">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(24px,3vw,38px)">
      <p class="eyebrow">{name}</p>
      <h2 class="d3">{blurb}</h2>
      <div class="rule left"><i></i></div>
    </div>
    <div class="grid g3">{cards}</div>
  </div>
</section>'''
    jump = "".join(f'<a class="btn btn-sm btn-ghost" href="#{c[0]}">{c[1]}</a>' for c in CATEGORIES)
    return head("Readings &amp; Works", "Every reading and spiritual work offered by Mother Powers — love, "
        "money, luck, protection, cleansing and guidance. The first blessed reading is free.",
        page="readings.html") + banner() + header("readings.html") + \
        page_hero("The readings &amp; <span class='script gold'>the work</span>",
            "Every call starts with a free blessed reading. What follows depends on what Mother finds. "
            "Nothing is paid before she has told you exactly what the work is and what it takes.",
            "hero-altar", ['<a href="index.html">Home</a>', 'Readings'],
            eyebrow="Come, call, or write") + f'''
<div class="wrap" style="padding-top:clamp(28px,4vw,44px)">
  <div class="btn-row rv" style="gap:10px">{jump}</div>
</div>
<section class="pad-sm">
  <div class="wrap"><div class="rv">{carousel(POSTERS[:5], cid="rposters")}</div></div>
</section>
{sections}
''' + footer()

def build_offering(o):
    slug, title, cat, price, lead, img, bullets, body = o
    b = "../"
    bl = "".join(f"<li>{x}</li>" for x in bullets)
    para = "".join(f"<p>{p}</p>" for p in body)
    related = [x for x in OFFERINGS if x[2] == cat and x[0] != slug][:3]
    if len(related) < 3:
        related += [x for x in OFFERINGS if x[0] != slug and x not in related][:3 - len(related)]
    rel = "".join(f'<div class="rv rv-d{i+1}">{offering_card(x, b)}</div>' for i, x in enumerate(related))
    price_lbl = "Free of charge" if price == "Free" else f"${price}"
    pay = ('This first reading costs nothing. If work follows, Mother tells you what it takes before '
           'anything is paid.') if price == "Free" else (
           'Mother will confirm the offering with you on the telephone before anything is sent. '
           'Cash App &middot; ' + CASHAPP + ' &middot; Apple Pay &middot; money order.')
    return head(strip_tags(title), strip_tags(lead), base=b, page="readings.html") + banner() + header("readings.html", b) + f'''
<section class="pad" style="padding-top:clamp(40px,5vw,64px)">
  <div class="wrap">
    <p class="crumbs" style="margin-bottom:clamp(24px,3vw,40px)">
      <a href="{b}index.html">Home</a> <span>/</span> <a href="{b}readings.html">Readings</a>
      <span>/</span> <a href="{b}readings.html#{cat}">{CAT_NAME[cat]}</a> <span>/</span> {strip_tags(title)}</p>
    <div class="detail">
      <div class="rv">
        <div class="detail-media">
          <img src="{b}assets/claude-photos/{img}.jpg" alt="{strip_tags(title)}" fetchpriority="high" decoding="async" width="900" height="900">
        </div>
        <div style="margin-top:clamp(28px,3.5vw,44px)">
          <p class="eyebrow">About this work</p>
          {para}
          <h3 class="d4" style="margin:2.2rem 0 1rem">What is included</h3>
          <ul class="ul-gold">{bl}</ul>
        </div>
      </div>

      <div class="detail-side rv rv-d2">
        <p class="eyebrow">{CAT_NAME[cat]}</p>
        <h1 class="d2" style="font-size:clamp(2rem,4.4vw,2.9rem)">{title}</h1>
        <div class="rule left"><i></i></div>
        <p class="lede">{lead}</p>

        <div class="offer-box" style="margin-top:2rem">
          <p class="offer-price">{price_html(price)}<sub>Offering</sub></p>
          <p class="small" style="margin-top:.9rem">{pay}</p>
          <a class="btn btn-solid btn-lg" style="width:100%;margin-top:1.6rem" href="tel:+1{TEL_MAIN}">
            {ICON["phone"]} Call to Begin &mdash; {TEL_MAIN_FMT}</a>
          <button class="btn btn-ghost" style="width:100%;margin-top:.7rem" type="button" data-add
                  data-id="{slug}" data-title="{strip_tags(title)}"
                  data-price="{'' if price == 'Free' else price}"
                  data-img="{b}assets/claude-photos/{img}.jpg">
            {ICON["plus"]}<span class="add-lbl">Add to cart</span>
          </button>
          <a class="btn btn-ghost" style="width:100%;margin-top:.7rem" href="{b}how-it-works.html">How Payment Works</a>
          <dl class="spec" style="margin-top:1.9rem">
            <div><dt>How it is done</dt><dd>By telephone</dd></div>
            <div><dt>Where</dt><dd>Any state</dd></div>
            <div><dt>First reading</dt><dd>Always free</dd></div>
            <div><dt>Privacy</dt><dd>Complete</dd></div>
            <div><dt>Arranged</dt><dd>By phone</dd></div>
          </dl>
          <p class="tiny center" style="margin-top:1.4rem">Everything is arranged on the telephone, with Mother herself.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="pad tint-deep">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(26px,3vw,40px)">
      <p class="eyebrow">Also consider</p>
      <h2 class="d3">Other work Mother does</h2>
      <div class="rule left"><i></i></div>
    </div>
    <div class="grid g3">{rel}</div>
  </div>
</section>
''' + footer(b)

def build_how():
    steps = [
     ("You call her", "Dial <a href='tel:+1"+TEL_MAIN+"' class='gold'>"+TEL_MAIN_FMT+"</a>. Mother answers her own telephone &mdash; "
      "no menu, no service, no waiting on hold. If she is with somebody else, give her a little while and "
      "call again, or try her second line, <a href='tel:+1"+TEL_ALT+"' class='gold'>"+TEL_ALT_FMT+"</a>."),
     ("You tell her what is wrong", "In your own words, in your own time. You do not have to have it "
      "organised and you do not have to explain yourself. A great many people who call are not asking for "
      "anything except somebody who will listen, and that is welcome too."),
     ("She prays with you and reads", "This is the free blessed reading, and it is free every time for a "
      "first call. Mother prays over you by name and tells you what she sees &mdash; including whether "
      "your trouble is natural or not natural."),
     ("She tells you what the work would be", "If there is work to be done she describes exactly what it "
      "is, how long it takes, and what the offering is &mdash; before a dollar changes hands. If there is "
      "nothing to be done, she will tell you that instead and charge you nothing for it."),
     ("You decide, in your own time", "Nobody is going to call you back and pressure you, and nobody is "
      "going to put you on a list. When you are ready, you call her back."),
     ("You send the offering", "Cash App is easiest &mdash; her handle is <b class='gold'>"+CASHAPP+"</b>. "
      "She also takes Apple Pay, and she has taken money orders her whole life. She will tell you on the "
      "telephone &mdash; there is nothing to type in anywhere."),
     ("The work is done, and she calls you", "Mother begins the work and stays in touch as it moves. She "
      "will tell you what to do and what not to do while it is working, and when to expect to see something."),
    ]
    steps_html = "".join(f'''<div class="step rv rv-d{min(i+1,8)}"><span class="num" aria-hidden="true"></span>
      <h3>{t}</h3><p>{d}</p></div>''' for i, (t, d) in enumerate(steps))
    pays = [("Cash App", CASHAPP, "The way most people send it. Fast, and it goes straight to her."),
            ("Apple Pay", "By telephone", "She will walk you through it on the call if you have not used it."),
            ("Money order", PO_BOX, "She has collected money orders all her life. Perfectly welcome.")]
    pay_cards = "".join(f'''<div class="offer-box rv rv-d{i+1}">
      <p class="eyebrow">{n}</p><p class="d4" style="font-family:var(--serif);color:var(--gold-lt);font-size:1.35rem;line-height:1.35">{v}</p>
      <p class="small" style="margin-top:.9rem">{d}</p></div>''' for i, (n, v, d) in enumerate(pays))
    return head("How It Works", "How a reading with Mother Powers works: you call, she prays and reads, "
        "and she tells you what the work takes before anything is paid.",
        page="how-it-works.html") + banner() + header("how-it-works.html") + \
        page_hero("How it <span class='script gold'>works</span>",
            "It is a telephone call, and that is deliberate. The people who come to Mother Powers want "
            "to speak to a person and keep it between the two of them.",
            "contact-phone", ['<a href="index.html">Home</a>', 'How It Works'],
            eyebrow="Help is just a phone call away") + f'''
<section class="pad">
  <div class="wrap split narrow-left top">
    <div class="rv sticky-col">
      <h2 class="d3">Seven steps,<br>and the first four <span class="script gold">are free.</span></h2>
      <div class="rule left"><i></i></div>
      <p style="color:var(--parchment)">Mother has done it this way her whole life. It works because
      nothing about it is automated &mdash; there is a person on the other end of the line.</p>
      <a class="btn btn-solid" style="margin-top:1.6rem" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call Now</a>
    </div>
    <div class="steps">{steps_html}</div>
  </div>
</section>

<section class="pad tint">
  <div class="wrap">
    <div class="center rv" style="max-width:600px;margin:0 auto clamp(34px,4vw,54px)">
      <p class="eyebrow center">The offering</p>
      <h2 class="d2">How people <span class="script gold">pay</span></h2>
      {rule()}
      <p style="color:var(--muted)">Always after the reading, and always after Mother has told you exactly
      what the work is.</p>
    </div>
    <div class="grid g3">{pay_cards}</div>
    <img src="assets/claude-photos/orn-key.png" alt="" class="rv" style="max-width:78px;margin:2.6rem auto 0;opacity:.85" loading="lazy">
    <p class="small center rv" style="margin-top:1.4rem;max-width:60ch;margin-left:auto;margin-right:auto">
      Mother Powers does not take card details over the telephone and will never ask you for a bank
      account number, a Social Security number, or a gift card. If anyone claiming to be her ever does,
      hang up and call her back on {TEL_MAIN_FMT}.</p>
  </div>
</section>

<section class="pad-sm">
  <div class="wrap"><div class="rv">{carousel(POSTERS[3:], cid="hposters")}</div></div>
</section>
<section class="pad-sm">
  <div class="wrap narrow rv">
    <h2 class="d3 center">Common questions</h2>
    {rule()}
    {acc_block(FAQ[:5])}
    <div class="btn-row center" style="margin-top:2.4rem"><a class="btn btn-ghost" href="faq.html">All Questions</a></div>
  </div>
</section>
''' + footer()

def build_lucky():
    return head("Lucky Numbers &amp; Numerology", "Mother Powers is a numerologist. Lucky days, lucky "
        "numbers, and numbers drawn from your dreams — worked by hand.",
        page="lucky-numbers.html") + banner() + header("lucky-numbers.html") + \
        page_hero("Lucky days,<br><span class='script gold'>lucky numbers.</span>",
            "Mother Powers is a numerologist and she has given numbers for a lifetime &mdash; long before "
            "she ever put an advertisement in a dream book.",
            "lucky-numbers", ['<a href="index.html">Home</a>', 'Lucky Numbers'],
            eyebrow="Win big money &middot; What are my lucky numbers?") + f'''
<section class="pad">
  <div class="wrap split wide-left">
    <div class="rv">
      <p class="dropcap">A printed sheet of numbers is the same sheet mailed to everybody who paid for
      it. Mother Powers has never worked that way and never will.</p>
      <p>She works your numbers by hand, from your name and your birth date, the way she was taught. Then
      she asks you about your dreams &mdash; because a dream carries numbers with it, and most people
      throw them away without ever knowing what they had.</p>
      <p>She will give you your lucky days and she will give you the days to keep your money in your
      pocket, which is the half most people never hear. <b class="gold">I also give lucky days and
      numbers.</b></p>
      <div class="btn-row" style="margin-top:2rem">
        <a class="btn btn-solid" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Ask Mother for Your Numbers</a>
        <a class="btn btn-ghost" href="readings/lucky-numbers-reading.html">See the Reading</a>
      </div>
    </div>
    <div class="rv rv-d2">
      <img class="split-img" src="assets/clean-image-gen/06-lucky-numbers.jpg"
           alt="Mother Powers — lucky numbers, lucky days and dream signs" loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="pad tint-deep">
  <div class="wrap">
    <div class="center rv" style="max-width:600px;margin:0 auto clamp(32px,4vw,50px)">
      <p class="eyebrow center">Bring her these</p>
      <h2 class="d2">What she needs<br>from <span class="script gold">you</span></h2>
      {rule()}
    </div>
    <div class="grid g4">
      {"".join(f"""<div class="offer-box rv rv-d{i+1}"><p class="offer-price" style="font-size:2.2rem">{i+1:02d}</p>
      <h3 class="d4" style="margin:.7rem 0 .5rem">{t}</h3><p class="small">{d}</p></div>"""
      for i, (t, d) in enumerate([
        ("Your full name","The name you were given, and the name you go by if they are different."),
        ("Your birth date","Month, day and year. The year matters more than people think."),
        ("Any dream","Even the parts that sound foolish. Especially those."),
        ("What you play","Three digit, four digit, Powerball, Mega Millions, or the horses."),
      ]))}
    </div>
  </div>
</section>

<section class="pad">
  <div class="wrap narrow center rv">
    <img src="assets/claude-photos/orn-sun.png" alt="" style="max-width:170px;margin:0 auto 1.8rem" loading="lazy">
    <h2 class="d3">A word before you spend</h2>
    {rule()}
    <p style="color:var(--parchment)">Your numbers are yours. Mother works them from your name, your
    birth date and your dreams, and she does not hand them to anybody else.</p>
    <p style="color:var(--parchment)">She will also tell you honestly that no number is a promise. All
    things are possible through God, and none of them are owed to us.
    <b class="gold">Play what you can afford to lose, and not one dollar more.</b></p>
  </div>
</section>
''' + footer()

def build_testimonials():
    quotes = "".join(quote_block(t, i % 4 + 1) for i, t in enumerate(TESTIMONIALS))
    return head("Testimonials", "What people say after calling Mother Powers.",
        page="testimonials.html") + banner() + header("testimonials.html") + \
        page_hero("One call will<br><span class='script gold'>convince you.</span>",
            "Mother Powers does not ask anybody for a review and she does not put names in print without "
            "permission. These are from people who called back and said she could use their words.",
            "testimonial-altar", ['<a href="index.html">Home</a>', 'Testimonials'],
            eyebrow="In their own words") + f'''
<!-- ============================================================
     PLACEHOLDER TESTIMONIALS — WRITTEN FOR LAYOUT, NOT REAL PEOPLE.
     Replace every one of these with a real, permitted quote before this
     site goes live, or delete this page and its nav entry.
     Source: _build/content.py -> TESTIMONIALS
     ============================================================ -->
<section class="pad">
  <div class="wrap"><div class="grid g3">{quotes}</div></div>
</section>
<section class="pad-sm tint-deep">
  <div class="wrap narrow center rv">
    <p class="small">Individual experiences vary and no outcome is promised or guaranteed. Testimonials
    reflect the personal experience of the people quoted. Readings and spiritual work are offered for
    personal guidance and comfort, for adults 18 and over.</p>
  </div>
</section>
''' + footer()

def build_dreambooks():
    figs = "".join(f'''<figure class="rv rv-d{i%4+1}" data-lb="assets/photos/{f}-2x.jpg">
  <img src="assets/photos/{f}.jpg"
       srcset="assets/photos/{f}-thumb.jpg 520w, assets/photos/{f}.jpg 1400w"
       sizes="(max-width:560px) 92vw, (max-width:900px) 46vw, 31vw"
       alt="{strip_tags(cap)}" loading="lazy" decoding="async">
  <figcaption><b style="color:var(--gold-lt);display:block;letter-spacing:.1em">{cap}</b>{sub}</figcaption>
</figure>''' for i, (f, cap, sub) in enumerate(DREAM_BOOKS))
    return head("Her Advertisements", "Mother Powers' own printed advertisements, in print for "
        "more than thirty years.",
        page="dream-books.html") + banner() + header("dream-books.html") + \
        page_hero("Thirty years<br><span class='script gold'>in print.</span>",
            "For more than thirty years Mother Powers&rsquo; page has run in print, and people have "
            "been calling the number on it ever since.",
            "dreambook-stack", ['<a href="index.html">Home</a>', 'Her Advertisements'],
            eyebrow="Her own pages") + f'''
<section class="pad-sm tint">
  <div class="wrap">
    <div class="center rv" style="max-width:620px;margin:0 auto clamp(30px,4vw,46px)">
      <p class="eyebrow center">Her promise in print</p>
      <h2 class="d2">You may already<br>know her <span class="script gold">page</span></h2>
      {rule()}
      <p style="color:var(--parchment)">The same promise she has made for three decades: God has
      gifted her to help you &mdash; come, call, or write, and the first blessed reading is free.</p>
    </div>
    <div class="rv">{carousel(HER_ADS, cid="ads2")}</div>
  </div>
</section>

<section class="pad">
  <div class="wrap">
    <div class="rv" style="max-width:640px;margin:0 auto clamp(28px,4vw,44px)">
      <p class="eyebrow">In print</p>
      <h2 class="d3">Her page, year after year</h2>
      <div class="rule left"><i></i></div>
      <p style="color:var(--parchment)">The advertisements people have been reading &mdash; and
      calling &mdash; for over thirty years.</p>
    </div>
    <div class="gal" data-gallery>{figs}</div>
  </div>
</section>

<div class="lightbox" data-lightbox aria-hidden="true">
  <button class="close" type="button" aria-label="Close">&times;</button>
  <button class="nav-b prev" type="button" aria-label="Previous">&lsaquo;</button>
  <img src="" alt="">
  <button class="nav-b next" type="button" aria-label="Next">&rsaquo;</button>
</div>
''' + footer()

def build_faq():
    return head("Questions", "Answers to the questions people ask before calling Mother Powers.",
        page="faq.html") + banner() + header("faq.html") + \
        page_hero("Questions people ask<br><span class='script gold'>before they call.</span>",
            "If what you want to know is not here, that is what the free first call is for. Ask her.",
            "smoke-veil", ['<a href="index.html">Home</a>', 'Questions'],
            eyebrow="Before you dial") + f'''
<section class="pad">
  <div class="wrap narrow">
    <div class="center rv" style="margin-bottom:clamp(28px,4vw,44px)">
      <img src="assets/claude-photos/orn-eye.png" alt="" style="max-width:150px;margin:0 auto" loading="lazy">
    </div>
    <div class="rv">{acc_block(FAQ)}</div>
  </div>
</section>
''' + footer()

def build_contact():
    return head("Contact &amp; Call", f"Call Mother Powers on {TEL_MAIN_FMT}. No forms, no e-mail — she "
        "answers her own telephone, and she reads for people in every state.",
        page="contact.html") + banner() + header("contact.html") + \
        page_hero("Come, call,<br>or <span class='script gold'>write.</span>",
            "Call today. Mother Powers would rather hear your voice &mdash; she can tell more from how "
            "you sound than from anything you could write down.",
            "contact-phone", ['<a href="index.html">Home</a>', 'Contact'],
            eyebrow="Day or night") + f'''
<section class="pad">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="offer-box rv">
        <p class="eyebrow">The first line</p>
        <a class="tel-big" href="tel:+1{TEL_MAIN}">{TEL_MAIN_FMT}</a>
        <p class="small" style="margin-top:1rem">Mother answers this one herself. Call day or night &mdash;
        she has picked up at two in the morning for people who had nobody else to call.</p>
        <a class="btn btn-solid" style="width:100%;margin-top:1.5rem" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Call This Number</a>
      </div>
      <div class="offer-box rv rv-d2">
        <p class="eyebrow">The second line</p>
        <a class="tel-big" href="tel:+1{TEL_ALT}">{TEL_ALT_FMT}</a>
        <p class="small" style="margin-top:1rem">If the first line is busy she is with another caller.
        Try this one, or give her a little while and call the first number back.</p>
        <a class="btn btn-ghost" style="width:100%;margin-top:1.5rem" href="tel:+1{TEL_ALT}">{ICON["phone"]} Call This Number</a>
      </div>
    </div>

    <div class="grid g3" style="margin-top:clamp(20px,2.5vw,28px)">
      <div class="offer-box rv rv-d1">
        <p class="eyebrow">To write to her</p>
        <p class="d4" style="font-family:var(--serif);color:var(--bone);line-height:1.4">{PO_BOX}</p>
        <p class="small" style="margin-top:.9rem">She reads everything that comes. But she would rather
        you called &mdash; it is faster and she can hear you.</p>
      </div>
      <div class="offer-box rv rv-d2">
        <p class="eyebrow">To send an offering</p>
        <p class="d4" style="font-family:var(--serif);color:var(--gold-lt);line-height:1.4">Cash App<br>{CASHAPP}</p>
        <p class="small" style="margin-top:.9rem">Apple Pay and money orders also welcome. Always after the
        reading, and never before.</p>
      </div>
      <div class="offer-box rv rv-d3">
        <p class="eyebrow">Where she reads</p>
        <p class="d4" style="font-family:var(--serif);color:var(--bone);line-height:1.4">Every state<br>in the country</p>
        <p class="small" style="margin-top:.9rem">Mother works out of the privacy of her own home in
        Tallahassee, Florida, and reads by telephone for people she will never meet.</p>
      </div>
    </div>

    <div class="rv" style="margin-top:clamp(30px,4vw,46px);display:flex;justify-content:center">
      <img src="assets/clean-image-gen/04-call-day-or-night.jpg"
           alt="Mother Powers — call day or night, she answers her own telephone"
           style="max-width:420px;width:100%;border:1px solid var(--line-soft);border-radius:2px"
           loading="lazy" decoding="async">
    </div>
    <div class="rv" style="margin-top:clamp(34px,4vw,52px);text-align:center">
      <img src="assets/claude-photos/orn-flourish.png" alt="" style="max-width:400px;margin:0 auto 1.6rem" loading="lazy">
      <p class="small" style="max-width:62ch;margin:0 auto">She answers her own telephone, day or night.
      Mother Powers keeps no mailing list and does not share, sell or discuss the people who call her.</p>
    </div>
  </div>
</section>
''' + footer()

def build_legal(slug, title, sub, blocks):
    body = "".join(f'<h3 class="d4" style="margin:2.2rem 0 .8rem;color:var(--gold-lt)">{h}</h3>{b}'
                   for h, b in blocks)
    return head(title, sub, page=slug) + banner() + header(slug) + \
        page_hero(title, sub, "velvet-texture", ['<a href="index.html">Home</a>', title],
                  eyebrow="Please read") + f'''
<section class="pad"><div class="wrap narrow rv">{body}</div></section>
''' + footer()



# ---------------------------------------------------------------- new pages
def build_category(cat):
    key, name, img, blurb = cat
    b = "../"
    items = [o for o in OFFERINGS if o[2] == key]
    cards = "".join(f'<div class="rv rv-d{i%4+1}">{offering_card(o, b)}</div>' for i, o in enumerate(items))
    others = "".join(
        f'<a class="btn btn-sm btn-ghost" href="{b}readings/{c[0]}.html">{c[1]}</a>'
        for c in CATEGORIES if c[0] != key)
    plain = strip_tags(name)
    return head(plain, strip_tags(blurb), base=b, page=f"readings/{key}.html") + banner() + \
        header(f"readings/{key}.html", b) + f'''
<section class="phero">
  <div class="phero-bg"><img src="{b}assets/claude-photos/{img}.jpg" alt="" decoding="async"></div>
  <div class="wrap">
    <p class="crumbs"><a href="{b}index.html">Home</a> <span>/</span>
       <a href="{b}readings.html">Readings</a> <span>/</span> {plain}</p>
    <p class="eyebrow">The work</p>
    <h1 class="d2">{name}</h1>
    <div class="rule left"><i></i></div>
    <p class="lede" style="max-width:58ch">{blurb}</p>
  </div>
</section>
<section class="pad">
  <div class="wrap"><div class="grid g3">{cards}</div></div>
</section>
<section class="pad-sm tint-deep">
  <div class="wrap center rv">
    <p class="eyebrow center">Other work Mother does</p>
    <div class="btn-row center" style="gap:10px;margin-top:1.4rem">{others}</div>
  </div>
</section>
''' + footer(b)

def build_candles():
    incense_rows = "".join(f'''<div class="inc-row rv rv-d{i%4+1}">
      <span class="inc-mark" aria-hidden="true"></span>
      <div><h3 class="d4">{n}</h3><p class="tiny" style="margin:.35rem 0 .6rem">{use}</p><p>{txt}</p></div>
    </div>''' for i, (n, use, txt) in enumerate(INCENSE))
    rows = "".join(f'''<div class="swatch rv rv-d{i%5+1}">
      <span class="dot" style="--c:{hexc}"></span>
      <div><h3 class="d4">{n}</h3><p class="tiny" style="margin:.35rem 0 .6rem">{use}</p><p>{txt}</p></div>
    </div>''' for i, (n, hexc, use, txt) in enumerate(CANDLES))
    return head("Candles &amp; Incense", "What each colour of candle and each incense — frankincense, myrrh, "
        "sage and hyssop — is burned for in Mother Powers' practice.",
        page="candle-meanings.html") + banner() + header("candle-meanings.html") + \
        page_hero("Candles, incense<br>&amp; what they <span class='script gold'>mean</span>",
            "Candles and incense both. People ask her about these more than almost anything else &mdash; "
            "and she will tell you on the telephone which one your situation actually calls for.",
            "prayer-candle", ['<a href="index.html">Home</a>', 'Candle Meanings'],
            eyebrow="Prayer &amp; candle work") + f'''
<section class="pad">
  <div class="wrap narrow"><div class="swatches">{rows}</div></div>
</section>
<section class="pad tint">
  <div class="wrap narrow">
    <div class="center rv" style="margin-bottom:clamp(30px,4vw,46px)">
      <p class="eyebrow center">What she burns</p>
      <h2 class="d2">Frankincense<br>&amp; <span class="script gold">holy smoke</span></h2>
      {rule()}
      <p style="color:var(--parchment)">Mother Powers works with incense as much as she works with
      candles. Frankincense above all &mdash; it was carried to the Lord Himself, and she has never
      known anything to lift a prayer like it.</p>
    </div>
    <div class="incense-list">{incense_rows}</div>
    <div class="btn-row center" style="margin-top:2.4rem">
      <a class="btn btn-solid" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Ask Mother What to Burn</a>
    </div>
  </div>
</section>

<section class="pad-sm tint-deep">
  <div class="wrap narrow center rv">
    <img src="assets/claude-photos/orn-flourish.png" alt="" style="max-width:340px;margin:0 auto 1.6rem" loading="lazy">
    <h2 class="d3">A word before you buy candles</h2>
    {rule()}
    <p style="color:var(--parchment)">You do not need an expensive kit. Mother has watched people spend
    five and six hundred dollars on packages and get nowhere, because nobody ever told them what they
    were for or said a prayer over them.</p>
    <p style="color:var(--parchment)">Call her first. She will tell you what your situation calls for, and
    more often than not it is one candle from the grocery store and a prayer said properly.</p>
    <div class="btn-row center" style="margin-top:2rem">
      <a class="btn btn-solid" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Ask Mother What to Burn</a>
    </div>
  </div>
</section>
''' + footer()

def build_prayers():
    rows = "".join(f'''<article class="prayer rv rv-d{i%4+1}">
      <h3 class="d4">{t}</h3><p class="tiny" style="margin:.4rem 0 .8rem">{u}</p><p>{txt}</p>
    </article>''' for i, (t, u, txt) in enumerate(PRAYERS))
    return head("Prayers &amp; Psalms", "The psalms and prayers Mother Powers works with, and what each is for.",
        page="prayers.html") + banner() + header("prayers.html") + \
        page_hero("The prayers she <span class='script gold'>works with</span>",
            "&ldquo;And I promise that my work is through God.&rdquo; These are the ones Mother comes back "
            "to most, and what she uses each of them for.",
            "about-altar", ['<a href="index.html">Home</a>', 'Prayers &amp; Psalms'],
            eyebrow="God given power of prayer") + f'''
<section class="pad">
  <div class="wrap narrow">
    <div class="rv" style="margin-bottom:clamp(28px,4vw,44px)">
      <p style="color:var(--parchment)">Mother Powers does not hand out prayers as a substitute for
      calling her, and she would tell you herself that reading a psalm off a screen is not the same as
      having somebody pray it over you by name. But people ask, so here they are.</p>
    </div>
    <div class="prayers">{rows}</div>
  </div>
</section>
<section class="pad-sm tint-deep">
  <div class="wrap narrow center rv">
    <p class="lede">&ldquo;Whatever your problem may be, all things are possible through God.&rdquo;</p>
    <p class="tiny" style="margin-top:1.2rem">&mdash; Mother Powers</p>
  </div>
</section>
''' + footer()

def build_dreamdict():
    rows = "".join(f'''<div class="acc-item">
      <button class="acc-q" type="button" aria-expanded="false">
        <span>{sign}<span class="nums">{nums}</span></span><span class="ic" aria-hidden="true"></span></button>
      <div class="acc-a"><div class="acc-a-in">{txt}</div></div>
    </div>''' for sign, nums, txt in DREAM_SIGNS)
    return head("Dream Dictionary", "Common dream signs, what Mother Powers reads them to mean, and the "
        "numbers that go with them.",
        page="dream-dictionary.html") + banner() + header("dream-dictionary.html") + \
        page_hero("The dream <span class='script gold'>dictionary</span>",
            "A dream is not always just a dream. These are the signs people bring Mother Powers most "
            "often, what she reads them to mean, and the numbers that travel with them.",
            "cat-dreams", ['<a href="index.html">Home</a>', 'Dream Dictionary'],
            eyebrow="Tell her the dream") + f'''
<section class="pad">
  <div class="wrap narrow">
    <p class="small rv" style="margin-bottom:clamp(24px,3vw,38px)">These are the general meanings.
    The same dream means different things to different people, which is why Mother would rather hear
    yours in your own words.</p>
    <div class="acc dreamdict rv" data-acc>{rows}</div>
    <div class="btn-row center" style="margin-top:clamp(34px,4vw,50px)">
      <a class="btn btn-solid btn-lg" href="tel:+1{TEL_MAIN}">{ICON["phone"]} Tell Mother Your Dream</a>
      <a class="btn btn-ghost btn-lg" href="readings/dream-interpretation.html">The Dream Reading</a>
    </div>
  </div>
</section>
<section class="pad-sm tint">
  <div class="wrap narrow center rv">
    <p class="small">Numbers are given for interest and tradition. No number is a promise, and Mother
    Powers will tell you the same thing herself: play what you can afford to lose and not one dollar more.</p>
  </div>
</section>
''' + footer()

def build_numerology():
    rows = "".join(f'''<div class="numrow rv rv-d{i%5+1}">
      <span class="numglyph">{n}</span>
      <div><h3 class="d4">{k}</h3><p>{txt}</p></div>
    </div>''' for i, (n, k, txt) in enumerate(NUMEROLOGY))
    return head("Numerology", "How Mother Powers works numbers by hand — your name, your birth date, and "
        "the year you are standing in.",
        page="numerology.html") + banner() + header("numerology.html") + \
        page_hero("Working the numbers <span class='script gold'>by hand</span>",
            "Mother Powers is a numerologist. She was taught to work numbers off a person's name and "
            "birth date, and she has done it the same way ever since.",
            "lucky-numbers", ['<a href="index.html">Home</a>', 'Numerology'],
            eyebrow="Spiritual healer &amp; numerologist") + f'''
<section class="pad">
  <div class="wrap narrow">
    <div class="rv" style="margin-bottom:clamp(30px,4vw,48px)">
      <h2 class="d3">Your personal year</h2>
      <div class="rule left"><i></i></div>
      <p style="color:var(--parchment)">Every person moves through a nine-year cycle, and where you are
      standing in it explains a great deal about why a year feels the way it does. Mother works out which
      year you are in from your birth date, and it is usually the first thing that makes a caller go quiet.</p>
    </div>
    <div class="nums">{rows}</div>
  </div>
</section>
<section class="pad tint-deep">
  <div class="wrap narrow center rv">
    <img src="assets/claude-photos/orn-moonphases.png" alt="" style="max-width:320px;margin:0 auto 2rem" loading="lazy">
    <h2 class="d2">She will work yours<br>on the <span class="script gold">telephone</span></h2>
    {rule()}
    <p class="lede">Give her your full name, your birth date, and any dream you can remember. That is all
    she needs.</p>
    <div class="btn-row center" style="margin-top:2rem">
      <a class="btn btn-solid btn-lg" href="tel:+1{TEL_MAIN}">{ICON["phone"]} {TEL_MAIN_FMT}</a>
      <a class="btn btn-ghost btn-lg" href="lucky-numbers.html">Lucky Numbers</a>
    </div>
  </div>
</section>
''' + footer()

# ---------------------------------------------------------------- run
def main():
    print("Building Mother Powers…")
    write("index.html",          build_home())
    write("about.html",          build_about())
    write("readings.html",       build_readings())
    write("how-it-works.html",   build_how())
    write("lucky-numbers.html",  build_lucky())
    write("testimonials.html",   build_testimonials())
    write("dream-books.html",    build_dreambooks())
    write("faq.html",            build_faq())
    write("contact.html",        build_contact())
    for o in OFFERINGS:
        write(f"readings/{o[0]}.html", build_offering(o))
    for c in CATEGORIES:
        write(f"readings/{c[0]}.html", build_category(c))
    write("candle-meanings.html",  build_candles())
    write("prayers.html",          build_prayers())
    write("dream-dictionary.html", build_dreamdict())
    write("numerology.html",       build_numerology())

    write("privacy.html", build_legal("privacy.html", "Privacy",
        "What Mother Powers does and does not do with anything you tell her.", [
        ("There is nothing to collect", "<p>This website has no contact form, no newsletter sign-up, no "
         "shopping cart and no account log-in. It does not ask you for your name, your e-mail address, or "
         "any payment detail, because there is nowhere on it to enter any of those things.</p>"),
        ("What happens when you call", "<p>When you telephone Mother Powers you tell her whatever you "
         "choose to tell her. She keeps her own handwritten notes so that she can remember your situation "
         "when you call back. She does not enter it into any database, she does not sell it, and she does "
         "not discuss one caller with another.</p><p>She does not keep a mailing list and she does not "
         "send e-mail.</p>"),
        ("Cookies and analytics", "<p>This site sets no cookies and runs no analytics or "
         "advertising trackers. Fonts are loaded from Google Fonts, which will see your IP address as part "
         "of serving the font files.</p>"),
        ("Your phone carrier", "<p>Calls travel over the ordinary telephone network. Mother Powers has no "
         "control over what your own carrier records about the calls you make.</p>"),
        ("Children", "<p>This site and these services are intended for adults 18 years of age and over.</p>"),
        ("Questions", f"<p>Ask her. <a class='gold' href='tel:+1{TEL_MAIN}'>{TEL_MAIN_FMT}</a>, or write to "
         f"{PO_BOX}.</p>"),
    ]))

    write("terms.html", build_legal("terms.html", "Terms",
        "The plain terms on which Mother Powers offers readings and spiritual work.", [
        ("What is offered", "<p>Mother Powers offers spiritual readings, prayer, numerology and spiritual "
         "work by telephone. These are offered for personal guidance, comfort and spiritual support.</p>"),
        ("What is not offered", "<p>Mother Powers is not a physician, a psychologist, an attorney, or a "
         "licensed financial adviser. Nothing offered here is medical, psychological, legal or financial "
         "advice, and nothing offered here is a substitute for professional care or treatment. Never stop "
         "or change a prescribed treatment on the basis of a reading.</p>"),
        ("No guarantee", "<p>No specific outcome is promised or guaranteed, and Mother Powers will tell "
         "you plainly to be careful of anybody who does promise one. Individual experiences vary.</p>"),
        ("Offerings and refunds", "<p>Offerings are discussed and agreed on the telephone before anything "
         "is sent. Once spiritual work has been performed it "
         "cannot be undone, and offerings for completed work are not refundable. If you are unhappy, call "
         f"her &mdash; <a class='gold' href='tel:+1{TEL_MAIN}'>{TEL_MAIN_FMT}</a>. She would rather hear it "
         "from you than not.</p>"),
        ("Age", "<p>Services are for adults 18 years of age and over.</p>"),
        ("Entertainment and belief", "<p>Spiritual readings are a matter of personal belief. Where required "
         "by state or local law, readings are offered for entertainment purposes.</p>"),
        ("If you are in crisis", "<p>If you are thinking about harming yourself or someone else, please "
         "call or text <a class='gold' href='tel:988'>988</a> in the United States, or dial "
         "<a class='gold' href='tel:911'>911</a>. Mother Powers will pray with you, but she is not an "
         "emergency service.</p>"),
    ]))
    write("disclaimer.html", build_legal("disclaimer.html", "Disclaimer",
        "What spiritual readings are, and what they are not.", [
        ("For guidance and comfort", "<p>Mother Powers offers spiritual readings, prayer, numerology and "
         "spiritual work. These are offered for personal guidance, comfort and spiritual support, and "
         "where required by state or local law, for entertainment purposes.</p>"),
        ("Not professional advice", "<p>Mother Powers is not a physician, psychologist, psychiatrist, "
         "attorney, accountant or licensed financial adviser. Nothing on this site or said in a reading is "
         "medical, psychological, legal or financial advice, or a diagnosis of any condition.</p>"
         "<p><b>Never stop, start or change a prescribed medication or treatment on the basis of a "
         "reading.</b> Speak to your doctor.</p>"),
        ("No guaranteed outcome", "<p>No specific result is promised or guaranteed. Individual "
         "experiences vary, and anybody who tells you otherwise should be treated carefully.</p>"),
        ("Numbers and games of chance", "<p>Lucky numbers are offered by tradition and for interest. They "
         "are not a prediction and they are not a system. Never gamble money you cannot afford to lose. "
         "If gambling has become a problem, call 1-800-GAMBLER.</p>"),
        ("Adults only", "<p>These services are for adults 18 years of age and over.</p>"),
        ("In an emergency", "<p>If you or somebody else is in danger, call <a class='gold' href='tel:911'>911</a>. "
         "If you are thinking about harming yourself, call or text <a class='gold' href='tel:988'>988</a> "
         "in the United States. Mother Powers will pray with you, and she would want you to make that call "
         "first.</p>"),
    ]))
    print("Done.")

if __name__ == "__main__":
    main()
