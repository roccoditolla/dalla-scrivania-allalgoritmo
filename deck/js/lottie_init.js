/**
 * lottie_init.js — Auto-load Lottie animations when slide becomes active.
 *
 * Markup: <div class="full-bleed-lottie" data-lottie="assets/lottie/scene_01.json"></div>
 *       <div class="illustration lottie-illustration" data-lottie="assets/lottie/slide_19.json"></div>
 *
 * Comportamento:
 * - Lazy load: l'animazione si carica solo quando la slide diventa attiva
 *   (così non si scaricano tutti i JSON al boot del deck)
 * - Una volta caricata, resta in memoria e fa loop
 * - Pausa quando la slide non è attiva (risparmia CPU)
 */
(function () {
  'use strict';

  if (typeof lottie === 'undefined') {
    console.warn('[lottie_init] lottie-web non caricato (CDN). Skip.');
    return;
  }

  const loaded = new WeakMap();

  function loadForSlide(slideEl) {
    if (!slideEl) return;
    const containers = slideEl.querySelectorAll('[data-lottie]');
    containers.forEach((c) => {
      let anim = loaded.get(c);
      if (anim) {
        try { anim.play(); } catch (e) { /* no-op */ }
        return;
      }
      const path = c.dataset.lottie;
      if (!path) return;
      try {
        anim = lottie.loadAnimation({
          container: c,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          path: path,
          rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice',
            progressiveLoad: true,
          },
        });
        loaded.set(c, anim);
      } catch (e) {
        console.warn('[lottie_init] load failed', path, e);
      }
    });
  }

  function pauseForSlide(slideEl) {
    if (!slideEl) return;
    slideEl.querySelectorAll('[data-lottie]').forEach((c) => {
      const anim = loaded.get(c);
      if (anim) { try { anim.pause(); } catch (e) {} }
    });
  }

  if (typeof Reveal !== 'undefined') {
    Reveal.on('slidechanged', (event) => {
      pauseForSlide(event.previousSlide);
      loadForSlide(event.currentSlide);
    });
    Reveal.on('ready', (event) => loadForSlide(event.currentSlide));
  } else {
    document.addEventListener('DOMContentLoaded', () => {
      loadForSlide(document.querySelector('.reveal .slides section'));
    });
  }
})();
