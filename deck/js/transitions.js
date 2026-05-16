/**
 * transitions.js — Comportamento custom del deck cinematic
 * 
 * Tre responsabilità:
 *  1. Audio mixer: gestisce ambient loop con crossfade tra scene
 *  2. GSAP animations: anima gli elementi delle slide realistic
 *  3. Speciale: transizione storia (12) → realistic (13) con crossfade arancione
 */

// ============================================================================
// 1. Audio Mixer — un solo ambient attivo alla volta, crossfade tra scene
// ============================================================================

class AudioMixer {
  constructor() {
    this.currentAmbient = null;
    this.fadeMs = 800;
    this.ambientVolume = 0.30;   // -12 dB circa
    this.sfxVolume = 0.85;       //  -1 dB
  }

  activate(audioEl) {
    if (!audioEl) return;
    if (this.currentAmbient === audioEl) return;
    
    if (this.currentAmbient) {
      this.fadeOut(this.currentAmbient);
    }
    
    this.currentAmbient = audioEl;
    audioEl.volume = 0;
    audioEl.loop = audioEl.dataset.ambient === 'true' || audioEl.loop;
    audioEl.play().catch(err => {
      console.warn('Autoplay audio bloccato:', err);
    });
    this.fadeIn(audioEl, this.ambientVolume);
  }

  fadeIn(el, targetVol) {
    const startTime = performance.now();
    const step = () => {
      const elapsed = performance.now() - startTime;
      const progress = Math.min(elapsed / this.fadeMs, 1);
      el.volume = targetVol * progress;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  fadeOut(el) {
    const startVol = el.volume;
    const startTime = performance.now();
    const step = () => {
      const elapsed = performance.now() - startTime;
      const progress = Math.min(elapsed / this.fadeMs, 1);
      el.volume = startVol * (1 - progress);
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.pause();
        el.currentTime = 0;
      }
    };
    requestAnimationFrame(step);
  }

  stopAll() {
    document.querySelectorAll('audio').forEach(a => {
      a.pause();
      a.currentTime = 0;
    });
    this.currentAmbient = null;
  }
}

const audioMixer = new AudioMixer();

// ============================================================================
// 2. GSAP Animations per slide realistic
// ============================================================================

function animateRealisticSlide(slideEl) {
  if (typeof gsap === 'undefined') return;
  
  const bigNumber = slideEl.querySelector('.big-number');
  const illustration = slideEl.querySelector('.illustration');
  const caption = slideEl.querySelector('.caption');
  
  // Reset stati
  gsap.set([bigNumber, illustration, caption], { opacity: 0, y: 30 });
  
  // Sequenza
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  tl.to(bigNumber, { opacity: 1, y: 0, duration: 0.8 })
    .to(illustration, { opacity: 1, y: 0, duration: 0.8 }, '-=0.4')
    .to(caption, { opacity: 1, y: 0, duration: 0.6 }, '-=0.3');
}

// ============================================================================
// 3. Speciale: transizione storia (12) → realistic (13)
// ============================================================================

function applyOrangeBridge(prevSlide, currSlide) {
  if (typeof gsap === 'undefined') return;
  
  // Overlay arancione fugace tra le due slide
  const overlay = document.createElement('div');
  overlay.style.cssText = `
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: radial-gradient(circle at 50% 50%, 
      rgba(255, 107, 26, 0.5) 0%, 
      rgba(255, 107, 26, 0) 70%);
    pointer-events: none;
    z-index: 9999;
    opacity: 0;
  `;
  document.body.appendChild(overlay);
  
  gsap.timeline()
    .to(overlay, { opacity: 1, duration: 0.8, ease: 'power2.in' })
    .to(overlay, { opacity: 0, duration: 1.2, ease: 'power2.out' })
    .call(() => overlay.remove());
}

// ============================================================================
// Hook reveal.js events
// ============================================================================

Reveal.on('slidechanged', event => {
  const prev = event.previousSlide;
  const curr = event.currentSlide;
  
  // Stop all videos in non-active slides (per evitare audio sovrapposto)
  document.querySelectorAll('video').forEach(v => {
    if (!curr.contains(v)) {
      v.pause();
      v.currentTime = 0;
    }
  });
  
  // Audio ambient
  const ambient = curr.querySelector('audio[data-ambient]') 
                  || curr.querySelector('audio');
  if (ambient) {
    audioMixer.activate(ambient);
  } else {
    if (audioMixer.currentAmbient) {
      audioMixer.fadeOut(audioMixer.currentAmbient);
      audioMixer.currentAmbient = null;
    }
  }
  
  // Animazioni realistic slide
  if (curr.classList.contains('realistic-slide')) {
    animateRealisticSlide(curr);
  }
  
  // Transizione speciale storia → realistic
  if (prev?.dataset.sceneId === '12' && curr?.dataset.slideId === '13') {
    applyOrangeBridge(prev, curr);
  }
  
  // Autoplay video
  const video = curr.querySelector('video[data-autoplay], video');
  if (video) {
    video.currentTime = 0;
    video.play().catch(err => {
      console.warn('Autoplay video bloccato. Click sulla slide per partire.', err);
    });
  }
});

// Sblocca autoplay con interazione iniziale (browser policy)
document.addEventListener('click', () => {
  const ctx = window.AudioContext || window.webkitAudioContext;
  if (ctx && !window._audioContextResumed) {
    new ctx().resume();
    window._audioContextResumed = true;
  }
}, { once: true });

// ============================================================================
// Keyboard shortcuts custom (oltre a quelli di reveal.js)
// ============================================================================

document.addEventListener('keydown', e => {
  // 'M' per mute/unmute globale audio
  if (e.key === 'm' || e.key === 'M') {
    const allAudio = document.querySelectorAll('audio, video');
    const allMuted = Array.from(allAudio).every(a => a.muted);
    allAudio.forEach(a => a.muted = !allMuted);
    console.log(allMuted ? 'Audio unmuted' : 'Audio muted');
  }
  
  // 'B' per blackout (slide nera istantanea — utile in emergenza)
  if (e.key === 'b' || e.key === 'B') {
    document.body.style.transition = 'background 200ms';
    document.body.style.background = '#000';
    document.querySelector('.reveal').style.opacity = 
      document.querySelector('.reveal').style.opacity === '0' ? '1' : '0';
  }
});

console.log('🎬 Deck cinematic caricato. Premi F per fullscreen, S per speaker view, M per mute, B per blackout.');
