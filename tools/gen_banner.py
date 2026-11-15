"""Generate the profile banner SVG. With FREEZE=t, emit a paused frame at t seconds (for previews)."""
import sys, random
freeze = float(sys.argv[2]) if len(sys.argv) > 2 else None
random.seed(7)
W, H, LOOP = 1200, 300, 10.0
GROUND = 246
X0, X1, T0, T1 = -120, 1320, 2.8, 4.4          # blade sweep: x range and seconds

def anim(name, delay=0.0, dur=LOOP, extra=""):
    if freeze is not None:
        return f"animation:{name} {dur}s linear infinite paused;animation-delay:{delay - freeze:.3f}s;{extra}"
    return f"animation:{name} {dur}s linear infinite;animation-delay:{delay:.3f}s;{extra}"

pins = [(250, 196, 9), (330, 172, 12), (415, 190, 10), (505, 150, 14), (600, 128, 17),
        (695, 156, 13), (785, 186, 11), (870, 168, 12), (950, 198, 9)]

o = []
o.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated banner">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#07070b"/><stop offset="0.55" stop-color="#0d0a10"/><stop offset="1" stop-color="#1a0a10"/>
  </linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0.62" stop-color="#c1121f" stop-opacity="0.55"/><stop offset="1" stop-color="#c1121f" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ground" x1="0" x2="1"><stop offset="0" stop-color="#6b6b76" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#6b6b76" stop-opacity="0.9"/><stop offset="1" stop-color="#6b6b76" stop-opacity="0"/></linearGradient>
  <linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="#e5383b" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#e5383b"/><stop offset="1" stop-color="#e5383b" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .h{{transform-box:fill-box;transform-origin:center}}
  @keyframes head{{0%,100%{{transform:translate(0,0) rotate(0) scale(1);opacity:1}}
    13%{{transform:translate(34px,var(--f)) rotate(160deg) scale(.9);opacity:.75}}
    20%{{transform:translate(40px,var(--f)) rotate(200deg) scale(.9);opacity:0}}
    30%{{transform:translate(40px,var(--f)) rotate(200deg) scale(.9);opacity:0}}
    30.1%{{transform:translate(0,0) rotate(0) scale(0);opacity:0}}
    46%{{transform:translate(0,0) rotate(0) scale(1);opacity:1}}}}
  @keyframes drop{{0%{{transform:translateY(0);opacity:0}}1%{{opacity:1}}
    14%{{transform:translateY(var(--d));opacity:.9}}18%,100%{{transform:translateY(var(--d));opacity:0}}}}
  @keyframes spark{{0%{{opacity:0;transform:scale(.2)}}1.5%{{opacity:1;transform:scale(1)}}6%,100%{{opacity:0;transform:scale(1.6)}}}}
  @keyframes blade{{0%{{transform:translateX({X0}px);opacity:0}}1%{{opacity:1}}
    {(T1-T0)/LOOP*100:.1f}%{{transform:translateX({X1}px);opacity:1}}{(T1-T0)/LOOP*100+1:.1f}%,100%{{transform:translateX({X1}px);opacity:0}}}}
  @keyframes trail{{0%{{stroke-dashoffset:1;opacity:.9}}{(T1-T0)/LOOP*100:.1f}%{{stroke-dashoffset:0;opacity:.9}}
    34%,100%{{stroke-dashoffset:0;opacity:0}}}}
  @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
  @keyframes twinkle{{0%,100%{{opacity:.15}}50%{{opacity:.8}}}}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>''')

for _ in range(46):
    x, y, r = random.uniform(20, W-20), random.uniform(12, 225), random.choice([0.6, 0.8, 1.0, 1.3])
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#d9d4cf" style="{anim("twinkle", -random.uniform(0, 6), random.choice([4, 5, 7]))}"/>')

# eclipsed disc
o.append(f'<circle cx="600" cy="138" r="150" fill="url(#halo)" style="{anim("pulse", 0, 6)}"/>')
o.append('<circle cx="600" cy="138" r="96" fill="#050507" stroke="#c1121f" stroke-width="1.6"/>')
o.append('<circle cx="600" cy="138" r="104" fill="none" stroke="#c1121f" stroke-opacity=".28" stroke-width="1"/>')
o.append(f'<rect x="90" y="{GROUND}" width="{W-180}" height="1.2" fill="url(#ground)"/>')

for x, top, r in pins:
    t = T0 + (T1 - T0) * (x - 62 - X0) / (X1 - X0)       # moment the blade reaches this pin
    cy = top - r - 3
    o.append(f'<line x1="{x}" y1="{GROUND}" x2="{x}" y2="{top}" stroke="#8d8d98" stroke-width="1.6" stroke-linecap="round"/>')
    for dx, dd in ((-3, 0.0), (4, 0.25)):
        o.append(f'<circle cx="{x+dx}" cy="{top+2}" r="2.2" fill="#e5383b" style="--d:{GROUND-top-4}px;opacity:0;{anim("drop", t+dd)}"/>')
    o.append(f'<circle class="h" cx="{x}" cy="{top}" r="9" fill="none" stroke="#ff6b6b" stroke-width="1.4" style="opacity:0;{anim("spark", t)}"/>')
    o.append(f'<circle class="h" cx="{x}" cy="{cy}" r="{r}" fill="#ece7e1" style="--f:{GROUND - cy - r}px;{anim("head", t)}"/>')

# slash trail + crescent blade
o.append(f'<path d="M{X0},236 Q600,84 {X1},236" pathLength="1" fill="none" stroke="url(#trail)" stroke-width="1.4" stroke-dasharray="1" stroke-dashoffset="1" style="opacity:0;{anim("trail", T0)}"/>')
cres = "M0,-78 A78,78 0 0 1 0,78 A104,104 0 0 0 0,-78 Z"
o.append(f'<g style="opacity:0;{anim("blade", T0)}"><g transform="translate(0,160)">'
         f'<path d="{cres}" fill="#e5383b" filter="url(#glow)" opacity=".8"/><path d="{cres}" fill="#f4efe9"/></g></g>')
o.append('</g></svg>')
open(sys.argv[1], 'w').write("\n".join(o))
