/* U.S. Strategic Resources — restrained interaction layer.
   The one orchestrated moment is the rail line drawing in on the map
   (CSS keyframes, gated behind a per-instance .is-visible trigger below).
   Everything else here — a scroll reveal, the closing band's subtle
   parallax, or the mobile nav disclosure — is a small, restrained
   micro-interaction in the same spirit, not a second showcase moment. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobile nav ---- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* ---- signature map draw-in ----
     Lives on About → Jurisdiction only (removed from the Home hero — see
     index.html). Generic .map selector rather than a page-specific hook so
     it plays no matter which page(s) the component ends up mounted on;
     querySelectorAll simply finds nothing to observe elsewhere. */
  var maps = document.querySelectorAll('.map');
  if (maps.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      maps.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var mapIo = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            mapIo.unobserve(entry.target);
          }
        });
      }, { threshold: 0.35 });
      maps.forEach(function (el) { mapIo.observe(el); });
    }
  }

  /* ---- band parallax ----
     A subtle scroll-driven drift on the closing photo band's image, so it
     reads as a quiet transition rather than a second static content block.
     Skipped entirely under reduced motion. Bounded to stay within the
     overscan the base CSS scale(1.08) gives it, so the shift never
     uncovers an edge — .duo's own overflow: hidden clips it regardless. */
  var parallaxImgs = document.querySelectorAll('.band--parallax > picture > img, .band--parallax > img');
  if (parallaxImgs.length && !reduced) {
    var maxShift = 32;
    var ticking = false;
    var updateParallax = function () {
      parallaxImgs.forEach(function (img) {
        var band = img.closest('.band');
        var rect = band.getBoundingClientRect();
        var vh = window.innerHeight || document.documentElement.clientHeight;
        var center = rect.top + rect.height / 2 - vh / 2;
        var progress = center / (vh / 2 + rect.height / 2);
        progress = Math.max(-1, Math.min(1, progress));
        img.style.transform = 'scale(1.2) translateY(' + (progress * maxShift).toFixed(1) + 'px)';
      });
      ticking = false;
    };
    var onScroll = function () {
      if (!ticking) {
        window.requestAnimationFrame(updateParallax);
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    updateParallax();
  }

  /* ---- scroll reveals ---- */
  var targets = document.querySelectorAll('.reveal, .reveal-group');
  if (!targets.length) return;

  if (reduced || !('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

  targets.forEach(function (el) { io.observe(el); });
})();
