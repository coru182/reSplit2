#!/usr/bin/env python3
"""reSplit2: the PlayStation buttons drawn in place of TimeSplitters 2's Xbox ones (original art, GPL-3.0).

Writes game/art/*.png, four times the game's own sizes, and game/src/game/ts2_button_art.cpp with them built in:
  cross / circle / square / triangle.png  128x128, for the game's 32x32 A / B / X / Y buttons
  sheet.png                               512x256, for its 128x64 sheet: B Y X A, Start and Back, two arrows
  pad.png                                 1024x1024, for its 128x128 controller picture (the Controls menu)
  pad_glow.png                            256x256, for the 64x64 glow drawn behind that picture
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


def svg(w, h, body, scale=1):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*scale}" height="{h*scale}" viewBox="0 0 {w} {h}">'
            f'{GLOW}{body}</svg>')


def render(name, text):
    src = os.path.join(ART, name + '.svg')
    with open(src, 'w') as f:
        f.write(text)
    out = os.path.join(ART, name + '.png')
    subprocess.run(['rsvg-convert', src, '-o', out], check=True)
    os.remove(src)
    return out


# The controller picture: reSplit2's own controller, white with PlayStation buttons on it. The game draws its
# 128x128 picture 152 wide and 128 tall at (74, 145) of its 640x480 screen, so the controller is drawn in that shape
# (608 x 512, centre 304, 266) and narrowed to the square; the drawing below is in a 512 x 512 space around
# (256, 266), drawn 1.2 times larger.
FIT = 'scale(0.842105,1) translate(304,266) scale(1.2) translate(-256,-266)'


def mirrored(right):
    """a closed outline symmetric about x 256, from its right half: a start, then cubic segments (c1, c2, end)"""
    start, segs = right[0], right[1:]
    d = f'M{start[0]},{start[1]} ' + ''.join(f'C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {e[0]},{e[1]} ' for c1, c2, e in segs)
    ends = [start] + [e for _, _, e in segs]
    for i in range(len(segs) - 1, -1, -1):  # back along the left half
        c1, c2, _ = segs[i]
        d += f'C{512-c2[0]},{c2[1]} {512-c1[0]},{c1[1]} {512-ends[i][0]},{ends[i][1]} '
    return d + 'Z'


BODY = mirrored([(256, 340),
                 ((290, 340), (318, 340), (338, 346)),
                 ((362, 354), (378, 378), (394, 404)),
                 ((410, 428), (430, 440), (452, 438)),
                 ((486, 434), (504, 404), (504, 360)),
                 ((504, 296), (496, 228), (482, 184)),
                 ((470, 146), (438, 124), (396, 124)),
                 ((350, 124), (300, 134), (256, 134))])
SHOULDERS = (78, 322)  # L1 and R1: 112 x 40 from y 104

# the symbols a shade deeper than the prompts' (COLOURS), to stand out on white
PAD_COLOURS = {'triangle': '#1aa57c', 'circle': '#e5484d', 'cross': '#4a7de6', 'square': '#d45aae'}

PAD_DEFS = '''<defs>
 <linearGradient id="shell" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fbfcfd"/><stop offset="0.55" stop-color="#eceff3"/><stop offset="1" stop-color="#cfd4db"/>
 </linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#5b6470" stop-opacity="0.35"/>
 </linearGradient>
 <radialGradient id="cap" cx="45%" cy="35%" r="70%">
  <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e1e5ea"/>
 </radialGradient>
 <radialGradient id="stick" cx="50%" cy="40%" r="60%">
  <stop offset="0" stop-color="#3d424b"/><stop offset="1" stop-color="#1d2025"/>
 </radialGradient>
 <radialGradient id="stickcap" cx="45%" cy="38%" r="65%">
  <stop offset="0" stop-color="#4a5059"/><stop offset="1" stop-color="#262a30"/>
 </radialGradient>
 <linearGradient id="shoulder" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#4a4f58"/><stop offset="1" stop-color="#25282e"/>
 </linearGradient>
 <filter id="shade" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>'''


def face(kind, cx, cy, r):
    """a white face button with its symbol in its colour"""
    c = PAD_COLOURS[kind]
    s, w = r * 0.5, r * 0.16
    if kind == 'cross':
        sym = (f'<path d="M{cx-s},{cy-s} L{cx+s},{cy+s} M{cx+s},{cy-s} L{cx-s},{cy+s}" stroke="{c}" '
               f'stroke-width="{w}" stroke-linecap="round"/>')
    elif kind == 'circle':
        sym = f'<circle cx="{cx}" cy="{cy}" r="{s*0.95}" stroke="{c}" stroke-width="{w}" fill="none"/>'
    elif kind == 'square':
        q = s * 0.8
        sym = (f'<rect x="{cx-q}" y="{cy-q}" width="{2*q}" height="{2*q}" rx="{w*0.3}" stroke="{c}" '
               f'stroke-width="{w}" fill="none"/>')
    else:
        t = s * 1.05
        sym = (f'<path d="M{cx},{cy-t} L{cx+t*0.98},{cy+t*0.7} L{cx-t*0.98},{cy+t*0.7} Z" stroke="{c}" '
               f'stroke-width="{w}" stroke-linejoin="round" fill="none"/>')
    return (f'<circle cx="{cx}" cy="{cy+2.5}" r="{r}" fill="#9aa2ad" opacity="0.6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#cap)" stroke="#8a929c" stroke-width="2"/>{sym}')


def stick(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="46" fill="#c9ced6" stroke="#9aa1ab" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy+3}" r="36" fill="#14161a" opacity="0.35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="36" fill="url(#stick)" stroke="#1b1e23" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="25" fill="url(#stickcap)" stroke="#202329" stroke-width="2"/>'
            f'<ellipse cx="{cx-5}" cy="{cy-13}" rx="13" ry="6" fill="#fff" opacity="0.12"/>')


def dpad(cx, cy):
    a, b = 14, 38  # an arm's half width, its reach
    p = (f'M{cx-a},{cy-b} L{cx+a},{cy-b} L{cx+a},{cy-a} L{cx+b},{cy-a} L{cx+b},{cy+a} L{cx+a},{cy+a} '
         f'L{cx+a},{cy+b} L{cx-a},{cy+b} L{cx-a},{cy+a} L{cx-b},{cy+a} L{cx-b},{cy-a} L{cx-a},{cy-a} Z')
    arrows = ''
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        tx, ty = cx + dx * 26, cy + dy * 26
        pts = (f'{tx},{ty+dy*6} {tx-5.5},{ty-dy*3} {tx+5.5},{ty-dy*3}' if dx == 0 else
               f'{tx+dx*6},{ty} {tx-dx*3},{ty-5.5} {tx-dx*3},{ty+5.5}')
        arrows += f'<polygon points="{pts}" fill="#3a3f47"/>'
    return (f'<path d="{p}" transform="translate(0,3)" fill="#9aa2ad" opacity="0.6"/>'
            f'<path d="{p}" fill="url(#cap)" stroke="#8a929c" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="6" fill="#d3d8df"/>{arrows}')


def controller():
    s = PAD_DEFS
    for x in SHOULDERS:  # behind the body
        s += f'<rect x="{x}" y="104" width="112" height="40" rx="16" fill="url(#shoulder)" stroke="#1b1e23" stroke-width="2.5"/>'
        s += f'<rect x="{x+14}" y="110" width="84" height="6" rx="3" fill="#fff" opacity="0.18"/>'
    s += f'<path d="{BODY}" transform="translate(0,8)" fill="#000" opacity="0.35" filter="url(#shade)"/>'
    s += f'<path d="{BODY}" fill="url(#shell)" stroke="#7e8691" stroke-width="3"/>'
    s += f'<path d="{BODY}" fill="url(#edge)"/>'
    s += ('<path d="M150,150 C200,142 230,141 256,141 C282,141 312,142 362,150" fill="none" stroke="#fff" '
          'stroke-width="5" stroke-linecap="round" opacity="0.9"/>')  # the top's highlight
    # the centre: two small buttons and a round one, ringed in the menus' blue
    for cx in (196, 316):
        s += f'<rect x="{cx-6}" y="186" width="12" height="26" rx="6" fill="#d3d8df" stroke="#8a929c" stroke-width="2"/>'
    s += ('<circle cx="256" cy="230" r="17" fill="url(#cap)" stroke="#8a929c" stroke-width="2"/>'
          '<circle cx="256" cy="230" r="10" fill="none" stroke="#4fa3f7" stroke-width="3"/>')
    s += dpad(128, 216)
    s += stick(190, 300) + stick(322, 300)
    # the face buttons: Triangle at the top, Circle right, Cross at the bottom, Square left
    for kind, dx, dy in (('triangle', 0, -1), ('circle', 1, 0), ('cross', 0, 1), ('square', -1, 0)):
        s += face(kind, 384 + dx * 36, 216 + dy * 36, 20)
    return f'<g transform="{FIT}">{s}</g>'


def outline():
    """the controller's shape in white, for its glow"""
    s = f'<path d="{BODY}" fill="#fff"/>'
    s += ''.join(f'<rect x="{x}" y="104" width="112" height="40" rx="16" fill="#fff"/>' for x in SHOULDERS)
    return f'<g transform="{FIT}">{s}</g>'


def glow():
    """the 64x64 glow is drawn 290 x 256 from (5, 81), the picture 152 x 128 from (74, 145): the outline placed as the
    game places the picture over it, widened a little and blurred"""
    place = f'translate({69/290*256:.3f},64) scale({152/290*256/512:.6f},0.25)'
    return (f'<defs><filter id="soft" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feMorphology operator="dilate" radius="3"/><feGaussianBlur stdDeviation="4"/></filter></defs>'
            f'<g filter="url(#soft)"><g transform="{place}">{outline()}</g></g>')


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
    # the Controls menu's controller (128x128, eight times larger: it is drawn large) and its glow (64x64)
    pngs['pad'] = render('pad', svg(512, 512, controller(), 2))
    pngs['glow'] = render('pad_glow', svg(256, 256, glow()))
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
