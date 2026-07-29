#!/usr/bin/env python3
"""Genera los assets SVG rosados de Miss Yera para el README.

Correlo con `python3 assets/generar-assets.py` cada vez que quieras cambiar
un texto, una cifra o un color: reescribe los SVG generados dentro de assets/.
Los SVG hechos a mano (logo, pollito, banner, facetas, sobre-mi, sec-*) no se tocan.
"""
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Paleta Miss Yera
BLUSH   = "#FFF5FA"
PETAL   = "#FFE9F5"
ROSE    = "#FFC2E0"
FLAMINGO= "#FF8FC8"
HOT     = "#FF69B4"
MAGENTA = "#E0218A"
LILAC   = "#DDA0DD"
NAVY    = "#1D334A"
SNOW    = "#FFFBFD"

FONT = "Trebuchet MS, Segoe UI, Verdana, sans-serif"

BOW = ('<path d="M-6 6 q-4 20 -14 30 q8 -2 12 -8 q2 12 6 16 q4 -14 2 -34 z" fill="{c}" opacity="0.95"/>'
       '<path d="M6 6 q4 20 14 30 q-8 -2 -12 -8 q-2 12 -6 16 q-4 -14 -2 -34 z" fill="{c}" opacity="0.95"/>'
       '<path d="M0 0 c-10 -15 -30 -12 -30 2 c0 11 10 15 15 18 c-2 -8 0 -14 15 -20 z" fill="{c}"/>'
       '<path d="M4 -2 c10 -15 30 -12 30 2 c0 11 -10 15 -15 18 c2 -8 0 -14 -15 -20 z" fill="{c}"/>'
       '<ellipse cx="1" cy="3" rx="8" ry="7" fill="{d}"/>')

HEART = ('<path d="M0 0 c-6 -8 -18 -5 -18 4 c0 8 10 14 18 19 c8 -5 18 -11 18 -19 c0 -9 -12 -12 -18 -4 z" '
         'fill="{c}" opacity="{o}"/>')

SPARK = '<path d="M0 0 l3 -10 l3 10 l10 3 l-10 3 l-3 10 l-3 -10 l-10 -3 z" fill="{c}" opacity="{o}"/>'


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("  ->", name, len(body), "bytes")


# ---------------------------------------------------------------- iconos 24x24
def gear(c, d):
    teeth = []
    for i in range(8):
        a = math.radians(i * 45)
        x, y = 12 + 9.2 * math.cos(a), 12 + 9.2 * math.sin(a)
        teeth.append(
            f'<rect x="{x-2.1:.1f}" y="{y-2.1:.1f}" width="4.2" height="4.2" rx="1.2" '
            f'fill="{c}" transform="rotate({i*45} {x:.1f} {y:.1f})"/>')
    return ("".join(teeth) +
            f'<circle cx="12" cy="12" r="7" fill="{c}"/>'
            f'<circle cx="12" cy="12" r="3.1" fill="{d}"/>')


ICONS = {
    "cerebro": lambda c, d: (
        f'<path d="M11 4.4a3.2 3.2 0 0 0-5 2 3 3 0 0 0-1.4 4.6A3.2 3.2 0 0 0 6 16.4a3.2 3.2 0 0 0 5 2.6z" '
        f'fill="{c}"/>'
        f'<path d="M13 4.4a3.2 3.2 0 0 1 5 2 3 3 0 0 1 1.4 4.6A3.2 3.2 0 0 1 18 16.4a3.2 3.2 0 0 1-5 2.6z" '
        f'fill="{c}" opacity="0.78"/>'
        f'<g stroke="{d}" fill="none" stroke-width="1.35" stroke-linecap="round">'
        f'<path d="M12 5.6v12.8"/>'
        f'<path d="M9.4 7.6c-1.7.5-2.3 2.1-1.4 3.4"/><path d="M8.6 13c-1.4.6-1.8 2.1-1 3.2"/>'
        f'<path d="M14.6 7.6c1.7.5 2.3 2.1 1.4 3.4"/><path d="M15.4 13c1.4.6 1.8 2.1 1 3.2"/>'
        f'</g>'),
    "engranaje": gear,
    "robot": lambda c, d: (
        f'<rect x="4" y="8" width="16" height="12" rx="4" fill="{c}"/>'
        f'<circle cx="9" cy="14" r="2" fill="{d}"/><circle cx="15" cy="14" r="2" fill="{d}"/>'
        f'<path d="M12 8V4.6" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="12" cy="3" r="2.2" fill="{c}"/>'
        f'<path d="M2.4 12.5v3M21.6 12.5v3" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'),
    "grafico": lambda c, d: (
        f'<rect x="3.5" y="13" width="4.4" height="8" rx="1.6" fill="{c}" opacity="0.68"/>'
        f'<rect x="9.8" y="8.5" width="4.4" height="12.5" rx="1.6" fill="{c}"/>'
        f'<rect x="16.1" y="4" width="4.4" height="17" rx="1.6" fill="{c}" opacity="0.85"/>'),
    "birrete": lambda c, d: (
        f'<path d="M12 3.4 22.4 8.4 12 13.4 1.6 8.4z" fill="{c}"/>'
        f'<path d="M6 10.6v4.6c0 1.7 2.7 3.2 6 3.2s6-1.5 6-3.2v-4.6" fill="none" stroke="{c}" '
        f'stroke-width="2.2" stroke-linecap="round"/>'
        f'<path d="M21.4 9v6" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'
        f'<circle cx="21.4" cy="16" r="1.7" fill="{c}"/>'),
    "micro": lambda c, d: (
        f'<rect x="9" y="2.4" width="6" height="11.2" rx="3" fill="{c}"/>'
        f'<path d="M5.6 11.4a6.4 6.4 0 0 0 12.8 0" fill="none" stroke="{c}" stroke-width="2.2" '
        f'stroke-linecap="round"/>'
        f'<path d="M12 17.8v3.4M8.6 21.2h6.8" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>'),
    "camara": lambda c, d: (
        f'<path d="M9.4 5.2h5.2l1.2 2.2H8.2z" fill="{c}"/>'
        f'<rect x="2.4" y="7" width="19.2" height="13" rx="3.4" fill="{c}"/>'
        f'<circle cx="12" cy="13.5" r="4.4" fill="{d}"/><circle cx="12" cy="13.5" r="2.1" fill="{c}"/>'),
    "globo": lambda c, d: (
        f'<circle cx="12" cy="12" r="9.2" fill="{c}"/>'
        f'<ellipse cx="12" cy="12" rx="4" ry="9.2" fill="none" stroke="{d}" stroke-width="1.4"/>'
        f'<path d="M3.2 9.2h17.6M3.2 14.8h17.6" stroke="{d}" stroke-width="1.4"/>'),
    "cohete": lambda c, d: (
        f'<path d="M12 2.2c3.4 2.6 5.2 6.4 5.2 10.4L12 17 6.8 12.6c0-4 1.8-7.8 5.2-10.4z" fill="{c}"/>'
        f'<circle cx="12" cy="9.4" r="2.2" fill="{d}"/>'
        f'<path d="M6.8 12.6 4 16.4l3.8-.8zM17.2 12.6 20 16.4l-3.8-.8z" fill="{c}" opacity="0.75"/>'
        f'<path d="M10.4 18.2c.6 2 1.6 3.4 1.6 3.4s1-1.4 1.6-3.4z" fill="{c}" opacity="0.6"/>'),
    "cv": lambda c, d: (
        f'<rect x="4.4" y="2.6" width="15.2" height="18.8" rx="3" fill="{c}"/>'
        f'<circle cx="12" cy="9" r="2.7" fill="{d}"/>'
        f'<path d="M7.6 16.6c0-2.4 2-3.8 4.4-3.8s4.4 1.4 4.4 3.8z" fill="{d}"/>'
        f'<path d="M8 19.2h8" stroke="{d}" stroke-width="1.5" stroke-linecap="round"/>'),
    "pluma": lambda c, d: (
        f'<path d="M20.4 3.4C13.8 4 8.4 7 6.4 13.2c-.7 2.1-.7 4-.5 5.3 1.2-2.9 3.2-5.2 6.6-6.9'
        f'-2.4 1.9-4.2 4.3-5.1 7.4 5.8.6 10.2-2.4 11.9-7.6.9-2.7 1.1-5.6 1.1-8z" fill="{c}"/>'
        f'<path d="M6 21.4c.4-1.6 1-3 1.8-4.3" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'),
    "regalo": lambda c, d: (
        f'<rect x="2.8" y="9.6" width="18.4" height="11.6" rx="2.6" fill="{c}"/>'
        f'<rect x="1.8" y="6" width="20.4" height="4.6" rx="2" fill="{c}" opacity="0.8"/>'
        f'<path d="M12 6v15.2" stroke="{d}" stroke-width="2.2"/>'
        f'<path d="M12 6C10.4 2.4 5.6 2.6 6.4 5.4 6.9 7 9.6 6.4 12 6zM12 6c1.6-3.6 6.4-3.4 5.6-.6'
        f'-.5 1.6-3.2 1-5.6.6z" fill="{c}"/>'),
}


# ---------------------------------------------------------------- tarjetas
def card(icon, title, lines, accent=HOT, deep=MAGENTA, w=340, h=220):
    """Tarjeta rosada con icono, titulo y descripcion."""
    tspans = "".join(
        f'<tspan x="30" dy="{0 if i == 0 else 23}">{ln}</tspan>' for i, ln in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.8" y2="1">
<stop offset="0%" stop-color="{SNOW}"/><stop offset="55%" stop-color="{BLUSH}"/><stop offset="100%" stop-color="{PETAL}"/>
</linearGradient>
<linearGradient id="ic" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{accent}"/><stop offset="100%" stop-color="{deep}"/>
</linearGradient>
<style>
.fl{{animation:fl 4s ease-in-out infinite;transform-origin:{w-46}px 40px}}
@keyframes fl{{0%,100%{{transform:translateY(0) rotate(-4deg)}}50%{{transform:translateY(-5px) rotate(4deg)}}}}
.tw{{animation:tw 2.8s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.35;transform:scale(.8)}}50%{{opacity:1;transform:scale(1.08)}}}}
</style>
</defs>
<rect x="5" y="5" width="{w-10}" height="{h-10}" rx="26" fill="url(#bg)" stroke="{accent}" stroke-width="3.4"/>
<rect x="5" y="5" width="{w-10}" height="{h-10}" rx="26" fill="none" stroke="{SNOW}" stroke-width="1.2" opacity="0.9"/>
<path d="M31 5h{w-62}" stroke="{deep}" stroke-width="4" stroke-linecap="round" opacity="0.35"/>
<g transform="translate(30,28)">
<rect width="58" height="58" rx="19" fill="url(#ic)"/>
<g transform="translate(8,8) scale(1.75)">{ICONS[icon](SNOW, accent)}</g>
</g>
<text x="30" y="126" font-family="{FONT}" font-size="25" font-weight="bold" font-style="italic" fill="{deep}">{title}</text>
<text x="30" y="157" font-family="{FONT}" font-size="16" fill="{NAVY}">{tspans}</text>
<g class="fl"><g transform="translate({w-46},32) scale(0.62)">{HEART.format(c=accent, o="0.55")}</g></g>
<g class="tw" style="transform-origin:{w-40}px {h-34}px"><g transform="translate({w-40},{h-42}) scale(0.62)">{SPARK.format(c=deep, o="0.7")}</g></g>
<g transform="translate(30,{h-24}) scale(0.42)">{BOW.format(c=accent, d=deep)}</g>
</svg>'''


# ---------------------------------------------------------------- separadores
def sep_corazones():
    hearts = []
    for i in range(19):
        x = 40 + i * 46
        col = [HOT, ROSE, FLAMINGO, LILAC][i % 4]
        sc = 0.5 if i % 2 else 0.66
        hearts.append(f'<g transform="translate({x},34) scale({sc})">{HEART.format(c=col, o="0.9")}</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 70" width="900" height="70">
<style>
.beat{{animation:beat 2.4s ease-in-out infinite}}
.beat2{{animation:beat 2.4s ease-in-out 1.2s infinite}}
@keyframes beat{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
.osc{{animation:osc 3.4s ease-in-out infinite;transform-origin:450px 30px}}
@keyframes osc{{0%,100%{{transform:rotate(-6deg)}}50%{{transform:rotate(6deg)}}}}
</style>
<path d="M20 35h860" stroke="{ROSE}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="2 12" opacity="0.85"/>
<g class="beat">{"".join(hearts[::2])}</g>
<g class="beat2">{"".join(hearts[1::2])}</g>
<g class="osc"><g transform="translate(450,22) scale(1.05)">{BOW.format(c=HOT, d=MAGENTA)}</g></g>
</svg>'''


# ---------------------------------------------------------------- cabeceras
def seccion(titulo, emoji_hint=None, w=900, h=110):
    """Cabecera de seccion en el mismo estilo que las sec-*.svg existentes."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{PETAL}"/><stop offset="55%" stop-color="{ROSE}"/><stop offset="100%" stop-color="{FLAMINGO}"/></linearGradient>
<style>.b{{animation:b 2.6s ease-in-out infinite}}.b2{{animation:b 2.6s ease-in-out 1.3s infinite}}
@keyframes b{{0%,100%{{opacity:.3;transform:scale(.85)}}50%{{opacity:1;transform:scale(1.1)}}}}
.sw{{animation:sw 3.4s ease-in-out infinite;transform-origin:78px 55px}}@keyframes sw{{0%,100%{{transform:rotate(-6deg)}}50%{{transform:rotate(6deg)}}}}</style></defs>
<g transform="translate(0,8)"><path d="{_scallop()}" fill="url(#g)" stroke="{ROSE}" stroke-width="3"/></g>
{_pearls()}
<g class="sw"><g transform="translate(80,52) scale(0.9)">{BOW.format(c=HOT, d=MAGENTA)}</g></g>
<text x="474" y="67" text-anchor="middle" font-family="{FONT}" font-size="36" font-style="italic" font-weight="bold" fill="{MAGENTA}">{titulo}</text>
<g class="b" style="transform-origin:805px 49px"><g transform="translate(805,41) scale(1)">{SPARK.format(c="#FFFFFF", o="0.95")}</g></g>
<g class="b2" style="transform-origin:842px 65px"><g transform="translate(842,59) scale(0.8)">{SPARK.format(c=MAGENTA, o="0.8")}</g></g>
<g transform="translate(760,39) scale(0.8)">{HEART.format(c=HOT, o="0.5")}</g>
</svg>'''


def _scallop():
    top = "M14 14 " + "a14 14 0 0 1 28 0 " * 31
    bottom = "L882 80 " + "a14 14 0 0 1 -28 0 " * 31
    return top + bottom + "Z"


def _pearls():
    return "".join(
        f'<circle cx="{60 + i*26}" cy="89" r="4" fill="{SNOW}" stroke="{ROSE}" stroke-width="1.6"/>'
        for i in range(30))


# ---------------------------------------------------------------- banda de cifras
def cifras(tiles, w=900, h=200):
    """Tarjetas de cifras. Sin animar la opacidad del bloque entero: eso apagaba
    los numeros. Solo parpadean los brillitos decorativos."""
    cw = (w - 40) / len(tiles)
    cells = []
    for i, (num, l1, l2) in enumerate(tiles):
        x0 = 20 + cw * i + 8
        tw = cw - 16
        cx = x0 + tw / 2
        accent = [MAGENTA, HOT, MAGENTA, HOT][i % 4]
        cells.append(f'''
<g>
<rect x="{x0:.1f}" y="18" width="{tw:.1f}" height="{h-42}" rx="26" fill="url(#tile)" stroke="{accent}" stroke-width="3.2"/>
<path d="M{x0+26:.1f} 18h{tw-52:.1f}" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>
<text x="{cx:.1f}" y="84" text-anchor="middle" font-family="{FONT}" font-size="42" font-weight="bold" fill="{accent}">{num}</text>
<text x="{cx:.1f}" y="114" text-anchor="middle" font-family="{FONT}" font-size="15.5" font-weight="bold" fill="{NAVY}">{l1}</text>
<text x="{cx:.1f}" y="136" text-anchor="middle" font-family="{FONT}" font-size="13.5" fill="{NAVY}" opacity="0.78">{l2}</text>
<g class="tw{i % 2}" style="transform-origin:{x0+tw-26:.1f}px 42px"><g transform="translate({x0+tw-26:.1f},36) scale(0.5)">{SPARK.format(c=accent, o="0.75")}</g></g>
<g transform="translate({cx:.1f},{h-42}) scale(0.36)">{BOW.format(c=accent, d=MAGENTA)}</g>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="tile" x1="0" y1="0" x2="0.4" y2="1">
<stop offset="0%" stop-color="{SNOW}"/><stop offset="60%" stop-color="{BLUSH}"/><stop offset="100%" stop-color="{PETAL}"/></linearGradient>
<style>
.tw0{{animation:tw 2.8s ease-in-out infinite}}.tw1{{animation:tw 2.8s ease-in-out 1.4s infinite}}
@keyframes tw{{0%,100%{{opacity:.3;transform:scale(.8)}}50%{{opacity:1;transform:scale(1.1)}}}}
</style></defs>
{"".join(cells)}
</svg>'''


# ---------------------------------------------------------------- logos de redes
# Marcas simplificadas, dibujadas en la paleta Miss Yera. Caja de 24x24.
LOGOS = {
    "tiktok": lambda c, d: (
        f'<path d="M14.2 3h3.1c.2 1.6 1 3 2.3 3.9 .8.5 1.7.9 2.6 1v3.1c-1.7-.1-3.3-.6-4.7-1.5v6.6'
        f'c0 1.5-.5 3-1.5 4.1-1.5 1.8-4 2.5-6.2 1.8-2.4-.7-4.1-2.9-4.2-5.4-.1-2.7 1.8-5.2 4.4-5.8'
        f'.9-.2 1.8-.2 2.7 0v3.2c-1.4-.5-3 .2-3.5 1.6-.5 1.3.1 2.9 1.4 3.5 1.4.6 3.1 0 3.6-1.5'
        f'.1-.4.2-.8.2-1.2V3z" fill="{c}"/>'),
    "instagram": lambda c, d: (
        f'<rect x="2.6" y="2.6" width="18.8" height="18.8" rx="6" fill="none" stroke="{c}" stroke-width="2.4"/>'
        f'<circle cx="12" cy="12" r="4.6" fill="none" stroke="{c}" stroke-width="2.4"/>'
        f'<circle cx="17.6" cy="6.4" r="1.5" fill="{c}"/>'),
    "youtube": lambda c, d: (
        f'<rect x="1.6" y="5" width="20.8" height="14" rx="4.6" fill="{c}"/>'
        f'<path d="M10 8.8 16 12l-6 3.2z" fill="{d}"/>'),
    "linkedin": lambda c, d: (
        f'<rect x="2.6" y="2.6" width="18.8" height="18.8" rx="4.6" fill="{c}"/>'
        f'<circle cx="7.4" cy="7.6" r="1.8" fill="{d}"/>'
        f'<rect x="5.9" y="10.4" width="3" height="8" fill="{d}"/>'
        f'<path d="M11.4 18.4v-8h2.9v1.1c.6-.9 1.6-1.4 2.7-1.3 2 0 3.2 1.3 3.2 3.7v4.5h-3v-4c0-1.1-.4-1.8-1.4-1.8'
        f'-.9 0-1.4.6-1.4 1.8v4z" fill="{d}"/>'),
    "x": lambda c, d: (
        f'<path d="M3.2 3h5.4l4.2 5.7L17.9 3h2.9l-6.5 7.6L21.4 21H16l-4.5-6.1L6 21H3.1l7-8.1z" fill="{c}"/>'),
    "web": lambda c, d: (
        f'<circle cx="12" cy="12" r="9.4" fill="none" stroke="{c}" stroke-width="2.2"/>'
        f'<ellipse cx="12" cy="12" rx="4.2" ry="9.4" fill="none" stroke="{c}" stroke-width="2.2"/>'
        f'<path d="M2.8 9h18.4M2.8 15h18.4" stroke="{c}" stroke-width="2.2"/>'),
}


def chip_red(logo, red, handle, accent=HOT, w=340, h=104):
    """Chip que va debajo de cada foto en la seccion de redes."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.7" y2="1">
<stop offset="0%" stop-color="{SNOW}"/><stop offset="60%" stop-color="{BLUSH}"/><stop offset="100%" stop-color="{PETAL}"/></linearGradient>
<linearGradient id="ic" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{accent}"/><stop offset="100%" stop-color="{MAGENTA}"/></linearGradient>
<style>.tw{{animation:tw 2.8s ease-in-out infinite;transform-origin:{w-26}px 26px}}
@keyframes tw{{0%,100%{{opacity:.3;transform:scale(.8)}}50%{{opacity:1;transform:scale(1.1)}}}}</style>
</defs>
<rect x="4" y="4" width="{w-8}" height="{h-8}" rx="24" fill="url(#bg)" stroke="{accent}" stroke-width="3.2"/>
<g transform="translate(22,{(h-54)//2})">
<rect width="54" height="54" rx="18" fill="url(#ic)"/>
<g transform="translate(9,9) scale(1.5)">{{glifo}}</g>
</g>
<text x="90" y="{h//2-4}" font-family="{FONT}" font-size="15" font-weight="bold" fill="{NAVY}" opacity="0.75">{red}</text>
<text x="90" y="{h//2+22}" font-family="{FONT}" font-size="21" font-weight="bold" font-style="italic" fill="{MAGENTA}">{handle}</text>
<g class="tw"><g transform="translate({w-26},20) scale(0.46)">{SPARK.format(c=accent, o="0.8")}</g></g>
</svg>'''.replace("{glifo}", LOGOS[logo](SNOW, accent))


# ---------------------------------------------------------------- boton de calendario
def boton_calendario(edicion, accent=MAGENTA, w=340, h=124):
    """Boton bajo la portada de cada calendario."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.6" y2="1">
<stop offset="0%" stop-color="{accent}"/><stop offset="100%" stop-color="{HOT}"/></linearGradient>
<style>.bob{{animation:bob 3.2s ease-in-out infinite;transform-origin:{w-40}px 62px}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}</style>
</defs>
<rect x="4" y="4" width="{w-8}" height="{h-8}" rx="26" fill="url(#bg)"/>
<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="20" fill="none" stroke="{SNOW}" stroke-width="2" opacity="0.75"/>
<text x="{w/2}" y="46" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="bold" fill="{PETAL}">CALENDARIO 2026</text>
<text x="{w/2}" y="78" text-anchor="middle" font-family="{FONT}" font-size="27" font-weight="bold" font-style="italic" fill="{SNOW}">{edicion}</text>
<text x="{w/2}" y="104" text-anchor="middle" font-family="{FONT}" font-size="16" fill="{PETAL}">descárgalo gratis</text>
<g class="bob"><g transform="translate({w-40},50) scale(0.42)">{HEART.format(c=SNOW, o="0.9")}</g></g>
<g transform="translate(40,50) scale(0.42)">{HEART.format(c=SNOW, o="0.9")}</g>
</svg>'''


# ---------------------------------------------------------------- ruta de trabajo
def ruta(pasos, w=900, h=250):
    """Los cuatro pasos de un proyecto, en burbujas unidas por una linea punteada."""
    cw = w / len(pasos)
    nodos, etiquetas = [], []
    for i, (titulo, l1, l2) in enumerate(pasos):
        cx = cw * i + cw / 2
        accent = [MAGENTA, HOT, FLAMINGO, MAGENTA][i % 4]
        nodos.append(f'''
<g class="bob{i % 2}" style="transform-origin:{cx:.1f}px 74px">
<circle cx="{cx:.1f}" cy="74" r="42" fill="{SNOW}" stroke="{accent}" stroke-width="4"/>
<circle cx="{cx:.1f}" cy="74" r="34" fill="url(#paso)" opacity="0.55"/>
<text x="{cx:.1f}" y="90" text-anchor="middle" font-family="{FONT}" font-size="40" font-weight="bold" fill="{accent}">{i+1}</text>
</g>''')
        etiquetas.append(f'''
<text x="{cx:.1f}" y="148" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="bold" font-style="italic" fill="{accent}">{titulo}</text>
<text x="{cx:.1f}" y="176" text-anchor="middle" font-family="{FONT}" font-size="14.5" fill="{NAVY}">{l1}</text>
<text x="{cx:.1f}" y="196" text-anchor="middle" font-family="{FONT}" font-size="14.5" fill="{NAVY}">{l2}</text>
<g transform="translate({cx:.1f},212) scale(0.32)">{BOW.format(c=accent, d=MAGENTA)}</g>''')
    linea = (f'<path d="M{cw/2:.0f} 74H{w - cw/2:.0f}" stroke="{ROSE}" stroke-width="5" '
             f'stroke-linecap="round" stroke-dasharray="3 16"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="paso" x1="0" y1="0" x2="0.6" y2="1">
<stop offset="0%" stop-color="{BLUSH}"/><stop offset="100%" stop-color="{ROSE}"/></linearGradient>
<style>
.bob0{{animation:bob 3.6s ease-in-out infinite}}.bob1{{animation:bob 3.6s ease-in-out 1.8s infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
</style></defs>
{linea}
{"".join(nodos)}
{"".join(etiquetas)}
</svg>'''


# ---------------------------------------------------------------- cierre
def cierre(w=900, h=260):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<linearGradient id="c" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="{PETAL}"/><stop offset="50%" stop-color="{ROSE}"/><stop offset="100%" stop-color="{FLAMINGO}"/></linearGradient>
<linearGradient id="in" x1="0" y1="0" x2="0.3" y2="1">
<stop offset="0%" stop-color="{SNOW}"/><stop offset="100%" stop-color="{BLUSH}"/></linearGradient>
<style>
.fl{{animation:fl 5s ease-in-out infinite}}@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
.tw{{animation:tw 2.6s ease-in-out infinite}}.tw2{{animation:tw 2.6s ease-in-out 1.3s infinite}}
@keyframes tw{{0%,100%{{opacity:.25;transform:scale(.8)}}50%{{opacity:1;transform:scale(1.12)}}}}
</style>
</defs>
<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="40" fill="url(#c)"/>
<rect x="24" y="24" width="{w-48}" height="{h-48}" rx="30" fill="url(#in)" stroke="{SNOW}" stroke-width="3"/>
<text x="{w/2}" y="94" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="bold" font-style="italic" fill="{MAGENTA}">Tu empresa ya tiene los datos.</text>
<text x="{w/2}" y="136" text-anchor="middle" font-family="{FONT}" font-size="34" font-weight="bold" font-style="italic" fill="{HOT}">Yo pongo la inteligencia y el brillo.</text>
<text x="{w/2}" y="180" text-anchor="middle" font-family="{FONT}" font-size="19" fill="{NAVY}">Consultoría, automatización y capacitación en IA, sin jerga y con humor.</text>
<text x="{w/2}" y="212" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="bold" fill="{MAGENTA}">missyera.com</text>
<g class="fl"><g transform="translate(96,120) scale(1.1)">{BOW.format(c=HOT, d=MAGENTA)}</g></g>
<g class="fl"><g transform="translate({w-96},120) scale(1.1)">{BOW.format(c=HOT, d=MAGENTA)}</g></g>
<g class="tw" style="transform-origin:64px 60px"><g transform="translate(64,52)">{SPARK.format(c=SNOW, o="0.95")}</g></g>
<g class="tw2" style="transform-origin:{w-64}px 60px"><g transform="translate({w-64},52)">{SPARK.format(c=SNOW, o="0.95")}</g></g>
<g class="tw2" style="transform-origin:64px {h-56}px"><g transform="translate(64,{h-64}) scale(0.8)">{SPARK.format(c=MAGENTA, o="0.7")}</g></g>
<g class="tw" style="transform-origin:{w-64}px {h-56}px"><g transform="translate({w-64},{h-64}) scale(0.8)">{SPARK.format(c=MAGENTA, o="0.7")}</g></g>
</svg>'''


# ---------------------------------------------------------------- marco de foto
def marco(titulo, w=900, h=64):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{PETAL}"/><stop offset="50%" stop-color="{ROSE}"/><stop offset="100%" stop-color="{PETAL}"/></linearGradient></defs>
<rect x="4" y="10" width="{w-8}" height="{h-20}" rx="22" fill="url(#m)" stroke="{FLAMINGO}" stroke-width="2.6"/>
<text x="{w/2}" y="{h/2+8}" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="bold" font-style="italic" fill="{MAGENTA}">{titulo}</text>
<g transform="translate(46,{h/2-8}) scale(0.42)">{BOW.format(c=HOT, d=MAGENTA)}</g>
<g transform="translate({w-46},{h/2-8}) scale(0.42)">{BOW.format(c=HOT, d=MAGENTA)}</g>
</svg>'''


if __name__ == "__main__":
    print("cabeceras de seccion")
    write("sec-impacto.svg", seccion("Mi impacto en números"))
    write("sec-como.svg", seccion("Cómo trabajamos juntas"))
    write("sec-servicios.svg", seccion("Lo que hago por tu empresa"))

    print("separador")
    write("sep-corazones.svg", sep_corazones())

    print("cifras")
    write("banda-cifras.svg", cifras([
        ("+200 mil", "pollitos y pollitas", "ya aprendieron conmigo"),
        ("13", "años de experiencia", "convirtiendo datos en valor"),
        ("+40 mil", "CVs analizados", "gratis con MissCV"),
        ("0", "líneas de código", "que necesitas saber"),
    ]))

    print("tarjetas de servicio")
    servicios = [
        ("card-consultoria.svg",   "cerebro",   "Consultoría en IA",   ["Diagnóstico, quick wins y hoja de", "ruta de IA hecha para tu empresa."], HOT,      MAGENTA),
        ("card-automatizacion.svg","engranaje", "Automatización",      ["Adiós tareas repetitivas, hola", "reportes y flujos inteligentes."],      FLAMINGO, MAGENTA),
        ("card-agentes.svg",       "robot",     "Agentes de IA",       ["Asistentes virtuales que trabajan", "mientras tú duermes."],              LILAC,    MAGENTA),
        ("card-predictivo.svg",    "grafico",   "Análisis predictivo", ["Dashboards y modelos que vuelven", "tu data en decisiones."],            MAGENTA,  MAGENTA),
        ("card-capacitacion.svg",  "birrete",   "Capacitación en IA",  ["Tu equipo aprende haciendo, con", "casos reales de su industria."],      HOT,      MAGENTA),
        ("card-speaker.svg",       "micro",     "Speaker y keynotes",  ["Charlas que hacen que la IA", "parezca fácil y hasta divertida."],       FLAMINGO, MAGENTA),
        ("card-modelo.svg",        "camara",    "Modelo y anfitriona", ["Campañas, editoriales y eventos", "con mi signature look pelirroja."],   LILAC,    MAGENTA),
    ]
    for name, ic, t, ls, a, d in servicios:
        write(name, card(ic, t, ls, a, d))

    print("tarjetas de ecosistema")
    eco = [
        ("eco-web.svg",      "globo",  "missyera.com",   ["Mi casa digital: consultoría,", "cursos, blog y recursos gratis."], MAGENTA,  MAGENTA),
        ("eco-fullday.svg",  "cohete", "Full Day de IA", ["Aprende IA desde cero en un día,", "15 herramientas sin programar."], HOT,      MAGENTA),
        ("eco-misscv.svg",   "cv",     "misscv.com",     ["Crea y analiza tu CV con IA,", "gratis y en minutos."],              FLAMINGO, MAGENTA),
        ("eco-blog.svg",     "pluma",  "El blog",        ["Guías de IA y datos explicadas", "sin tecnicismos."],                LILAC,    MAGENTA),
        ("eco-recursos.svg", "regalo", "Recursos gratis",["Calendarios, guías y plantillas", "de regalo para mis pollitos."],   HOT,      MAGENTA),
    ]
    for name, ic, t, ls, a, d in eco:
        write(name, card(ic, t, ls, a, d))

    print("chips de redes")
    redes = [
        ("chip-tiktok.svg",    "tiktok",    "TikTok",    "@soymissyera", HOT),
        ("chip-instagram.svg", "instagram", "Instagram", "@soymissyera", MAGENTA),
        ("chip-youtube.svg",   "youtube",   "YouTube",   "@soymissyera", HOT),
        ("chip-linkedin.svg",  "linkedin",  "LinkedIn",  "soymissyera",  MAGENTA),
        ("chip-x.svg",         "x",         "X",         "@soymissyera", HOT),
        ("chip-web.svg",       "web",       "Mi web",    "missyera.com", MAGENTA),
    ]
    for name, lg, red, handle, acc in redes:
        write(name, chip_red(lg, red, handle, acc))

    print("botones de calendario")
    write("btn-calendario-1.svg", boton_calendario("Edición 1", MAGENTA))
    write("btn-calendario-2.svg", boton_calendario("Edición 2", HOT))
    write("sec-calendarios.svg", seccion("Mis calendarios 2026"))

    print("ruta de trabajo")
    write("ruta-trabajo.svg", ruta([
        ("Conversamos", "Entiendo tu negocio y", "los dolores de verdad"),
        ("Diagnóstico", "Detecto quick wins y", "priorizo por impacto"),
        ("Implementamos", "Automatizaciones, modelos", "y dashboards que sirven"),
        ("Aprenden", "Capacito a tu equipo para", "que no dependa de mí"),
    ]))

    print("cierre y marcos")
    write("cta-final.svg", cierre())
    write("marco-charlas.svg", marco("La consultora sobre el escenario"))
    write("marco-calendario.svg", marco("La modelo, fotos de mis calendarios 2026"))
    print("listo")
