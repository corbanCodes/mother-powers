/* Mother Powers — site behaviour. No dependencies. */
(function () {
  'use strict';
  var doc = document, body = doc.body;

  /* ---- Preview banner: dismiss for the session ---- */
  var bannerBtn = doc.querySelector('[data-banner-close]');
  if (bannerBtn) {
    try { if (sessionStorage.getItem('mp-banner') === 'off') body.classList.add('banner-hidden'); } catch (e) {}
    bannerBtn.addEventListener('click', function () {
      body.classList.add('banner-hidden');
      try { sessionStorage.setItem('mp-banner', 'off'); } catch (e) {}
    });
  }

  /* ---- Mobile drawer ---- */
  var burger = doc.querySelector('[data-menu]');
  var drawer = doc.querySelector('.drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      body.style.overflow = open ? 'hidden' : '';
    });
    drawer.addEventListener('click', function (e) {
      /* Grouped accordion inside the drawer */
      var t = e.target.closest('.dgroup-t');
      if (t && t.tagName === 'BUTTON') {
        var g = t.parentElement;
        var panel = g.querySelector('.dgroup-b');
        var wasOpen = g.classList.contains('open');
        drawer.querySelectorAll('.dgroup.open').forEach(function (o) {
          o.classList.remove('open');
          o.querySelector('.dgroup-b').style.maxHeight = '';
          o.querySelector('.dgroup-t').setAttribute('aria-expanded', 'false');
        });
        if (!wasOpen) {
          g.classList.add('open');
          panel.style.maxHeight = panel.scrollHeight + 'px';
          t.setAttribute('aria-expanded', 'true');
        }
        return;
      }
      if (e.target.tagName === 'A') {
        body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
        drawer.setAttribute('aria-hidden', 'true');
        body.style.overflow = '';
      }
    });
  }

  /* ---- Desktop dropdowns: keyboard + touch ---- */
  doc.querySelectorAll('.nav-item.has-sub').forEach(function (item) {
    var top = item.querySelector('.nav-top');
    var sub = item.querySelector('.sub');
    function close() {
      item.classList.remove('open');
      top.setAttribute('aria-expanded', 'false');
      sub.style.cssText = '';
    }
    function open() {
      item.classList.add('open');
      top.setAttribute('aria-expanded', 'true');
      sub.style.cssText = 'opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0)';
    }
    top.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault(); open();
        var first = sub.querySelector('a'); if (first) first.focus();
      }
    });
    item.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); top.focus(); } });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) close();
    });
    item.addEventListener('mouseleave', close);
  });

  /* Open the drawer group that contains the current page */
  var here = doc.querySelector('.dgroup-in a.on');
  if (here) {
    var grp = here.closest('.dgroup');
    var pnl = grp.querySelector('.dgroup-b');
    grp.classList.add('open');
    pnl.style.maxHeight = pnl.scrollHeight + 'px';
    grp.querySelector('.dgroup-t').setAttribute('aria-expanded', 'true');
  }

  /* ---- Header state on scroll ---- */
  var hdr = doc.querySelector('.hdr');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('solid', window.scrollY > 40); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Reveal on scroll ---- */
  var revealables = doc.querySelectorAll('.rv');
  if (revealables.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
      revealables.forEach(function (el) { io.observe(el); });
    } else {
      revealables.forEach(function (el) { el.classList.add('in'); });
    }
  }

  /* ---- Accordion ---- */
  doc.querySelectorAll('[data-acc]').forEach(function (acc) {
    acc.addEventListener('click', function (e) {
      var btn = e.target.closest('.acc-q');
      if (!btn) return;
      var item = btn.parentElement;
      var panel = item.querySelector('.acc-a');
      var open = item.classList.contains('open');

      acc.querySelectorAll('.acc-item.open').forEach(function (o) {
        o.classList.remove('open');
        o.querySelector('.acc-a').style.maxHeight = '';
        o.querySelector('.acc-q').setAttribute('aria-expanded', 'false');
      });
      if (!open) {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---- Lightbox for the dream-book gallery ---- */
  var lb = doc.querySelector('[data-lightbox]');
  var gal = doc.querySelector('[data-gallery]');
  if (lb && gal) {
    var figs = Array.prototype.slice.call(gal.querySelectorAll('figure[data-lb]'));
    var lbImg = lb.querySelector('img');
    var idx = 0;

    function show(i) {
      idx = (i + figs.length) % figs.length;
      var f = figs[idx];
      lbImg.src = f.getAttribute('data-lb');
      lbImg.alt = f.querySelector('img').alt;
      lb.classList.add('on');
      lb.setAttribute('aria-hidden', 'false');
      body.style.overflow = 'hidden';
    }
    function hide() {
      lb.classList.remove('on');
      lb.setAttribute('aria-hidden', 'true');
      body.style.overflow = '';
      setTimeout(function () { lbImg.src = ''; }, 400);
    }
    gal.addEventListener('click', function (e) {
      var f = e.target.closest('figure[data-lb]');
      if (f) show(figs.indexOf(f));
    });
    lb.querySelector('.close').addEventListener('click', hide);
    lb.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    lb.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lbImg) hide(); });
    doc.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') hide();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ================= Cart =================
     A real cart, but checkout is a phone call — she does not want online
     payment. Items live in localStorage; nothing is ever transmitted. */
  var CART_KEY = 'mp-cart';

  function cartRead() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
    catch (e) { return []; }
  }
  function cartWrite(items) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(items)); } catch (e) {}
    cartPaint();
  }
  function money(items) {
    var t = items.reduce(function (n, i) { return n + (parseFloat(i.price) || 0); }, 0);
    return t ? '$' + t.toLocaleString('en-US') : 'Free';
  }

  var panel  = doc.querySelector('[data-cart-panel]');
  var scrim  = doc.querySelector('[data-cart-scrim]');
  var bodyEl = doc.querySelector('[data-cart-body]');
  var footEl = doc.querySelector('[data-cart-foot]');
  var toastEl = doc.querySelector('[data-toast]');
  var toastT;

  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('on');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2600);
  }

  function cartPaint() {
    var items = cartRead();
    doc.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.textContent = items.length;
      el.hidden = items.length === 0;
    });
    doc.querySelectorAll('[data-cart-count-m]').forEach(function (el) {
      el.textContent = items.length ? 'Cart (' + items.length + ')' : 'Cart';
    });
    doc.querySelectorAll('[data-add]').forEach(function (b) {
      var on = items.some(function (i) { return i.id === b.getAttribute('data-id'); });
      b.classList.toggle('added', on);
      var lbl = b.querySelector('.add-lbl');
      if (lbl) lbl.textContent = on ? 'In your cart' : 'Add to cart';
    });
    if (!bodyEl) return;
    if (!items.length) {
      bodyEl.innerHTML =
        '<div class="cart-empty">' +
        '<p>Your cart is empty.</p>' +
        '<p class="small" style="margin-top:.7rem">Add any reading you want to ask about, then ' +
        'call Mother Powers to check out. She will tell you what you actually need.</p>' +
        '</div>';
      if (footEl) footEl.hidden = true;
      return;
    }
    bodyEl.innerHTML = items.map(function (i) {
      return '<div class="cart-line">' +
        (i.img ? '<img src="' + i.img + '" alt="">' : '') +
        '<div><div class="n">' + i.title + '</div>' +
        '<div class="p">' + (parseFloat(i.price) ? '$' + i.price : 'Free of charge') + '</div></div>' +
        '<button class="rm" type="button" aria-label="Remove" data-rm="' + i.id + '">&times;</button>' +
        '</div>';
    }).join('');
    if (footEl) {
      footEl.hidden = false;
      var tot = footEl.querySelector('[data-cart-total]');
      if (tot) tot.textContent = money(items);
    }
  }

  function cartOpen() {
    if (!panel) return;
    scrim.hidden = false;
    requestAnimationFrame(function () { scrim.classList.add('on'); panel.classList.add('on'); });
    panel.setAttribute('aria-hidden', 'false');
    body.style.overflow = 'hidden';
  }
  function cartClose() {
    if (!panel) return;
    scrim.classList.remove('on');
    panel.classList.remove('on');
    panel.setAttribute('aria-hidden', 'true');
    body.style.overflow = '';
    setTimeout(function () { scrim.hidden = true; }, 420);
  }

  doc.addEventListener('click', function (e) {
    var add = e.target.closest('[data-add]');
    if (add) {
      e.preventDefault();
      var id = add.getAttribute('data-id');
      var items = cartRead();
      if (items.some(function (i) { return i.id === id; })) {
        cartWrite(items.filter(function (i) { return i.id !== id; }));
        toast('Removed from your cart.');
      } else {
        items.push({
          id: id,
          title: add.getAttribute('data-title'),
          price: add.getAttribute('data-price'),
          img: add.getAttribute('data-img')
        });
        cartWrite(items);
        toast('Added to cart. Call Mother to check out.');
        doc.querySelectorAll('.cart-btn').forEach(function (b) {
          b.classList.remove('bump');
          void b.offsetWidth;
          b.classList.add('bump');
        });
      }
      return;
    }
    if (e.target.closest('[data-cart-open]')) { e.preventDefault(); cartOpen(); return; }
    if (e.target.closest('[data-cart-close]') || e.target.closest('[data-cart-scrim]')) { cartClose(); return; }
    var rm = e.target.closest('[data-rm]');
    if (rm) {
      var rid = rm.getAttribute('data-rm');
      cartWrite(cartRead().filter(function (i) { return i.id !== rid; }));
      return;
    }
    if (e.target.closest('[data-cart-clear]')) { cartWrite([]); toast('Cart emptied.'); }
  });
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel && panel.classList.contains('on')) cartClose();
  });
  cartPaint();

  /* ================= Carousels ================= */
  doc.querySelectorAll('[data-carousel]').forEach(function (car) {
    var track = car.querySelector('.carousel-track');
    var slides = Array.prototype.slice.call(track.children);
    var prev = car.querySelector('[data-car-prev]');
    var next = car.querySelector('[data-car-next]');
    var dotWrap = car.querySelector('.car-dots');
    if (!slides.length) return;

    if (dotWrap) {
      dotWrap.innerHTML = slides.map(function (_, i) {
        return '<button type="button" aria-label="Go to slide ' + (i + 1) + '"></button>';
      }).join('');
    }
    var dots = dotWrap ? Array.prototype.slice.call(dotWrap.children) : [];

    function nearest() {
      var c = track.scrollLeft + track.clientWidth / 2;
      var best = 0, bd = Infinity;
      slides.forEach(function (s, i) {
        var d = Math.abs(s.offsetLeft + s.offsetWidth / 2 - c);
        if (d < bd) { bd = d; best = i; }
      });
      return best;
    }
    function sync() {
      var i = nearest();
      dots.forEach(function (d, j) { d.classList.toggle('on', j === i); });
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    }
    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      var s = slides[i];
      track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.offsetWidth) / 2, behavior: 'smooth' });
    }
    if (prev) prev.addEventListener('click', function () { go(nearest() - 1); });
    if (next) next.addEventListener('click', function () { go(nearest() + 1); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });

    var raf;
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(sync);
    }, { passive: true });
    window.addEventListener('resize', sync, { passive: true });

    track.setAttribute('tabindex', '0');
    track.setAttribute('role', 'region');
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(nearest() + 1); }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); go(nearest() - 1); }
    });
    sync();
  });

  /* ---- Footer year ---- */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
