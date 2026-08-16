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

  /* ---- Footer year ---- */
  doc.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
