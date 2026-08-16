# Mother Powers — notes for the sales call

Everything below is a decision I made so the demo could exist. All of it is
cheap to change. **Nothing here is confirmed by her.**

## Ask her to confirm

| Thing | What I used | Why |
|---|---|---|
| **Prices** | $60–$300, shown as "offering" | Invented. She told me the dream books charge $500–$600 minimum and she undercuts that, but she never gave me her numbers. This is the single biggest thing to nail down. |
| **Testimonials** | 8, written by me, first-name + state | **Fabricated for layout.** Must be replaced with real ones (or the page pulled) before launch. Flagged in the code. |
| **The free first reading** | Front and centre everywhere | Straight off her own printed ad: "For your FREE blessed reading, call Mother Powers." |
| **Two phone numbers** | 850-264-1337 primary, 850-385-3847 second | Both are on her flyers. I made 264-1337 primary because it's the one in the dream-book ad. |
| **Home address** | **Left off deliberately.** PO Box only. | Her flyers print 1805 Gibbs Drive. She works out of her home and wants national reach — putting a home address on a public site invites walk-ins. Ask before adding it. |
| **Cash App handle** | `$motherpowers` | From your notes. Confirm the `$` prefix is right. |
| **14 readings** | Named and described by me | Built from the services her ads list: love, breaking-up, luck, money, marriage, health, business, jinx removal, lucky numbers. Rename freely. |

## Things she said, and where they landed

- *"No form filling, no emails."* → **Zero forms on the site.** Every CTA is tap-to-call. There's a permanent call bar on mobile. Your Formspree is not wired in — she doesn't want it.
- *"She wants them to call her and get on the phone with her."* → The whole site funnels to one action.
- *"Nothing to do with Florida, no local advertisements."* → No city/state SEO, no map, no service-area page. Copy repeatedly says every state, by telephone.
- *"A lot of them just like to talk."* → There's a reading called *Peace of Mind & Nerves* that is explicitly "somebody to listen," and the about page says she doesn't rush people off the phone.
- *"It's more private, like going to a psychiatrist."* → Privacy is a stated promise on the home page, FAQ, contact page and privacy policy.
- *"She loves psychicrituals.com."* → I took its **structure** (mystic bios → categories → detail pages → how-it-works → FAQ) and none of its content or look. Theirs is a marketplace with a cart; hers is one woman and a telephone, so the "add to cart" is "call to begin."
- *"She collects money orders, Apple Pay, Cash App."* → All three on the contact page and every reading page.

## Copy

Written in her voice, lifted almost line-for-line from the photos of her ads:
"Change your luck now," "I am gifted to help," "Don't consider me just another
reader," "I do what others claim to do," "Help is just a phone call away,"
"Come, call, or write," "God bless — Mother Powers."

The `dream-books.html` page shows the ads themselves. It's a strong trust page —
people who've seen her page in the books for years will recognise it.

## Her photos

The 8 photos she sent are in `existing-photos(sent)/`:
- Rotation corrected. One (the Monkey Paw page) was sideways — fixed.
- All converted from Display P3 to sRGB so they don't shift colour on the web.
- Enhanced 2× upscales in `assets/photos/*-2x.jpg` — this is what the lightbox
  loads, and her small ad body-text is now readable on a phone.

I did **not** run them through AI image-to-image. That model would have
re-hallucinated the text on her ads into gibberish — the wrong tool for photos of
printed pages. Lanczos upscale + local contrast + unsharp is what actually makes
small print legible, so that's what I used.

## Imagery

All original, generated with OpenAI `gpt-image-2` — nothing scraped, no stock
licence to worry about, no other psychic site's photos. Candlelit still lifes
rather than crystal balls and purple gradients, and gold engraved ornaments as
true transparent PNGs.

## Before this goes live

- [ ] Real prices
- [ ] Real testimonials, or delete the page
- [ ] Decide on the street address
- [ ] Buy the domain
- [ ] Remove the preview banner (`banner()` in `_build/shell.py`)
- [ ] Delete `robots.txt` (it currently blocks all indexing)
- [ ] Have somebody look at `terms.html` / `privacy.html` — I drafted them, I'm not a lawyer. The "entertainment purposes" line matters in some states.

## Ideas worth raising on the call

1. **Call tracking.** A tracked number that forwards to her cell would tell you
   exactly what the ads produce. Costs a few dollars a month, changes nothing for her.
2. **The dream books are the ad channel she already trusts.** She's paying for
   those pages anyway — putting the URL on them turns a print ad into a funnel
   she can measure.
3. **She has no Instagram.** `@customspellwork` was the account you looked at,
   not hers. The dream-book gallery is enough social proof to start; Instagram
   is a later conversation and it's work she'd have to do herself.

## The cart

She said no forms and no online payment, so the cart is a cart right up until
checkout — and then checkout is a phone call. Add to cart, see a running total,
open the panel, and the checkout button dials her.

It's `localStorage` only. Nothing is transmitted, there is no backend, and no
card details are collected anywhere. Worth demoing live on the call — it lets a
browser gather what they want and then read it to her, which is closer to how
she already works than a form ever would be.

## Image sets

Three sets are in the repo so they can be compared:

- `assets/clean-image-gen/` — the ChatGPT posters. Best of the three and the
  closest match to the site palette. These are placed on home, readings,
  about, lucky-numbers, contact and how-it-works.
- `assets/web-gen/` — the earlier ChatGPT ads (gold). On `dream-books.html`.
- `assets/claude-photos/` — my API still lifes and ornaments. Still doing the
  work everywhere else; they weren't replaced.

One caution: `web-gen/catalog-*.jpg` are Double Red Lucky's catalogue pages,
not hers — their products, their prices, their 1-800 number. They're used on
`dream-books.html` only to make the price-contrast argument, and the caption
says plainly that they are not hers and she does not sell them. Don't move
them anywhere that reads as her own product list.
