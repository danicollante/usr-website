(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Count-up on .stats__figure -------------------------------------------
     The HTML value is always the true, final figure. This only animates the
     approach to it — parsing a leading non-digit prefix ($, ~), the number
     itself, and a trailing suffix (%, B, M, +), so it works unmodified for
     "90%", "$12B", "$30B+", "7", etc.                                       */
  function parseFigure(text) {
    var match = text.match(/^(\D*)([\d,]+(?:\.\d+)?)(.*)$/);
    if (!match) return null;
    var numStr = match[2].replace(/,/g, '');
    var value = parseFloat(numStr);
    if (isNaN(value)) return null;
    var decimals = numStr.indexOf('.') > -1 ? numStr.split('.')[1].length : 0;
    return { prefix: match[1], suffix: match[3], value: value, decimals: decimals, original: text };
  }

  function animateCount(el) {
    var meta = parseFigure(el.textContent.trim());
    if (!meta || prefersReducedMotion) return;

    var duration = 1100;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = meta.value * eased;
      var str = meta.decimals > 0 ? current.toFixed(meta.decimals) : Math.round(current).toString();
      el.textContent = meta.prefix + str + meta.suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = meta.original;
      }
    }
    requestAnimationFrame(step);
  }

  /* --- Scroll reveal ----------------------------------------------------- */
  function initReveal() {
    var targets = document.querySelectorAll('.reveal, .reveal-group');
    if (!targets.length) return;

    if (!('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('reveal--visible'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('reveal--visible');
        if (entry.target.classList.contains('reveal-group')) {
          entry.target.querySelectorAll('.stats__figure').forEach(animateCount);
        }
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.2, rootMargin: '0px 0px -40px 0px' });

    targets.forEach(function (el) { observer.observe(el); });
  }

  /* --- Hero parallax -------------------------------------------------------
     Translates the terrain band's inner layer a few px either side of centre
     as it crosses the viewport — subtle, never more than `range`.           */
  function initParallax() {
    if (prefersReducedMotion) return;
    var band = document.querySelector('[data-parallax]');
    if (!band) return;
    var inner = band.querySelector('.placeholder--band__inner');
    if (!inner) return;

    var range = 22;
    var ticking = false;

    function update() {
      var rect = band.getBoundingClientRect();
      var viewportH = window.innerHeight || document.documentElement.clientHeight;
      var total = viewportH + rect.height;
      var progress = total > 0 ? (viewportH - rect.top) / total : 0.5;
      progress = Math.max(0, Math.min(1, progress));
      var offset = (progress - 0.5) * range * 2;
      inner.style.transform = 'translateY(' + offset.toFixed(1) + 'px)';
      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  function init() {
    initReveal();
    initParallax();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
