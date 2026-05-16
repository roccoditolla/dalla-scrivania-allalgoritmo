/**
 * synth_audio.js — Generatore audio sintetico via Web Audio API
 *
 * Sostituisce/affianca i file MP3 di Pixabay/Freesound quando non disponibili.
 * Tutto generato programmaticamente nel browser, zero asset esterni, zero costi.
 *
 * Espone window.SynthAudio con metodi:
 *   - playAmbient(type)   — avvia loop continuo (crossfade con quello precedente)
 *   - stopAmbient()       — fade-out del loop corrente
 *   - playSFX(type)       — riproduce un effetto one-shot
 *   - dbToGain(db)        — utility dB → linear gain
 *
 * Tipi ambient: 'ocean_dawn', 'deck_work', 'thunderstorm', 'calm_after',
 *               'island_drone', 'rowing', 'sand_shift', 'warm_pad',
 *               'sails_wind', 'transition_pad', 'realistic_intro', 'end_pulse'
 * Tipi SFX:     'compass_shimmer', 'thunder_crack', 'chime'
 */

(function () {
  'use strict';

  const SynthAudio = {
    ctx: null,
    masterGain: null,
    currentAmbient: null, // { stop: fn, label: str }
    fadeMs: 1000,

    /**
     * Inizializza l'AudioContext (deve avvenire dopo user gesture).
     */
    init() {
      if (this.ctx) return this.ctx;
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) {
        console.warn('Web Audio API non disponibile');
        return null;
      }
      this.ctx = new AC();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.value = 1.0;
      this.masterGain.connect(this.ctx.destination);
      return this.ctx;
    },

    dbToGain(db) {
      return Math.pow(10, db / 20);
    },

    /**
     * Crea un nodo reverb semplice via convolver+impulse generato in code.
     */
    createReverb(durationS = 2.5, decay = 2.0) {
      const ctx = this.ctx;
      const sr = ctx.sampleRate;
      const length = sr * durationS;
      const impulse = ctx.createBuffer(2, length, sr);
      for (let ch = 0; ch < 2; ch++) {
        const data = impulse.getChannelData(ch);
        for (let i = 0; i < length; i++) {
          data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, decay);
        }
      }
      const conv = ctx.createConvolver();
      conv.buffer = impulse;
      return conv;
    },

    /**
     * Crossfade-aware: ferma l'ambient corrente e avvia il nuovo.
     */
    playAmbient(type, targetDb = -14) {
      if (!this.ctx) this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') this.ctx.resume();

      const targetGain = this.dbToGain(targetDb);

      if (this.currentAmbient && this.currentAmbient.label === type) return;

      // Fade-out del corrente
      if (this.currentAmbient) {
        this.currentAmbient.stop(this.fadeMs);
      }

      const builder = AMBIENT_BUILDERS[type];
      if (!builder) {
        console.warn('Ambient type sconosciuto:', type);
        this.currentAmbient = null;
        return;
      }

      this.currentAmbient = builder.call(this, targetGain);
      this.currentAmbient.label = type;
    },

    stopAmbient() {
      if (this.currentAmbient) {
        this.currentAmbient.stop(this.fadeMs);
        this.currentAmbient = null;
      }
    },

    playSFX(type, db = -6) {
      if (!this.ctx) this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') this.ctx.resume();

      const builder = SFX_BUILDERS[type];
      if (!builder) {
        console.warn('SFX type sconosciuto:', type);
        return;
      }
      const gain = this.dbToGain(db);
      builder.call(this, gain);
    },
  };

  // ============================================================================
  // AMBIENT BUILDERS — ognuno ritorna { stop(fadeMs) }
  // ============================================================================

  /**
   * Crea un noise buffer (5s, mono) usato per onde/vento/pioggia.
   */
  function noiseBuffer(durationS = 5) {
    const ctx = SynthAudio.ctx;
    const buf = ctx.createBuffer(1, ctx.sampleRate * durationS, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    return buf;
  }

  /**
   * Helper: oscillator con detune random per "instabilità" organica.
   */
  function makeOsc(freq, type = 'sine', detune = 0) {
    const o = SynthAudio.ctx.createOscillator();
    o.type = type;
    o.frequency.value = freq;
    o.detune.value = detune;
    return o;
  }

  function makeGain(value = 1) {
    const g = SynthAudio.ctx.createGain();
    g.gain.value = value;
    return g;
  }

  function makeFilter(freq = 1000, type = 'lowpass', q = 1) {
    const f = SynthAudio.ctx.createBiquadFilter();
    f.type = type;
    f.frequency.value = freq;
    f.Q.value = q;
    return f;
  }

  const AMBIENT_BUILDERS = {
    /**
     * ocean_dawn: noise low-passato a 600Hz + LFO lento sul cutoff per "respiro" onda
     */
    ocean_dawn(targetGain) {
      const ctx = SynthAudio.ctx;
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(6);
      src.loop = true;
      const filt = makeFilter(500, 'lowpass', 0.6);
      // LFO sul cutoff: simula onde
      const lfo = makeOsc(0.15, 'sine');
      const lfoGain = makeGain(250);
      lfo.connect(lfoGain).connect(filt.frequency);
      const out = makeGain(0);
      src.connect(filt).connect(out).connect(SynthAudio.masterGain);
      src.start();
      lfo.start();
      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + SynthAudio.fadeMs / 1000);

      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => { src.stop(); lfo.stop(); }, fadeMs + 100);
        }
      };
    },

    /**
     * calm_after: come ocean_dawn ma più lento e più alto cutoff
     */
    calm_after(targetGain) {
      return AMBIENT_BUILDERS.ocean_dawn.call(this, targetGain);
    },

    /**
     * deck_work: noise + tiny resonant peaks (legno che scricchiola)
     */
    deck_work(targetGain) {
      const ctx = SynthAudio.ctx;
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(6);
      src.loop = true;
      const filt = makeFilter(800, 'bandpass', 4);
      const out = makeGain(0);
      src.connect(filt).connect(out).connect(SynthAudio.masterGain);
      src.start();
      out.gain.linearRampToValueAtTime(targetGain * 0.8, ctx.currentTime + 1);

      // Sporadici "creaks" (random pitched bursts)
      const interval = setInterval(() => {
        if (Math.random() < 0.4) {
          const o = makeOsc(180 + Math.random() * 120, 'triangle');
          const g = makeGain(0);
          o.connect(g).connect(SynthAudio.masterGain);
          o.start();
          const t = ctx.currentTime;
          g.gain.linearRampToValueAtTime(targetGain * 0.4, t + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, t + 0.3);
          o.stop(t + 0.4);
        }
      }, 800);

      return {
        stop(fadeMs) {
          clearInterval(interval);
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => src.stop(), fadeMs + 100);
        }
      };
    },

    /**
     * thunderstorm: heavy noise rain + random thunder cracks
     */
    thunderstorm(targetGain) {
      const ctx = SynthAudio.ctx;
      const rain = ctx.createBufferSource();
      rain.buffer = noiseBuffer(8);
      rain.loop = true;
      const rainFilt = makeFilter(2200, 'lowpass', 0.5);
      const rainOut = makeGain(0);
      rain.connect(rainFilt).connect(rainOut).connect(SynthAudio.masterGain);
      rain.start();
      rainOut.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 1);

      // Thunder cracks ogni 3-7 secondi
      const thunderInterval = setInterval(() => {
        const t = ctx.currentTime;
        const lf = makeOsc(40 + Math.random() * 30, 'sine');
        const lfg = makeGain(0);
        const lfFilt = makeFilter(150, 'lowpass', 2);
        lf.connect(lfFilt).connect(lfg).connect(SynthAudio.masterGain);
        lf.start(t);
        lfg.gain.linearRampToValueAtTime(targetGain * 2.5, t + 0.05);
        lfg.gain.exponentialRampToValueAtTime(0.001, t + 2.5);
        lf.stop(t + 2.6);
      }, 4000 + Math.random() * 3000);

      return {
        stop(fadeMs) {
          clearInterval(thunderInterval);
          rainOut.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => rain.stop(), fadeMs + 100);
        }
      };
    },

    /**
     * island_drone: low sub-bass 55Hz + sine 82Hz (perfect 5th) + slow LFO
     */
    island_drone(targetGain) {
      const ctx = SynthAudio.ctx;
      const o1 = makeOsc(55, 'sine');
      const o2 = makeOsc(82.4, 'sine');
      const o3 = makeOsc(110, 'sine');
      const o3Gain = makeGain(0.4);
      const out = makeGain(0);
      o1.connect(out);
      o2.connect(out);
      o3.connect(o3Gain).connect(out);
      out.connect(SynthAudio.masterGain);
      o1.start(); o2.start(); o3.start();

      // Distant ethereal chimes (raro)
      const chimeInterval = setInterval(() => {
        if (Math.random() < 0.3) {
          const cFreq = [880, 1109, 1318, 1760][Math.floor(Math.random() * 4)];
          const c = makeOsc(cFreq, 'sine');
          const cg = makeGain(0);
          c.connect(cg).connect(SynthAudio.masterGain);
          c.start();
          const t = ctx.currentTime;
          cg.gain.linearRampToValueAtTime(targetGain * 0.25, t + 0.05);
          cg.gain.exponentialRampToValueAtTime(0.0001, t + 3.5);
          c.stop(t + 3.6);
        }
      }, 2500);

      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 1.5);

      return {
        stop(fadeMs) {
          clearInterval(chimeInterval);
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => { o1.stop(); o2.stop(); o3.stop(); }, fadeMs + 100);
        }
      };
    },

    /**
     * rowing: rhythmic noise pulses + low splash
     */
    rowing(targetGain) {
      const ctx = SynthAudio.ctx;
      const out = makeGain(0);
      out.connect(SynthAudio.masterGain);
      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 1);

      const interval = setInterval(() => {
        const t = ctx.currentTime;
        const splash = ctx.createBufferSource();
        splash.buffer = noiseBuffer(0.5);
        const sf = makeFilter(900, 'bandpass', 1.2);
        const sg = makeGain(0);
        splash.connect(sf).connect(sg).connect(out);
        splash.start(t);
        sg.gain.linearRampToValueAtTime(targetGain * 1.6, t + 0.03);
        sg.gain.exponentialRampToValueAtTime(0.0001, t + 0.4);
        splash.stop(t + 0.5);
      }, 1400);

      return {
        stop(fadeMs) {
          clearInterval(interval);
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
        }
      };
    },

    /**
     * sand_shift: high-freq granular hiss, very quiet
     */
    sand_shift(targetGain) {
      const ctx = SynthAudio.ctx;
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(4);
      src.loop = true;
      const filt = makeFilter(8000, 'highpass', 0.5);
      const out = makeGain(0);
      src.connect(filt).connect(out).connect(SynthAudio.masterGain);
      src.start();
      out.gain.linearRampToValueAtTime(targetGain * 0.7, ctx.currentTime + 0.8);

      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => src.stop(), fadeMs + 100);
        }
      };
    },

    /**
     * warm_pad: chord (root, 5th, octave) with slow LFO mod, used for revelation
     */
    warm_pad(targetGain) {
      const ctx = SynthAudio.ctx;
      const root = 130.81; // C3
      const o1 = makeOsc(root, 'sine');
      const o2 = makeOsc(root * 1.5, 'sine', -8);   // 5th
      const o3 = makeOsc(root * 2, 'sine', +6);     // 8va
      const o4 = makeOsc(root * 2.5, 'triangle', -12); // softer top
      const o4g = makeGain(0.18);
      const out = makeGain(0);
      o1.connect(out); o2.connect(out); o3.connect(out);
      o4.connect(o4g).connect(out);
      out.connect(SynthAudio.masterGain);
      o1.start(); o2.start(); o3.start(); o4.start();

      // Slow LFO on master gain for breathing
      const lfo = makeOsc(0.08, 'sine');
      const lfoG = makeGain(targetGain * 0.2);
      lfo.connect(lfoG).connect(out.gain);
      lfo.start();

      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 2);

      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => { o1.stop(); o2.stop(); o3.stop(); o4.stop(); lfo.stop(); }, fadeMs + 100);
        }
      };
    },

    /**
     * sails_wind: white noise filtered + high-freq sweep ogni 6-9 secondi
     */
    sails_wind(targetGain) {
      const ctx = SynthAudio.ctx;
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(6);
      src.loop = true;
      const filt = makeFilter(1400, 'lowpass', 0.8);
      const out = makeGain(0);
      src.connect(filt).connect(out).connect(SynthAudio.masterGain);
      src.start();
      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 1);
      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => src.stop(), fadeMs + 100);
        }
      };
    },

    /**
     * transition_pad: smooth modern ambient pad
     */
    transition_pad(targetGain) {
      return AMBIENT_BUILDERS.warm_pad.call(this, targetGain * 0.7);
    },

    /**
     * realistic_intro: very subtle bass + airy top
     */
    realistic_intro(targetGain) {
      const ctx = SynthAudio.ctx;
      const o1 = makeOsc(65.4, 'sine');
      const o2 = makeOsc(196, 'sine', -4);
      const out = makeGain(0);
      o1.connect(out); o2.connect(out);
      out.connect(SynthAudio.masterGain);
      o1.start(); o2.start();
      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 2);
      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => { o1.stop(); o2.stop(); }, fadeMs + 100);
        }
      };
    },

    /**
     * end_pulse: low warm pulse (heartbeat-like) per chiusura
     */
    end_pulse(targetGain) {
      const ctx = SynthAudio.ctx;
      const carrier = makeOsc(65.4, 'sine');
      const out = makeGain(0);
      carrier.connect(out).connect(SynthAudio.masterGain);
      carrier.start();

      // Pulse via LFO sul gain
      const pulse = makeOsc(0.85, 'sine');
      const pulseG = makeGain(targetGain * 0.5);
      pulse.connect(pulseG).connect(out.gain);
      pulse.start();

      out.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 1.5);
      return {
        stop(fadeMs) {
          out.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeMs / 1000);
          setTimeout(() => { carrier.stop(); pulse.stop(); }, fadeMs + 100);
        }
      };
    },
  };

  // ============================================================================
  // SFX BUILDERS — one-shot
  // ============================================================================

  const SFX_BUILDERS = {
    /**
     * compass_shimmer: bell-like crystalline tones + reverb. Il momento WOW 3.
     */
    compass_shimmer(gain) {
      const ctx = SynthAudio.ctx;
      const reverb = SynthAudio.createReverb(3.5, 2.2);
      const wet = makeGain(0.7);
      const dry = makeGain(0.4);
      const out = makeGain(gain);
      reverb.connect(wet).connect(out);
      out.connect(SynthAudio.masterGain);

      // Cascading bell tones
      const notes = [880, 1108.7, 1318.5, 1760, 2217, 2637];
      notes.forEach((freq, i) => {
        const o = makeOsc(freq, 'sine', (Math.random() * 6 - 3));
        const o2 = makeOsc(freq * 2, 'sine', -8);
        const g = makeGain(0);
        const g2 = makeGain(0.18);
        o.connect(g); o2.connect(g2).connect(g);
        g.connect(reverb);
        g.connect(dry).connect(out);
        const t = ctx.currentTime + i * 0.18;
        o.start(t); o2.start(t);
        g.gain.linearRampToValueAtTime(0.55, t + 0.04);
        g.gain.exponentialRampToValueAtTime(0.0001, t + 2.5);
        o.stop(t + 2.6); o2.stop(t + 2.6);
      });

      // Final warm low resonance (the compass "wakes up")
      const t = ctx.currentTime + 1.0;
      const drone = makeOsc(110, 'sine');
      const drone2 = makeOsc(165, 'sine', -4);
      const dg = makeGain(0);
      drone.connect(dg); drone2.connect(dg);
      dg.connect(out);
      drone.start(t); drone2.start(t);
      dg.gain.linearRampToValueAtTime(0.35, t + 0.5);
      dg.gain.linearRampToValueAtTime(0.0, t + 4);
      drone.stop(t + 4.1); drone2.stop(t + 4.1);
    },

    /**
     * thunder_crack: low BOOM con decay
     */
    thunder_crack(gain) {
      const ctx = SynthAudio.ctx;
      const t = ctx.currentTime;
      const o = makeOsc(38, 'sine');
      const g = makeGain(0);
      const f = makeFilter(180, 'lowpass', 1.8);
      const out = makeGain(gain);
      o.connect(f).connect(g).connect(out).connect(SynthAudio.masterGain);
      o.start(t);
      g.gain.linearRampToValueAtTime(3, t + 0.05);
      g.gain.exponentialRampToValueAtTime(0.001, t + 3.5);
      o.stop(t + 3.6);
    },

    /**
     * chime: single bell stroke
     */
    chime(gain) {
      const ctx = SynthAudio.ctx;
      const t = ctx.currentTime;
      const o = makeOsc(1318.5, 'sine');
      const o2 = makeOsc(2637, 'sine', -4);
      const g = makeGain(0);
      const g2 = makeGain(0.25);
      const out = makeGain(gain);
      o.connect(g); o2.connect(g2).connect(g);
      g.connect(out).connect(SynthAudio.masterGain);
      o.start(t); o2.start(t);
      g.gain.linearRampToValueAtTime(1, t + 0.03);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 2.5);
      o.stop(t + 2.6); o2.stop(t + 2.6);
    },
  };

  // ============================================================================
  // Mappa scene → ambient (usata da transitions.js)
  // ============================================================================

  SynthAudio.AMBIENT_FOR_SCENE = {
    '01': { type: 'ocean_dawn', db: -14 },
    '02A': { type: 'deck_work', db: -12 },
    '02B': { type: 'deck_work', db: -12 },
    '03A': { type: 'thunderstorm', db: -8 },
    '03B': { type: 'thunderstorm', db: -8 },
    '04':  { type: 'calm_after', db: -14 },
    '05':  { type: 'island_drone', db: -10 },
    '06':  { type: 'rowing', db: -12 },
    '07':  { type: 'sand_shift', db: -16 },
    '08A': { type: null, db: 0, sfx: 'compass_shimmer', sfxDb: -6 }, // silenzio + shimmer
    '08B': { type: 'warm_pad', db: -12 },
    '09A': { type: 'warm_pad', db: -12 },
    '09B': { type: 'warm_pad', db: -12 },
    '10':  { type: 'rowing', db: -12 },
    '11A': { type: 'sails_wind', db: -10 },
    '11B': { type: 'sails_wind', db: -10 },
    '12':  { type: 'transition_pad', db: -14 },
  };

  SynthAudio.AMBIENT_FOR_SLIDE = {
    '13': { type: 'realistic_intro', db: -18 },
    '14': { type: 'realistic_intro', db: -18 },
    '15': { type: 'realistic_intro', db: -18 },
    '16': { type: 'realistic_intro', db: -18 },
    '17': { type: 'realistic_intro', db: -18 },
    '18': { type: 'realistic_intro', db: -18 },
    '19': { type: 'realistic_intro', db: -18 },
    '20': { type: 'realistic_intro', db: -18 },
    '21': { type: 'realistic_intro', db: -18 },
    '22': { type: 'realistic_intro', db: -18 },
    '23': { type: 'end_pulse', db: -10 },
  };

  window.SynthAudio = SynthAudio;
  console.log('🎵 SynthAudio caricato. Tipi ambient disponibili:', Object.keys(AMBIENT_BUILDERS).join(', '));
})();
