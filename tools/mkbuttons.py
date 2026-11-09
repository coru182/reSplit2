#!/usr/bin/env python3
"""reSplit2: the PlayStation buttons drawn in place of TimeSplitters 2's Xbox ones (original art, GPL-3.0).

Writes game/art/*.png, four times the game's own sizes, and game/src/game/ts2_button_art.cpp with them built in:
  cross / circle / square / triangle.png  128x128, for the game's 32x32 A / B / X / Y buttons
  sheet.png                               512x256, for its 128x64 sheet: B Y X A, Start and Back, two arrows
Needs rsvg-convert (librsvg2-bin).   python3 tools/mkbuttons.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'game', 'art')

# the PlayStation colours: Cross blue, Circle red, Square pink, Triangle green
COLOURS = {'cross': '#8fb3ff', 'circle': '#ff6d6d', 'square': '#ff9ade', 'triangle': '#3ee0a8'}


def button(kind, cx, cy, r):
    """a dark glossy face button of radius r at (cx, cy), its symbol in its colour"""
    c = COLOURS[kind]
    s = r * 0.46  # the symbol's half size
    w = r * 0.155  # its stroke
    if kind == 'cross':
        sym = (f'<path d="M{cx-s},{cy-s} L{cx+s},{cy+s} M{cx+s},{cy-s} L{cx-s},{cy+s}" stroke="{c}" '
               f'stroke-width="{w}" stroke-linecap="round" fill="none"/>')
    elif kind == 'circle':
        sym = f'<circle cx="{cx}" cy="{cy}" r="{s*0.95}" stroke="{c}" stroke-width="{w}" fill="none"/>'
    elif kind == 'square':
        q = s * 0.82
        sym = (f'<rect x="{cx-q}" y="{cy-q}" width="{2*q}" height="{2*q}" rx="{w*0.25}" stroke="{c}" '
               f'stroke-width="{w}" fill="none"/>')
    else:
        t = s * 1.05
        sym = (f'<path d="M{cx},{cy-t} L{cx+t*0.98},{cy+t*0.68} L{cx-t*0.98},{cy+t*0.68} Z" stroke="{c}" '
               f'stroke-width="{w}" stroke-linejoin="round" fill="none"/>')
    gid = f'g{kind}{int(cx)}{int(cy)}'
    return f'''
  <defs>
    <radialGradient id="{gid}" cx="40%" cy="32%" r="75%">
      <stop offset="0" stop-color="#5a606c"/><stop offset="0.55" stop-color="#262a31"/><stop offset="1" stop-color="#0d0f12"/>
    </radialGradient>
    <linearGradient id="{gid}h" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <circle cx="{cx}" cy="{cy+r*0.06}" r="{r}" fill="#000" opacity="0.45"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})" stroke="#07080a" stroke-width="{r*0.06}"/>
  <circle cx="{cx}" cy="{cy}" r="{r*0.9}" fill="none" stroke="#7d8594" stroke-opacity="0.35" stroke-width="{r*0.04}"/>
  <g filter="url(#glow)">{sym}</g>
  <ellipse cx="{cx-r*0.12}" cy="{cy-r*0.48}" rx="{r*0.55}" ry="{r*0.3}" fill="url(#{gid}h)"/>'''


GLOW = '''<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'''


def pill(x0, y0, x1, y1, label, lx, ly):
    """a small dark pill button (Options, the touch pad) with its name under it"""
    h = y1 - y0
    return f'''
  <rect x="{x0}" y="{y0+3}" width="{x1-x0}" height="{h}" rx="{h/2}" fill="#000" opacity="0.4"/>
  <rect x="{x0}" y="{y0}" width="{x1-x0}" height="{h}" rx="{h/2}" fill="#23272e" stroke="#07080a" stroke-width="3"/>
  <rect x="{x0+8}" y="{y0+6}" width="{x1-x0-16}" height="{h*0.35}" rx="{h*0.17}" fill="#ffffff" opacity="0.18"/>
  <text x="{lx}" y="{ly}" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="24"
        fill="#ffffff" letter-spacing="0.5">{label}</text>'''


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{GLOW}{body}</svg>'


def render(name, text):
    src = os.path.join(ART, name + '.svg')
    with open(src, 'w') as f:
        f.write(text)
    out = os.path.join(ART, name + '.png')
    subprocess.run(['rsvg-convert', src, '-o', out], check=True)
    os.remove(src)
    return out


def main():
    os.makedirs(ART, exist_ok=True)
    pngs = {}
    # the 32x32 buttons: the game's fill x 1..29, y 2..29 of 32; four times larger
    for kind in COLOURS:
        pngs[kind] = render(kind, svg(128, 128, button(kind, 61, 63, 53)))
    # the 128x64 sheet: B Y X A in its top row (centres 15.5, 47, 80, 112.5; y 16.5; about 26 x 31), Start and Back
    # pills (x 5..27 and 38..60, y 34..50) with their names under them (y 56..61), and the two white arrows
    body = ''.join(button(k, cx * 4, 66, 54) for k, cx in (('circle', 15.5), ('triangle', 47), ('square', 80),
                                                              ('cross', 112.5)))
    body += pill(20, 140, 108, 196, 'OPTIONS', 64, 242)
    body += pill(152, 140, 240, 196, 'PAD', 196, 242)
    body += '<path d="M286,140 L334,192 L286,244 Z" fill="#e5e5e5"/>'  # the right arrow (x 71..84, y 34..61)
    body += '<path d="M432,164 L484,216 L380,216 Z" fill="#e4e4e4"/>'  # the up arrow (x 94..121, y 41..54)
    pngs['sheet'] = render('sheet', svg(512, 256, body))
    # built into the program
    out = os.path.join(ROOT, 'game', 'src', 'game', 'ts2_button_art.cpp')
    with open(out, 'w') as o:
        o.write('// written by tools/mkbuttons.py from game/art/*.png (reSplit2\'s own drawings, GPL-3.0)\n')
        o.write('#include <cstddef>\n\nnamespace ts2::art {\n')
        for name, path in pngs.items():
            data = open(path, 'rb').read()
            o.write(f'extern const unsigned char k{name.capitalize()}[];\n')
            o.write(f'extern const size_t k{name.capitalize()}Size = {len(data)};\n')
            o.write(f'const unsigned char k{name.capitalize()}[] = {{')
            for i in range(0, len(data), 24):
                o.write('\n    ' + ','.join(str(b) for b in data[i:i + 24]) + ',')
            o.write('\n};\n')
        o.write('}  // namespace ts2::art\n')
    print('mkbuttons: game/art/*.png and', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    sys.exit(main())
