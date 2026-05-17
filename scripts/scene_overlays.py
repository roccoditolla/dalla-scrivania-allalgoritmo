"""Scene-specific animated SVG overlays for Pollinations photo backgrounds.

Each value is an inline SVG string to be injected on top of the photo
in deck/index.html via build_story_slide_html (scripts/assemble_deck.py).

Conventions
-----------
* viewBox 0 0 1920 1080, preserveAspectRatio xMidYMid slice, class photo-overlay-svg
* Width/height 100% via the existing CSS rule (.photo-overlay-svg)
* SMIL animations only (no JS, no external assets)
* Colors:
    - orange narrative: #FF6B1A   (only from scene 08A onwards)
    - white spray/lightning: #FFFFFF
    - water cyan/highlight: #A8D8F0
    - dust / sunset glow: #FFD580
* Every <defs id="..."> uses a "_NN" suffix matching the scene key,
  so multiple overlays on the same DOM never collide.
* Keep each overlay between 2 and 8 KB. No text. No raster.
"""

# ---------------------------------------------------------------------------
# Scene 01 — Mare all'alba, ciurma in distanza (NO ORANGE)
# Gulls flying L->R, dust gold in god rays, water ripple opacity pulse.
# ---------------------------------------------------------------------------
SCENE_01 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_01" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <filter id="glow_01"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="glowSoft_01"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_01)" pointer-events="none"/>
  <!-- horizon water shimmer ellipses -->
  <g opacity="0.55" filter="url(#glowSoft_01)">
    <ellipse cx="640" cy="720" rx="180" ry="3" fill="#A8D8F0">
      <animate attributeName="opacity" values="0.1;0.6;0.1" dur="4s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="1180" cy="740" rx="220" ry="3" fill="#A8D8F0">
      <animate attributeName="opacity" values="0.1;0.55;0.1" dur="5s" begin="0.7s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="760" rx="260" ry="2.5" fill="#A8D8F0">
      <animate attributeName="opacity" values="0.1;0.5;0.1" dur="6s" begin="1.4s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- gulls drifting L->R, slow path -->
  <g fill="none" stroke="#1a1a1a" stroke-width="2.4" stroke-linecap="round" opacity="0.75">
    <path d="M-40,260 q8,-7 16,0 q8,7 16,0">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="2000 -30" dur="22s" repeatCount="indefinite"/>
    </path>
    <path d="M-40,310 q6,-5 12,0 q6,5 12,0">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="2000 20" dur="26s" begin="3s" repeatCount="indefinite"/>
    </path>
    <path d="M-40,200 q7,-6 14,0 q7,6 14,0">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="2000 60" dur="30s" begin="6s" repeatCount="indefinite"/>
    </path>
    <path d="M-40,360 q5,-4 10,0 q5,4 10,0">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="2000 -10" dur="28s" begin="10s" repeatCount="indefinite"/>
    </path>
  </g>
  <!-- gold dust rising in god rays -->
  <g filter="url(#glow_01)">
    <circle r="2.6" cx="320" cy="900" fill="#FFD580"><animate attributeName="cy" values="900;180" dur="11s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="11s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="540" cy="950" fill="#FFD580"><animate attributeName="cy" values="950;220" dur="13s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="13s" begin="1s" repeatCount="indefinite"/></circle>
    <circle r="2.4" cx="780" cy="920" fill="#FFD580"><animate attributeName="cy" values="920;200" dur="12s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.65;0" dur="12s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="1040" cy="960" fill="#FFD580"><animate attributeName="cy" values="960;240" dur="14s" begin="0.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="14s" begin="0.5s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="1260" cy="940" fill="#FFD580"><animate attributeName="cy" values="940;210" dur="13s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="13s" begin="3s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="1480" cy="970" fill="#FFD580"><animate attributeName="cy" values="970;260" dur="15s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="15s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle r="2.3" cx="1700" cy="930" fill="#FFD580"><animate attributeName="cy" values="930;180" dur="12s" begin="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.65;0" dur="12s" begin="4s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="900" cy="980" fill="#FFD580"><animate attributeName="cy" values="980;230" dur="14s" begin="5.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="14s" begin="5.5s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 02A — Ciurma sul ponte (NO ORANGE)
# Flag flapping (path morph via animate d), gold dust rising, vignette.
# ---------------------------------------------------------------------------
SCENE_02A = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_02A" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <filter id="glow_02A"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_02A)" pointer-events="none"/>
  <!-- flag flapping top-right (mast area, approx) -->
  <g transform="translate(1480,90)" opacity="0.85">
    <rect x="-2" y="0" width="3" height="220" fill="#2a1f17"/>
    <path fill="#c9b48a" stroke="#3a2e22" stroke-width="1">
      <animate attributeName="d"
        values="M0,10 L120,18 L130,52 L120,86 L0,80 Z;
                M0,10 L120,8 L138,46 L120,92 L0,80 Z;
                M0,10 L120,22 L128,58 L122,80 L0,80 Z;
                M0,10 L120,18 L130,52 L120,86 L0,80 Z"
        keyTimes="0;0.34;0.68;1"
        keySplines="0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1"
        calcMode="spline"
        dur="3.4s" repeatCount="indefinite"/>
    </path>
  </g>
  <!-- gold dust rising in god rays -->
  <g filter="url(#glow_02A)">
    <circle r="2.6" cx="240" cy="930" fill="#FFD580"><animate attributeName="cy" values="930;160" dur="12s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="12s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="480" cy="960" fill="#FFD580"><animate attributeName="cy" values="960;200" dur="14s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="14s" begin="1s" repeatCount="indefinite"/></circle>
    <circle r="2.4" cx="720" cy="940" fill="#FFD580"><animate attributeName="cy" values="940;180" dur="13s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.65;0" dur="13s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="960" cy="970" fill="#FFD580"><animate attributeName="cy" values="970;220" dur="15s" begin="0.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="15s" begin="0.5s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="1200" cy="950" fill="#FFD580"><animate attributeName="cy" values="950;190" dur="13s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="13s" begin="3s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="1620" cy="980" fill="#FFD580"><animate attributeName="cy" values="980;240" dur="16s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="16s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle r="2.3" cx="1380" cy="930" fill="#FFD580"><animate attributeName="cy" values="930;170" dur="12s" begin="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.65;0" dur="12s" begin="4s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 03A — Tempesta WOW1 (NO ORANGE)
# Anticipation pre-flash + main lightning, cool-blue rim ambient bounce,
# dense diagonal rain (40+ lines), waves layer.
# ---------------------------------------------------------------------------
def _rain_line(x1: float, y1: float, dur: float, begin: float) -> str:
    x2 = x1 + 80
    y2 = y1 + 140
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#E8F1F8" '
        f'stroke-width="1.6" stroke-linecap="round" opacity="0.55">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 -300" to="0 1400" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'</line>'
    )

_RAIN_03A = "".join(
    _rain_line(x, -100, 0.55 + (i % 4) * 0.05, (i * 0.07) % 0.55)
    for i, x in enumerate(range(-200, 1900, 42))
)

SCENE_03A = f"""<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_03A" cx="50%" cy="50%" r="78%">
      <stop offset="55%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.6"/>
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_03A)" pointer-events="none"/>
  <!-- waves layer at bottom (dark ellipses pulsing) -->
  <g opacity="0.45">
    <ellipse cx="480" cy="1000" rx="520" ry="40" fill="#0a1a2a">
      <animate attributeName="opacity" values="0.25;0.55;0.25" dur="3.2s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="1380" cy="1020" rx="600" ry="44" fill="#0a1a2a">
      <animate attributeName="opacity" values="0.3;0.6;0.3" dur="3.6s" begin="0.8s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="980" rx="440" ry="30" fill="#0a1a2a">
      <animate attributeName="opacity" values="0.25;0.5;0.25" dur="2.8s" begin="1.4s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- diagonal rain lines -->
  <g>{_RAIN_03A}</g>
  <!-- cool-blue ambient bounce (sky rim) -->
  <rect width="1920" height="1080" fill="#3a6e9e" opacity="0">
    <animate attributeName="opacity" values="0;0;0.18;0;0;0.12;0;0;0.22;0;0" keyTimes="0;0.27;0.29;0.32;0.45;0.47;0.5;0.69;0.71;0.74;1" dur="10s" repeatCount="indefinite"/>
  </rect>
  <!-- anticipation pre-flash (white, 0.05s) + main lightning flashes -->
  <rect width="1920" height="1080" fill="#FFFFFF" opacity="0">
    <!-- 3 flashes at 2.8s, 4.6s, 6.9s with anticipation 0.05s before -->
    <animate attributeName="opacity"
      values="0;0;0.25;0;0.9;0;0;0;0.25;0;0.85;0;0;0;0.25;0;0.95;0;0"
      keyTimes="0;0.275;0.28;0.285;0.295;0.34;0.45;0.455;0.46;0.465;0.475;0.52;0.68;0.685;0.69;0.695;0.705;0.75;1"
      dur="10s" repeatCount="indefinite"/>
  </rect>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 03B — Capitano nella tempesta (NO ORANGE)
# Continuous rain (30 lines), sporadic distant lightning, hat drip.
# ---------------------------------------------------------------------------
_RAIN_03B = "".join(
    _rain_line(x, -100, 0.6 + (i % 3) * 0.05, (i * 0.09) % 0.6)
    for i, x in enumerate(range(-200, 1900, 58))
)

SCENE_03B = f"""<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_03B" cx="50%" cy="50%" r="78%">
      <stop offset="55%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.55"/>
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_03B)" pointer-events="none"/>
  <g>{_RAIN_03B}</g>
  <!-- distant lightning, dimmer, asymmetric timing 4s & 7s -->
  <rect width="1920" height="540" fill="#a8c8e8" opacity="0">
    <animate attributeName="opacity"
      values="0;0;0.18;0;0;0;0.14;0;0"
      keyTimes="0;0.49;0.5;0.52;0.78;0.85;0.86;0.88;1"
      dur="9s" repeatCount="indefinite"/>
  </rect>
  <!-- hat drip (small drop falling from tricorne area, approx top-left of captain) -->
  <g>
    <ellipse cx="820" cy="380" rx="2.4" ry="3.6" fill="#A8D8F0" opacity="0">
      <animate attributeName="cy" values="380;380;560" keyTimes="0;0.5;1" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" keyTimes="0;0.55;1" dur="2.4s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="820" cy="380" rx="2" ry="3" fill="#A8D8F0" opacity="0">
      <animate attributeName="cy" values="380;380;560" keyTimes="0;0.5;1" dur="2.4s" begin="1.1s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.7;0" keyTimes="0;0.55;1" dur="2.4s" begin="1.1s" repeatCount="indefinite"/>
    </ellipse>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 04 — Mare calmo dopo la tempesta (NO ORANGE)
# Single gull turning slow circular path, sun glare pulsing, 2 clouds drifting.
# ---------------------------------------------------------------------------
SCENE_04 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_04" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.4"/>
    </radialGradient>
    <filter id="glow_04"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="cloudBlur_04"><feGaussianBlur stdDeviation="22"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_04)" pointer-events="none"/>
  <!-- 2 soft clouds drifting slow -->
  <g filter="url(#cloudBlur_04)" opacity="0.5">
    <ellipse cx="300" cy="240" rx="180" ry="32" fill="#FFFFFF">
      <animateTransform attributeName="transform" type="translate" from="-200 0" to="2200 30" dur="42s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="800" cy="180" rx="220" ry="36" fill="#FFFFFF">
      <animateTransform attributeName="transform" type="translate" from="-400 0" to="2000 -20" dur="55s" begin="6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="1400" cy="280" rx="160" ry="28" fill="#FFFFFF">
      <animateTransform attributeName="transform" type="translate" from="-600 0" to="1800 10" dur="48s" begin="15s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- sun glare on water (center horizon, breathing) -->
  <ellipse cx="960" cy="640" rx="320" ry="22" fill="#FFE9C2" opacity="0.55" filter="url(#glow_04)">
    <animate attributeName="opacity" values="0.35;0.7;0.35" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="rx" values="280;360;280" dur="4s" repeatCount="indefinite"/>
  </ellipse>
  <!-- single gull doing slow circular turn (radius 80, period 18s) -->
  <g opacity="0.8">
    <path fill="none" stroke="#1a1a1a" stroke-width="2.6" stroke-linecap="round" d="M0,0 q9,-7 18,0 q9,7 18,0">
      <animateMotion dur="18s" repeatCount="indefinite" rotate="auto"
        path="M 1100 320 c 0 -100 200 -100 200 0 c 0 100 -200 100 -200 0 Z"/>
    </path>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 05 — Isola misteriosa WOW2 (NO ORANGE narrative, allowed pre-hint mandala cyanate)
# Fog dissipating first 8s, 4 distant gulls turning, decorative mandala
# (3 concentric circles opacity pulse), shimmer pre-revelation pulsing.
# ---------------------------------------------------------------------------
SCENE_05 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_05" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.4"/>
    </radialGradient>
    <filter id="fogBlur_05"><feGaussianBlur stdDeviation="36"/></filter>
    <filter id="glow_05"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_05)" pointer-events="none"/>
  <!-- fog cyanate dissipating progressively in first 8s, then stays subtle -->
  <rect width="1920" height="1080" fill="#A8D8F0" opacity="0.45" filter="url(#fogBlur_05)">
    <animate attributeName="opacity" values="0.45;0.1;0.12" keyTimes="0;0.55;1" dur="8s" fill="freeze"/>
  </rect>
  <!-- 4 distant gulls turning slowly across the island silhouette -->
  <g fill="none" stroke="#1a1a1a" stroke-width="2.2" stroke-linecap="round" opacity="0.6">
    <path d="M0,0 q6,-5 12,0 q6,5 12,0">
      <animateMotion dur="24s" repeatCount="indefinite" rotate="auto"
        path="M 600 380 c 100 -40 280 0 360 40 c 80 40 -60 100 -200 80 c -160 -20 -260 -80 -160 -120 Z"/>
    </path>
    <path d="M0,0 q5,-4 10,0 q5,4 10,0">
      <animateMotion dur="28s" begin="3s" repeatCount="indefinite" rotate="auto"
        path="M 800 280 c 120 -30 280 10 340 50 c 60 40 -80 90 -200 70 c -140 -20 -260 -90 -140 -120 Z"/>
    </path>
    <path d="M0,0 q5,-4 10,0 q5,4 10,0">
      <animateMotion dur="32s" begin="6s" repeatCount="indefinite" rotate="auto"
        path="M 900 420 c 80 -30 240 0 320 30 c 80 30 -60 80 -180 70 c -140 -10 -240 -70 -140 -100 Z"/>
    </path>
    <path d="M0,0 q4,-3 8,0 q4,3 8,0">
      <animateMotion dur="26s" begin="9s" repeatCount="indefinite" rotate="auto"
        path="M 1100 360 c 80 -20 220 0 260 30 c 40 30 -60 60 -160 50 c -120 -10 -180 -60 -100 -80 Z"/>
    </path>
  </g>
  <!-- 3 concentric mandala circles around island center (~960,640) -->
  <g fill="none" stroke="#A8D8F0" stroke-width="1.4" opacity="0.45" filter="url(#glow_05)">
    <circle cx="960" cy="640" r="180">
      <animate attributeName="opacity" values="0.1;0.55;0.1" dur="5s" repeatCount="indefinite"/>
      <animate attributeName="stroke" values="#A8D8F0;#A8D8F0;#A8D8F0" dur="5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="640" r="280">
      <animate attributeName="opacity" values="0.05;0.45;0.05" dur="5s" begin="0.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="640" r="380">
      <animate attributeName="opacity" values="0.05;0.35;0.05" dur="5s" begin="1.6s" repeatCount="indefinite"/>
    </circle>
  </g>
  <!-- shimmer pre-revelation: small white dots pulsing on island silhouette -->
  <g fill="#FFFFFF" filter="url(#glow_05)">
    <circle cx="940" cy="620" r="3"><animate attributeName="opacity" values="0;0.8;0" dur="3.4s" repeatCount="indefinite"/></circle>
    <circle cx="980" cy="650" r="2.5"><animate attributeName="opacity" values="0;0.7;0" dur="3.8s" begin="0.6s" repeatCount="indefinite"/></circle>
    <circle cx="1000" cy="620" r="2.5"><animate attributeName="opacity" values="0;0.75;0" dur="3.6s" begin="1.2s" repeatCount="indefinite"/></circle>
    <circle cx="920" cy="660" r="2"><animate attributeName="opacity" values="0;0.65;0" dur="4s" begin="1.8s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 06 — Sbarco (NO ORANGE)
# Waves around the rowboat (3 layers + foam), 4 oar splashes pulsing, gull turn.
# ---------------------------------------------------------------------------
SCENE_06 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_06" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.42"/>
    </radialGradient>
    <filter id="foamBlur_06"><feGaussianBlur stdDeviation="4"/></filter>
    <filter id="glow_06"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_06)" pointer-events="none"/>
  <!-- 3 wave layers lapping around boat (approx center bottom) -->
  <g filter="url(#foamBlur_06)">
    <ellipse cx="960" cy="900" rx="540" ry="14" fill="#FFFFFF" opacity="0.4">
      <animate attributeName="opacity" values="0.2;0.55;0.2" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="rx" values="500;580;500" dur="2.6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="950" rx="640" ry="16" fill="#FFFFFF" opacity="0.35">
      <animate attributeName="opacity" values="0.15;0.5;0.15" dur="3.2s" begin="0.6s" repeatCount="indefinite"/>
      <animate attributeName="rx" values="600;680;600" dur="3.2s" begin="0.6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="1000" rx="780" ry="20" fill="#FFFFFF" opacity="0.3">
      <animate attributeName="opacity" values="0.12;0.45;0.12" dur="3.8s" begin="1.2s" repeatCount="indefinite"/>
      <animate attributeName="rx" values="740;820;740" dur="3.8s" begin="1.2s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- 4 oar splash spots (small white ellipses pulsing offset) -->
  <g fill="#FFFFFF" filter="url(#glow_06)">
    <ellipse cx="780" cy="880" rx="14" ry="6" opacity="0"><animate attributeName="opacity" values="0;0.9;0" dur="1.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="860" cy="900" rx="12" ry="5" opacity="0"><animate attributeName="opacity" values="0;0.85;0" dur="1.5s" begin="0.4s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1060" cy="900" rx="12" ry="5" opacity="0"><animate attributeName="opacity" values="0;0.85;0" dur="1.5s" begin="0.8s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1140" cy="880" rx="14" ry="6" opacity="0"><animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="1.2s" repeatCount="indefinite"/></ellipse>
  </g>
  <!-- distant gull turning -->
  <g opacity="0.7">
    <path fill="none" stroke="#1a1a1a" stroke-width="2.2" stroke-linecap="round" d="M0,0 q7,-6 14,0 q7,6 14,0">
      <animateMotion dur="22s" repeatCount="indefinite" rotate="auto"
        path="M 400 260 c 100 -40 600 -40 800 0 c 200 40 -300 80 -500 60 c -300 -20 -500 -80 -300 -60 Z"/>
    </path>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 08A — Bussola si accende WOW3 (FIRST FULL ORANGE)
# Pulsing inner orange glow 3-phase, 5-7 magic orange particles rising,
# subtle upward beam.
# ---------------------------------------------------------------------------
SCENE_08A = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_08A" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <radialGradient id="glowOrange_08A" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF6B1A" stop-opacity="1"/>
      <stop offset="55%" stop-color="#FF6B1A" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FF6B1A" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow_08A"><feGaussianBlur stdDeviation="10"/></filter>
    <filter id="glowSoft_08A"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_08A)" pointer-events="none"/>
  <!-- 3-phase pulsing orange glow centered on compass (~960,640) -->
  <ellipse cx="960" cy="640" rx="80" ry="80" fill="url(#glowOrange_08A)" opacity="0.6">
    <animate attributeName="rx" values="80;160;240;160;80" keyTimes="0;0.33;0.5;0.66;1"
      keySplines="0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1"
      calcMode="spline" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="ry" values="80;160;240;160;80" keyTimes="0;0.33;0.5;0.66;1"
      keySplines="0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1"
      calcMode="spline" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;1;0.6" dur="6s" repeatCount="indefinite"/>
  </ellipse>
  <!-- soft upward beam (triangle) -->
  <path d="M 940 640 L 980 640 L 1020 80 L 900 80 Z" fill="#FF6B1A" opacity="0.18" filter="url(#glow_08A)">
    <animate attributeName="opacity" values="0.05;0.28;0.05" dur="5s" repeatCount="indefinite"/>
  </path>
  <!-- 7 magic orange particles rising from compass, staggered -->
  <g filter="url(#glowSoft_08A)">
    <circle cx="940" cy="640" r="3" fill="#FF6B1A"><animate attributeName="cy" values="640;440" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite"/></circle>
    <circle cx="970" cy="650" r="2.5" fill="#FFD580"><animate attributeName="cy" values="650;430" dur="4s" begin="0.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="4s" begin="0.5s" repeatCount="indefinite"/></circle>
    <circle cx="1000" cy="640" r="3" fill="#FF6B1A"><animate attributeName="cy" values="640;420" dur="4s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;0" dur="4s" begin="1s" repeatCount="indefinite"/></circle>
    <circle cx="920" cy="655" r="2.5" fill="#FFD580"><animate attributeName="cy" values="655;450" dur="4s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.85;0" dur="4s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle cx="980" cy="660" r="3" fill="#FF6B1A"><animate attributeName="cy" values="660;460" dur="4s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;0" dur="4s" begin="2s" repeatCount="indefinite"/></circle>
    <circle cx="950" cy="645" r="2.5" fill="#FFD580"><animate attributeName="cy" values="645;440" dur="4s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.85;0" dur="4s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle cx="1010" cy="650" r="2.5" fill="#FF6B1A"><animate attributeName="cy" values="650;430" dur="4s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="4s" begin="3s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 08B — Ago bussola (FULL ORANGE)
# Needle spinning fast (720deg in 4s), decelerates and stops, orange pulsing
# glow, 4 sparkles exploding at stop moment.
# ---------------------------------------------------------------------------
SCENE_08B = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_08B" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <radialGradient id="glowOrange_08B" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF6B1A" stop-opacity="0.8"/>
      <stop offset="60%" stop-color="#FF6B1A" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FF6B1A" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow_08B"><feGaussianBlur stdDeviation="4"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_08B)" pointer-events="none"/>
  <!-- pulsing orange glow ring around compass center -->
  <ellipse cx="960" cy="540" rx="220" ry="220" fill="url(#glowOrange_08B)" opacity="0.55">
    <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3.5s" repeatCount="indefinite"/>
  </ellipse>
  <!-- needle spinning, decelerating, then stops (rotate 720deg in 4s, then static) -->
  <g transform="translate(960,540)">
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="0;720;780;800;810;810"
        keyTimes="0;0.5;0.7;0.85;0.95;1"
        keySplines="0.1 0.6 0.4 1; 0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1; 0 0 1 1"
        calcMode="spline"
        dur="8s" repeatCount="indefinite"/>
      <polygon points="0,-90 -8,0 0,90 8,0" fill="#FF6B1A" opacity="0.85" filter="url(#glow_08B)"/>
      <polygon points="0,-90 -4,0 0,0" fill="#FFFFFF" opacity="0.7"/>
      <circle r="6" fill="#1a1a1a"/>
    </g>
  </g>
  <!-- sparkles exploding at moment of stop (~4s mark of 8s loop) -->
  <g fill="#FF6B1A" filter="url(#glow_08B)">
    <polygon points="960,420 968,450 998,458 968,466 960,496 952,466 922,458 952,450" opacity="0">
      <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.48;0.55;0.65;1" dur="8s" repeatCount="indefinite"/>
    </polygon>
    <polygon points="1100,540 1106,560 1126,566 1106,572 1100,592 1094,572 1074,566 1094,560" opacity="0">
      <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.48;0.58;0.68;1" dur="8s" repeatCount="indefinite"/>
    </polygon>
    <polygon points="820,540 826,560 846,566 826,572 820,592 814,572 794,566 814,560" opacity="0">
      <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.48;0.58;0.68;1" dur="8s" repeatCount="indefinite"/>
    </polygon>
    <polygon points="960,660 966,680 986,686 966,692 960,712 954,692 934,686 954,680" opacity="0">
      <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.48;0.55;0.65;1" dur="8s" repeatCount="indefinite"/>
    </polygon>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 09A — Cerchio di rivelazione (FULL ORANGE)
# Counter-rotating mandala under figures (30s), 3 concentric light waves
# from compass center, orange particles rising around figures.
# ---------------------------------------------------------------------------
SCENE_09A = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_09A" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <filter id="glow_09A"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="glowSoft_09A"><feGaussianBlur stdDeviation="2.5"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_09A)" pointer-events="none"/>
  <!-- mandala counter-rotating under figures (center ~960,780) -->
  <g transform="translate(960,780)" opacity="0.55" filter="url(#glow_09A)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="30s" repeatCount="indefinite"/>
      <circle r="240" fill="none" stroke="#FF6B1A" stroke-width="1.6" stroke-dasharray="14 22"/>
      <circle r="180" fill="none" stroke="#FF6B1A" stroke-width="1.2" stroke-dasharray="8 14"/>
      <g stroke="#FF6B1A" stroke-width="1" opacity="0.6">
        <line x1="-260" y1="0" x2="260" y2="0"/>
        <line x1="0" y1="-260" x2="0" y2="260"/>
        <line x1="-184" y1="-184" x2="184" y2="184"/>
        <line x1="-184" y1="184" x2="184" y2="-184"/>
      </g>
    </g>
  </g>
  <!-- 3 concentric light waves expanding from center -->
  <g fill="none" stroke="#FF6B1A" stroke-width="2" filter="url(#glow_09A)">
    <circle cx="960" cy="780" r="100">
      <animate attributeName="r" values="100;500" dur="5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="780" r="100">
      <animate attributeName="r" values="100;500" dur="5s" begin="1.6s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="5s" begin="1.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="780" r="100">
      <animate attributeName="r" values="100;500" dur="5s" begin="3.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="5s" begin="3.2s" repeatCount="indefinite"/>
    </circle>
  </g>
  <!-- orange particles rising around figures -->
  <g fill="#FF6B1A" filter="url(#glowSoft_09A)">
    <circle cx="720" cy="800" r="2.4"><animate attributeName="cy" values="800;480" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="6s" repeatCount="indefinite"/></circle>
    <circle cx="820" cy="820" r="2.6"><animate attributeName="cy" values="820;500" dur="7s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="7s" begin="1s" repeatCount="indefinite"/></circle>
    <circle cx="1100" cy="820" r="2.4"><animate attributeName="cy" values="820;480" dur="6.5s" begin="0.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="6.5s" begin="0.5s" repeatCount="indefinite"/></circle>
    <circle cx="1200" cy="800" r="2.6"><animate attributeName="cy" values="800;500" dur="7s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="7s" begin="2s" repeatCount="indefinite"/></circle>
    <circle cx="900" cy="830" r="2.4"><animate attributeName="cy" values="830;510" dur="6s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="6s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle cx="1020" cy="830" r="2.6"><animate attributeName="cy" values="830;490" dur="6.5s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="6.5s" begin="3s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 10 — Ritorno alla nave (FULL ORANGE allowed - they carry compass)
# 4 oar splashes pulse, 3 wave layers, gull turning, subtle orange glow
# from boat (compass being carried back).
# ---------------------------------------------------------------------------
SCENE_10 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_10" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.42"/>
    </radialGradient>
    <radialGradient id="boatGlow_10" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF6B1A" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#FF6B1A" stop-opacity="0"/>
    </radialGradient>
    <filter id="foamBlur_10"><feGaussianBlur stdDeviation="4"/></filter>
    <filter id="glow_10"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_10)" pointer-events="none"/>
  <!-- subtle orange glow from boat (compass carried) -->
  <ellipse cx="960" cy="780" rx="180" ry="80" fill="url(#boatGlow_10)" opacity="0.5">
    <animate attributeName="opacity" values="0.3;0.6;0.3" dur="4s" repeatCount="indefinite"/>
  </ellipse>
  <!-- 3 wave layers -->
  <g filter="url(#foamBlur_10)">
    <ellipse cx="960" cy="900" rx="540" ry="12" fill="#FFFFFF" opacity="0.4">
      <animate attributeName="opacity" values="0.2;0.55;0.2" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="rx" values="500;580;500" dur="2.6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="960" rx="660" ry="14" fill="#FFFFFF" opacity="0.35">
      <animate attributeName="opacity" values="0.15;0.5;0.15" dur="3.2s" begin="0.6s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="1020" rx="800" ry="18" fill="#FFFFFF" opacity="0.3">
      <animate attributeName="opacity" values="0.12;0.45;0.12" dur="3.8s" begin="1.2s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- 4 oar splashes -->
  <g fill="#FFFFFF" filter="url(#glow_10)">
    <ellipse cx="780" cy="880" rx="14" ry="6" opacity="0"><animate attributeName="opacity" values="0;0.9;0" dur="1.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="860" cy="900" rx="12" ry="5" opacity="0"><animate attributeName="opacity" values="0;0.85;0" dur="1.5s" begin="0.4s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1060" cy="900" rx="12" ry="5" opacity="0"><animate attributeName="opacity" values="0;0.85;0" dur="1.5s" begin="0.8s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1140" cy="880" rx="14" ry="6" opacity="0"><animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="1.2s" repeatCount="indefinite"/></ellipse>
  </g>
  <!-- gull turning above -->
  <g opacity="0.7">
    <path fill="none" stroke="#1a1a1a" stroke-width="2.4" stroke-linecap="round" d="M0,0 q8,-6 16,0 q8,6 16,0">
      <animateMotion dur="20s" repeatCount="indefinite" rotate="auto"
        path="M 500 280 c 100 -40 600 -40 800 0 c 200 40 -300 80 -500 60 c -300 -20 -500 -80 -300 -60 Z"/>
    </path>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 11A — Salpa al tramonto (FULL ORANGE - sunset)
# Orange flag flapping, sun-reflection glitter on water (5 staggered),
# 8-10 gold dust in god rays, sails gentle scale breathing.
# ---------------------------------------------------------------------------
SCENE_11A = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_11A" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.4"/>
    </radialGradient>
    <filter id="glow_11A"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="glowSoft_11A"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_11A)" pointer-events="none"/>
  <!-- sails breathing (subtle scale on a soft white shape) -->
  <g transform="translate(960,420)" opacity="0.08">
    <ellipse cx="0" cy="0" rx="220" ry="180" fill="#FFFFFF">
      <animateTransform attributeName="transform" type="scale" values="1;1.04;1" dur="6s" repeatCount="indefinite"/>
    </ellipse>
  </g>
  <!-- orange flag flapping on main mast (top center-ish) -->
  <g transform="translate(940,80)" opacity="0.9">
    <rect x="-2" y="0" width="3" height="240" fill="#2a1f17"/>
    <path fill="#FF6B1A" stroke="#3a2e22" stroke-width="1">
      <animate attributeName="d"
        values="M0,10 L130,18 L142,56 L130,92 L0,82 Z;
                M0,10 L130,4 L150,50 L130,98 L0,82 Z;
                M0,10 L130,24 L138,62 L132,86 L0,82 Z;
                M0,10 L130,18 L142,56 L130,92 L0,82 Z"
        keyTimes="0;0.34;0.68;1"
        keySplines="0.42 0 0.58 1; 0.42 0 0.58 1; 0.42 0 0.58 1"
        calcMode="spline" dur="3.2s" repeatCount="indefinite"/>
    </path>
  </g>
  <!-- sun glitter ellipses on water, staggered pulse -->
  <g filter="url(#glowSoft_11A)">
    <ellipse cx="540" cy="780" rx="80" ry="3" fill="#FFD580"><animate attributeName="opacity" values="0.2;0.85;0.2" dur="2.4s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="760" cy="800" rx="120" ry="3" fill="#FFD580"><animate attributeName="opacity" values="0.2;0.85;0.2" dur="2.8s" begin="0.4s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1020" cy="820" rx="160" ry="3.5" fill="#FFD580"><animate attributeName="opacity" values="0.25;0.9;0.25" dur="3.2s" begin="0.8s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1280" cy="800" rx="120" ry="3" fill="#FFD580"><animate attributeName="opacity" values="0.2;0.85;0.2" dur="2.8s" begin="1.2s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="1500" cy="780" rx="80" ry="3" fill="#FFD580"><animate attributeName="opacity" values="0.2;0.8;0.2" dur="2.4s" begin="1.6s" repeatCount="indefinite"/></ellipse>
  </g>
  <!-- gold dust rising in sunset god rays -->
  <g filter="url(#glow_11A)">
    <circle r="2.6" cx="240" cy="930" fill="#FFD580"><animate attributeName="cy" values="930;200" dur="12s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.75;0" dur="12s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="420" cy="960" fill="#FFD580"><animate attributeName="cy" values="960;240" dur="14s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.65;0" dur="14s" begin="1s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="640" cy="940" fill="#FFD580"><animate attributeName="cy" values="940;220" dur="13s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="13s" begin="2s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="860" cy="970" fill="#FFD580"><animate attributeName="cy" values="970;260" dur="15s" begin="0.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="15s" begin="0.5s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="1100" cy="950" fill="#FFD580"><animate attributeName="cy" values="950;200" dur="13s" begin="3s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.75;0" dur="13s" begin="3s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="1320" cy="980" fill="#FFD580"><animate attributeName="cy" values="980;280" dur="16s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="16s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="1500" cy="930" fill="#FFD580"><animate attributeName="cy" values="930;190" dur="12s" begin="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="12s" begin="4s" repeatCount="indefinite"/></circle>
    <circle r="2.2" cx="1700" cy="960" fill="#FFD580"><animate attributeName="cy" values="960;240" dur="14s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="14s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle r="2.6" cx="180" cy="950" fill="#FFD580"><animate attributeName="cy" values="950;220" dur="13s" begin="5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.7;0" dur="13s" begin="5s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 11B — Due bussole sul tavolo (FULL ORANGE)
# Pulsing orange glow from new compass, brass needle subtle oscillation,
# warm dust particles in background.
# ---------------------------------------------------------------------------
SCENE_11B = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_11B" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
    </radialGradient>
    <radialGradient id="compassGlow_11B" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF6B1A" stop-opacity="0.85"/>
      <stop offset="60%" stop-color="#FF6B1A" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#FF6B1A" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow_11B"><feGaussianBlur stdDeviation="4"/></filter>
    <filter id="glowSoft_11B"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_11B)" pointer-events="none"/>
  <!-- pulsing glow from new compass (right side, approx 1180,580) -->
  <ellipse cx="1180" cy="580" rx="60" ry="60" fill="url(#compassGlow_11B)" opacity="0.7">
    <animate attributeName="rx" values="60;120;60" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="ry" values="60;120;60" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;0.95;0.5" dur="4s" repeatCount="indefinite"/>
  </ellipse>
  <!-- brass compass needle oscillation (left compass, approx 740,580) -->
  <g transform="translate(740,580)">
    <g>
      <animateTransform attributeName="transform" type="rotate"
        values="-3;3;-3" keyTimes="0;0.5;1"
        keySplines="0.42 0 0.58 1; 0.42 0 0.58 1" calcMode="spline"
        dur="3.6s" repeatCount="indefinite"/>
      <polygon points="0,-46 -4,0 0,46 4,0" fill="#c9a86a" opacity="0.75" filter="url(#glow_11B)"/>
      <polygon points="0,-46 -2,0 0,0" fill="#FFFFFF" opacity="0.5"/>
      <circle r="3" fill="#3a2e22"/>
    </g>
  </g>
  <!-- warm dust particles around -->
  <g filter="url(#glowSoft_11B)">
    <circle r="2.4" cx="380" cy="820" fill="#FFD580"><animate attributeName="cy" values="820;380" dur="14s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="14s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="540" cy="860" fill="#FFD580"><animate attributeName="cy" values="860;420" dur="16s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="16s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle r="2.4" cx="1500" cy="840" fill="#FFD580"><animate attributeName="cy" values="840;400" dur="14s" begin="2.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.6;0" dur="14s" begin="2.5s" repeatCount="indefinite"/></circle>
    <circle r="2" cx="1660" cy="870" fill="#FFD580"><animate attributeName="cy" values="870;440" dur="16s" begin="3.5s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.55;0" dur="16s" begin="3.5s" repeatCount="indefinite"/></circle>
  </g>
</svg>"""

# ---------------------------------------------------------------------------
# Scene 12 — Transizione (FULL ORANGE, bridge to realistic deck)
# Hexagonal orange compass scaling 0.4->2.6 in 7s ease-out,
# 4-5 concentric orange light waves, cream overlay fade-in last 1.2s.
# ---------------------------------------------------------------------------
SCENE_12 = """<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vig_12" cx="50%" cy="50%" r="78%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.4"/>
    </radialGradient>
    <filter id="glow_12"><feGaussianBlur stdDeviation="8"/></filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#vig_12)" pointer-events="none"/>
  <!-- 4 concentric orange light waves -->
  <g fill="none" stroke="#FF6B1A" stroke-width="2" filter="url(#glow_12)">
    <circle cx="960" cy="540" r="80">
      <animate attributeName="r" values="80;600" dur="3.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="3.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="540" r="80">
      <animate attributeName="r" values="80;600" dur="3.5s" begin="0.9s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="3.5s" begin="0.9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="540" r="80">
      <animate attributeName="r" values="80;600" dur="3.5s" begin="1.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="3.5s" begin="1.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="960" cy="540" r="80">
      <animate attributeName="r" values="80;600" dur="3.5s" begin="2.7s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;0" dur="3.5s" begin="2.7s" repeatCount="indefinite"/>
    </circle>
  </g>
  <!-- hexagonal orange compass scaling exponentially 0.4 -> 2.6 in 7s (loop) -->
  <g transform="translate(960,540)" filter="url(#glow_12)">
    <g>
      <animateTransform attributeName="transform" type="scale"
        values="0.4;2.6" keyTimes="0;1"
        keySplines="0.16 1 0.3 1" calcMode="spline"
        dur="7s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="7s" repeatCount="indefinite"/>
      <!-- hexagon -->
      <polygon points="0,-120 104,-60 104,60 0,120 -104,60 -104,-60"
        fill="none" stroke="#FF6B1A" stroke-width="3"/>
      <polygon points="0,-60 52,-30 52,30 0,60 -52,30 -52,-30"
        fill="none" stroke="#FF6B1A" stroke-width="2"/>
      <!-- compass needle inside -->
      <polygon points="0,-80 -8,0 0,80 8,0" fill="#FF6B1A"/>
    </g>
  </g>
  <!-- cream overlay fade-in last 1.2s of 7s loop (~5.8s..7s) -->
  <rect width="1920" height="1080" fill="#FAF7F2" opacity="0">
    <animate attributeName="opacity" values="0;0;0.85" keyTimes="0;0.828;1" dur="7s" repeatCount="indefinite"/>
  </rect>
</svg>"""


SCENE_OVERLAYS = {
    "01":  SCENE_01,
    "02A": SCENE_02A,
    "03A": SCENE_03A,
    "03B": SCENE_03B,
    "04":  SCENE_04,
    "05":  SCENE_05,
    "06":  SCENE_06,
    "08A": SCENE_08A,
    "08B": SCENE_08B,
    "09A": SCENE_09A,
    "10":  SCENE_10,
    "11A": SCENE_11A,
    "11B": SCENE_11B,
    "12":  SCENE_12,
}


def get_overlay(scene_id: str) -> str | None:
    """Return the scene-specific SVG overlay string, or None if not defined."""
    return SCENE_OVERLAYS.get(scene_id.upper())


if __name__ == "__main__":
    total = sum(len(v) for v in SCENE_OVERLAYS.values())
    print(f"Scenes: {len(SCENE_OVERLAYS)}")
    print(f"Total payload: {total/1024:.2f} KB")
    for k, v in SCENE_OVERLAYS.items():
        print(f"  {k:>4}: {len(v)/1024:.2f} KB")
