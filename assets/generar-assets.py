#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los assets del README de Miss Yera en lenguaje editorial rosa.

Correlo con `python3 assets/generar-assets.py` cada vez que quieras cambiar un
texto, una cifra, un tono o un color. Reescribe los SVG generados dentro de
assets/. No toca placa-logo.svg ni pollito.svg, que son piezas de la marca.

La idea del sistema: el rosa tiene rango tonal completo, del nude al borgoña.
Las secciones alternan tonos claros y oscuros para dar ritmo, en vez de un solo
rosa plano en todas partes. Sin negro: hasta el tono más profundo sigue siendo
rosa. El fucsia de la marca queda reservado para acentos, no para fondos.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- el rosa, completo
NUDE       = "#F7E7EC"
BLUSH      = "#F2D9DF"
ROSA_PALO  = "#DCA9B4"
ROSA_VIEJO = "#C17C8C"
FRAMBUESA  = "#9B2F55"
VINO       = "#6E1435"
BORGONA    = "#4A0C24"
HOT        = "#FF69B4"   # el fucsia de la marca, ahora solo como acento
MAGENTA    = "#E0218A"
NIEVE      = "#FFFBFD"

# oro rosa, para filetes y monogramas
ORO = (("0%", "#F6D9C7"), ("32%", "#E3A886"), ("52%", "#F9E8DB"),
       ("74%", "#DFA184"), ("100%", "#EFC3AB"))

SERIF = "Didot, 'Bodoni MT', 'Playfair Display', Georgia, 'Times New Roman', serif"
SANS  = "Trebuchet MS, Segoe UI, Verdana, sans-serif"

# Los lienzos se mantienen angostos a propósito: cuanto más angosto el lienzo,
# menos se encoge el texto cuando GitHub escala la imagen en un móvil.
ANCHO   = 820   # piezas a todo lo ancho
TARJETA = 380   # tarjetas, dos por fila


class Tono:
    """Un escalón del rango tonal, con sus tintas ya resueltas."""

    def __init__(self, nombre, fondo, tinta, suave, acento, filete, oscuro):
        self.nombre, self.fondo, self.tinta = nombre, fondo, tinta
        self.suave, self.acento, self.filete, self.oscuro = suave, acento, filete, oscuro


T_NUDE = Tono("nude",      NUDE,      VINO, ROSA_VIEJO, MAGENTA, ROSA_PALO,  False)
T_FRAM = Tono("frambuesa", FRAMBUESA, NUDE, BLUSH,      HOT,     "url(#oro)", True)
T_VINO = Tono("vino",      VINO,      NUDE, BLUSH,      HOT,     "url(#oro)", True)
T_BORG = Tono("borgona",   BORGONA,   NUDE, BLUSH,      HOT,     "url(#oro)", True)


def escribir(nombre, cuerpo):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as fh:
        fh.write(cuerpo)
    print("  ->", nombre)


# ---------------------------------------------------------------- motivos
def defs_oro():
    paradas = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in ORO)
    return f'<linearGradient id="oro" x1="0" y1="0" x2="1" y2="1">{paradas}</linearGradient>'


def seda(t):
    """Viñeta suave: centro apenas más claro, bordes al tono pleno.

    Antes esto era un degradado diagonal que se leía como una mancha. Una
    viñeta radial da profundidad sin parecer un artefacto de compresión.
    """
    claro = NIEVE if not t.oscuro else FRAMBUESA
    return (f'<radialGradient id="seda" cx="0.5" cy="0.42" r="0.78">'
            f'<stop offset="0%" stop-color="{claro}" stop-opacity="{0.16 if t.oscuro else 0.5}"/>'
            f'<stop offset="70%" stop-color="{claro}" stop-opacity="0"/>'
            f'<stop offset="100%" stop-color="{BORGONA}" stop-opacity="{0.14 if t.oscuro else 0.04}"/>'
            f'</radialGradient>')


def lazo(color, ancho=1.5):
    """El lacito de siempre, pero de línea fina en vez de relleno macizo."""
    return (f'<g fill="none" stroke="{color}" stroke-width="{ancho}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M0 0 C-7 -13 -28 -11 -28 2 C-28 12 -13 12 0 2"/>'
            f'<path d="M0 0 C7 -13 28 -11 28 2 C28 12 13 12 0 2"/>'
            f'<path d="M-3 4 C-7 17 -11 24 -17 31"/>'
            f'<path d="M3 4 C7 17 11 24 17 31"/>'
            f'<ellipse cx="0" cy="1.5" rx="4.6" ry="4"/></g>')


def encaje(x0, x1, y, color, paso=26, alto=9, opacidad=0.9):
    """Borde de encaje: arcos finos con un puntito colgando de cada uno."""
    arcos, puntos = [], []
    x = x0
    while x + paso <= x1:
        arcos.append(f"M{x} {y} q{paso/2} {alto} {paso} 0")
        puntos.append(f'<circle cx="{x + paso/2:.1f}" cy="{y + alto*0.78:.1f}" r="1.5" fill="{color}"/>')
        x += paso
    return (f'<g opacity="{opacidad}"><path d="{" ".join(arcos)}" fill="none" stroke="{color}" '
            f'stroke-width="1.2"/>{"".join(puntos)}</g>')


def monograma(x, y, color, escala=1.0, opacidad=1.0):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="{16*escala:.0f}" letter-spacing="{3.4*escala:.1f}" '
            f'fill="{color}" opacity="{opacidad}">MY</text>')


def rotulo(x, y, texto, color, tam=12, esp=4.4):
    """Rótulo en versalitas espaciadas, el gesto editorial por excelencia."""
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="{tam}" letter-spacing="{esp}" fill="{color}">{texto.upper()}</text>')


def filete(x0, x1, y, t, grosor=1.3):
    return f'<path d="M{x0:.0f} {y:.0f}H{x1:.0f}" stroke="{t.filete}" stroke-width="{grosor}"/>'


def marco_base(w, h, t):
    """Fondo de satén más filete interior: la caja común a todas las piezas."""
    return (f'<rect width="{w}" height="{h}" fill="{t.fondo}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#seda)"/>'
            f'<rect x="13" y="13" width="{w-26}" height="{h-26}" '
            f'fill="none" stroke="{t.filete}" stroke-width="1.3"/>')


def envoltura(w, h, cuerpo, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}"><defs>{defs_oro()}{extra_defs}</defs>{cuerpo}</svg>')


# ---------------------------------------------------------------- cabecera de sección
def seccion(titulo, t, w=ANCHO, h=146):
    c = (marco_base(w, h, t) +
         encaje(40, w - 40, h - 30, t.filete, opacidad=0.5) +
         f'<text x="{w/2}" y="{h/2+20}" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="40" letter-spacing="2.4" fill="{t.tinta}">{titulo}</text>' +
         filete(62, w/2 - 240, h/2 + 8, t) +
         filete(w/2 + 240, w - 62, h/2 + 8, t) +
         f'<g transform="translate({w/2},36) scale(0.5)">{lazo(t.acento, 2.5)}</g>' +
         '')
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- tarjeta
def tarjeta(rotulo_txt, titulo, lineas, t, w=TARJETA, h=252):
    cuerpo = "".join(
        f'<text x="{w/2}" y="{162 + i*28}" text-anchor="middle" font-family="{SANS}" '
        f'font-size="19" fill="{t.tinta}" opacity="0.88">{ln}</text>'
        for i, ln in enumerate(lineas))
    c = (marco_base(w, h, t) +
         rotulo(w/2, 62, rotulo_txt, t.acento, 12.5, 4.2) +
         f'<text x="{w/2}" y="116" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="31" letter-spacing="1.1" fill="{t.tinta}">{titulo}</text>' +
         filete(w/2 - 34, w/2 + 34, 134, t) + cuerpo)
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- banda de cifras
def cifras(datos, w=ANCHO, h=186):
    cw = (w - 52) / len(datos)
    celdas = ""
    for i, (num, etiqueta) in enumerate(datos):
        cx = 26 + cw * i + cw / 2
        if i:
            celdas += (f'<path d="M{26 + cw*i:.1f} 50V{h-50}" stroke="{T_VINO.filete}" '
                       f'stroke-width="1" opacity="0.55"/>')
        celdas += (
            f'<text x="{cx:.1f}" y="104" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="54" fill="{T_VINO.tinta}">{num}</text>'
            + rotulo(cx, 140, etiqueta, T_VINO.suave, 12.5, 2.6))
    c = marco_base(w, h, T_VINO) + celdas
    return envoltura(w, h, c, seda(T_VINO))


# ---------------------------------------------------------------- ruta de trabajo
def ruta(pasos, w=ANCHO, h=244):
    cw = (w - 52) / len(pasos)
    nodos = ""
    for i, (titulo, linea) in enumerate(pasos):
        cx = 26 + cw * i + cw / 2
        nodos += (
            f'<circle cx="{cx:.1f}" cy="88" r="34" fill="none" stroke="{T_NUDE.filete}" stroke-width="1.4"/>'
            f'<circle cx="{cx:.1f}" cy="88" r="27" fill="{NIEVE}" opacity="0.6"/>'
            f'<text x="{cx:.1f}" y="101" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="34" fill="{T_NUDE.tinta}">{i+1}</text>'
            f'<text x="{cx:.1f}" y="162" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="25" letter-spacing="0.8" fill="{T_NUDE.tinta}">{titulo}</text>'
            + rotulo(cx, 196, linea, T_NUDE.suave, 12.5, 2.4))
    c = (marco_base(w, h, T_NUDE) +
         f'<path d="M{26+cw/2:.0f} 88H{w-26-cw/2:.0f}" stroke="{T_NUDE.filete}" '
         f'stroke-width="1.2" stroke-dasharray="1 9"/>' + nodos)
    return envoltura(w, h, c, seda(T_NUDE))



# ---------------------------------------------------------------- iconos de marca
# Glifos dibujados a mano en caja de 24x24, para no depender de shields.io y
# poder teñirlos con la paleta. Trazo abierto salvo donde el logo pide macizo.
GLIFOS = {
    "python": lambda c: (
        f'<g fill="{c}"><path d="M11.9 1.6c-.9 0-1.7.1-2.4.2-2.2.4-2.6 1.2-2.6 2.6v1.9h5.2v.7H4.9'
        f'c-1.5 0-2.8.9-3.2 2.6-.5 1.9-.5 3.1 0 5.1.4 1.5 1.2 2.6 2.7 2.6h1.8v-2.3c0-1.7 1.5-3.2 3.2-3.2'
        f'h5.2c1.4 0 2.6-1.2 2.6-2.6V4.4c0-1.4-1.2-2.4-2.6-2.7-.9-.1-1.8-.2-2.7-.1zM9.1 3.2'
        f'c.5 0 1 .4 1 1s-.4 1-1 1-1-.4-1-1 .4-1 1-1z"/>'
        f'<path d="M18.6 7v2.3c0 1.8-1.5 3.3-3.2 3.3h-5.2c-1.4 0-2.6 1.2-2.6 2.6v4.9c0 1.4 1.2 2.2 2.6 2.6'
        f'1.6.5 3.2.6 5.2 0 1.3-.4 2.6-1.1 2.6-2.6v-1.9h-5.2v-.7h7.8c1.5 0 2.1-1.1 2.6-2.6.5-1.6.5-3.1 0-5.1'
        f'-.4-1.5-1.1-2.6-2.6-2.6h-2zm-2.9 12.6c.5 0 1 .4 1 1s-.4 1-1 1-1-.4-1-1 .4-1 1-1z" opacity="0.62"/></g>'),
    "sql": lambda c: (
        f'<g fill="none" stroke="{c}" stroke-width="1.9">'
        f'<ellipse cx="12" cy="5.6" rx="7.6" ry="3.1"/>'
        f'<path d="M4.4 5.6v12.8c0 1.7 3.4 3.1 7.6 3.1s7.6-1.4 7.6-3.1V5.6"/>'
        f'<path d="M4.4 12c0 1.7 3.4 3.1 7.6 3.1s7.6-1.4 7.6-3.1"/></g>'),
    "powerbi": lambda c: (
        f'<rect x="3.4" y="13" width="4.6" height="8.2" rx="1.2" fill="{c}" opacity="0.6"/>'
        f'<rect x="9.7" y="7.6" width="4.6" height="13.6" rx="1.2" fill="{c}" opacity="0.82"/>'
        f'<rect x="16" y="2.8" width="4.6" height="18.4" rx="1.2" fill="{c}"/>'),
    "excel": lambda c: (
        f'<g fill="none" stroke="{c}" stroke-width="1.8">'
        f'<rect x="3" y="4" width="18" height="16" rx="2.4"/>'
        f'<path d="M3 9.2h18M3 14.6h18M9.4 4v16M15.2 4v16"/></g>'
        f'<rect x="3" y="4" width="18" height="5.2" rx="2.4" fill="{c}" opacity="0.35"/>'),
    "ml": lambda c: (
        f'<g stroke="{c}" stroke-width="1.4" opacity="0.7">'
        f'<path d="M5 6.4 12 7.4M5 6.4 12 16.6M5 17.6 12 7.4M5 17.6 12 16.6M12 7.4 19 12M12 16.6 19 12"/></g>'
        f'<g fill="{c}"><circle cx="4.6" cy="6.4" r="2.3"/><circle cx="4.6" cy="17.6" r="2.3"/>'
        f'<circle cx="12" cy="7.4" r="2.3"/><circle cx="12" cy="16.6" r="2.3"/>'
        f'<circle cx="19.4" cy="12" r="2.3"/></g>'),
    "ia": lambda c: (
        f'<path d="M12 1.8 14 9.2 21.4 11.2 14 13.2 12 20.6 10 13.2 2.6 11.2 10 9.2z" fill="{c}"/>'
        f'<path d="M19 16.4 19.8 19 22.4 19.8 19.8 20.6 19 23.2 18.2 20.6 15.6 19.8 18.2 19z" '
        f'fill="{c}" opacity="0.7"/>'),
    "claude": lambda c: (
        f'<g stroke="{c}" stroke-width="2.1" stroke-linecap="round">'
        f'<path d="M12 3.2v17.6M4.4 7.6l15.2 8.8M19.6 7.6 4.4 16.4"/></g>'),
    "git": lambda c: (
        f'<g stroke="{c}" stroke-width="1.9" fill="none">'
        f'<path d="M6.4 8.6v7.6"/><path d="M6.4 12.4h5.2a2.6 2.6 0 0 0 2.6-2.6V8.4"/></g>'
        f'<g fill="{c}"><circle cx="6.4" cy="6" r="2.6"/><circle cx="6.4" cy="18.4" r="2.6"/>'
        f'<circle cx="14.2" cy="6" r="2.6"/></g>'),
    "tiktok": lambda c: (
        f'<path d="M14.2 3h2.9c.2 1.5 1 2.8 2.2 3.6.8.5 1.6.8 2.5.9v2.9c-1.6-.1-3.1-.6-4.4-1.4v6.2'
        f'c0 1.4-.5 2.8-1.4 3.8-1.4 1.7-3.8 2.3-5.8 1.7-2.3-.7-3.9-2.7-4-5.1-.1-2.5 1.7-4.9 4.1-5.4'
        f'.8-.2 1.7-.2 2.5 0v3c-1.3-.5-2.8.2-3.3 1.5-.5 1.2.1 2.7 1.3 3.3 1.3.6 2.9 0 3.4-1.4'
        f'.1-.4.2-.7.2-1.1V3z" fill="{c}"/>'),
    "instagram": lambda c: (
        f'<g fill="none" stroke="{c}" stroke-width="2.1">'
        f'<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.6"/>'
        f'<circle cx="12" cy="12" r="4.5"/></g><circle cx="17.5" cy="6.5" r="1.5" fill="{c}"/>'),
    "youtube": lambda c: (
        f'<rect x="1.8" y="5" width="20.4" height="14" rx="4.4" fill="{c}"/>'
        f'<path d="M10 8.9 15.8 12 10 15.1z" fill="{NIEVE}"/>'),
    "linkedin": lambda c: (
        f'<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="4.4" fill="{c}"/>'
        f'<circle cx="7.4" cy="7.6" r="1.8" fill="{NIEVE}"/>'
        f'<rect x="5.9" y="10.4" width="3" height="8" fill="{NIEVE}"/>'
        f'<path d="M11.4 18.4v-8h2.9v1.1c.6-.9 1.6-1.4 2.7-1.3 2 0 3.2 1.3 3.2 3.7v4.5h-3v-4'
        f'c0-1.1-.4-1.8-1.4-1.8-.9 0-1.4.6-1.4 1.8v4z" fill="{NIEVE}"/>'),
    "x": lambda c: (
        f'<path d="M3.2 3h5.4l4.2 5.7L17.9 3h2.9l-6.5 7.6L21.4 21H16l-4.5-6.1L6 21H3.1l7-8.1z" fill="{c}"/>'),
    "web": lambda c: (
        f'<g fill="none" stroke="{c}" stroke-width="2">'
        f'<circle cx="12" cy="12" r="9.2"/><ellipse cx="12" cy="12" rx="4.1" ry="9.2"/>'
        f'<path d="M3 9h18M3 15h18"/></g>'),
}


def herramientas(filas, w=ANCHO):
    """Muro de herramientas con los logos dibujados, en vez de badges de texto."""
    cols = max(len(f) for f in filas)
    cw = (w - 60) / cols
    alto_fila = 128
    h = 56 + alto_fila * len(filas)
    piezas = ""
    for r, fila in enumerate(filas):
        y = 44 + alto_fila * r
        sobra = (cols - len(fila)) * cw / 2
        for i, (glifo, nombre) in enumerate(fila):
            cx = 30 + sobra + cw * i + cw / 2
            piezas += (f'<g transform="translate({cx-22:.1f},{y}) scale(1.85)">'
                       f'{GLIFOS[glifo](T_VINO.suave)}</g>'
                       + rotulo(cx, y + 76, nombre, T_VINO.tinta, 12.5, 2.4))
    return envoltura(w, h, marco_base(w, h, T_VINO) + piezas, seda(T_VINO))


def boton_cta(rotulo_txt, titulo, t, w=TARJETA, h=124):
    """Botón de llamada a la acción, en el mismo lenguaje que el resto."""
    c = (marco_base(w, h, t) +
         rotulo(w/2, 48, rotulo_txt, t.acento, 12, 4) +
         f'<text x="{w/2}" y="88" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="28" letter-spacing="0.8" fill="{t.tinta}">{titulo}</text>' +
         filete(w/2 - 40, w/2 + 40, 104, t))
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- chip de red
def chip(glifo, red, handle, t, w=TARJETA, h=118):
    c = (marco_base(w, h, t) +
         f'<g transform="translate(34,{h/2-23}) scale(1.9)">{GLIFOS[glifo](t.acento)}</g>'
         f'<text x="104" y="{h/2-6}" font-family="{SANS}" font-size="12.5" '
         f'letter-spacing="4.2" fill="{t.suave}">{red.upper()}</text>'
         f'<text x="104" y="{h/2+28}" font-family="{SERIF}" font-size="27" '
         f'letter-spacing="0.6" fill="{t.tinta}">{handle}</text>')
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- botón
def boton(edicion, t, w=TARJETA, h=128):
    c = (marco_base(w, h, t) +
         rotulo(w/2, 50, "calendario 2026", t.acento, 12.5, 4.2) +
         f'<text x="{w/2}" y="90" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="30" letter-spacing="1" fill="{t.tinta}">{edicion}</text>' +
         rotulo(w/2, 112, "descárgalo gratis", t.suave, 12, 3.2))
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- pie editorial
def pie(texto, t, w=ANCHO, h=72):
    c = (f'<rect width="{w}" height="{h}" fill="{t.fondo}"/>'
         f'<rect width="{w}" height="{h}" fill="url(#seda)"/>' +
         filete(40, w/2 - 250, h/2, t) + filete(w/2 + 250, w - 40, h/2, t) +
         rotulo(w/2, h/2 + 6, texto, t.tinta, 15, 4.6))
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- separador
def separador(t, w=ANCHO, h=64):
    c = (encaje(30, w - 30, h/2 - 2, t.filete if not t.oscuro else ROSA_VIEJO,
                paso=24, alto=8, opacidad=0.9) +
         f'<g transform="translate({w/2},{h/2-18}) scale(0.62)">'
         f'{lazo(t.acento if not t.oscuro else ROSA_VIEJO, 2.1)}</g>')
    # los separadores son lo único sin fondo propio, así que se adaptan al tema
    estilo = ('<style>@media (prefers-color-scheme:dark){'
              f'path,ellipse{{stroke:{ROSA_PALO}}}circle{{fill:{ROSA_PALO}}}'
              '}</style>')
    return envoltura(w, h, c, estilo)


# ---------------------------------------------------------------- bloque de texto
def bloque(titulo, subtitulo, puntos, cita, t, w=ANCHO, h=None, tam_titulo=44):
    h = h or 258 + len(puntos) * 40
    sangria = 70 if w > 500 else 40
    filas = "".join(
        f'{filete(sangria, sangria + 26, 212 + i*40 - 6, t, 1)}'
        f'<text x="{sangria + 42}" y="{212 + i*40}" font-family="{SANS}" font-size="19" '
        f'fill="{t.tinta}" opacity="0.9">{p}</text>'
        for i, p in enumerate(puntos))
    c = (marco_base(w, h, t) +
         f'<g transform="translate({w/2},62) scale(0.7)">{lazo(t.acento, 2.2)}</g>' +
         f'<text x="{w/2}" y="142" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="{tam_titulo}" letter-spacing="1.6" fill="{t.tinta}">{titulo}</text>' +
         rotulo(w/2, 174, subtitulo, t.suave, 12, 3.2) + filas +
         filete(w/2 - 80, w/2 + 80, h - 76, t) +
         f'<text x="{w/2}" y="{h-42}" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="21" font-style="italic" fill="{t.acento}">{cita}</text>')
    return envoltura(w, h, c, seda(t))


# ---------------------------------------------------------------- ficha de modelo
def comp_card(w=ANCHO, h=252):
    """Al estilo de las tarjetas de composición que usan las agencias."""
    datos = [("BASE", "Lima, Perú"), ("ALCANCE", "LATAM y España"),
             ("IDIOMAS", "Español · Inglés"), ("SEÑA", "Pelirroja")]
    cols = ""
    for i, (k, v) in enumerate(datos):
        cx = 26 + (w - 52) / 4 * i + (w - 52) / 8
        if i:
            cols += (f'<path d="M{26 + (w-52)/4*i:.1f} 152V212" stroke="{T_VINO.filete}" '
                     f'stroke-width="1" opacity="0.55"/>')
        cols += (rotulo(cx, 176, k, T_VINO.acento, 11.5, 3.4) +
                 f'<text x="{cx:.1f}" y="204" text-anchor="middle" font-family="{SERIF}" '
                 f'font-size="21" fill="{T_VINO.tinta}">{v}</text>')
    c = (marco_base(w, h, T_VINO) +
         rotulo(w/2, 64, "ficha de modelo", T_VINO.acento, 12.5, 4.6) +
         f'<text x="{w/2}" y="116" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="44" letter-spacing="3" fill="{T_VINO.tinta}">MISS YERA</text>' +
         filete(w/2 - 90, w/2 + 90, 136, T_VINO) + cols +
         monograma(w - 46, h - 26, T_VINO.filete, 0.9, 0.75))
    return envoltura(w, h, c, seda(T_VINO))


# ---------------------------------------------------------------- placa del logotipo
def placa_vino():
    """Deriva la placa en vino desde placa-logo.svg, sin tocar el original.

    El logotipo es un gradiente de fondo (id "g") con las letras en blanco
    encima, así que basta con reemplazar las paradas del gradiente: el
    lettering de la marca queda intacto y encima del vino resalta más.
    """
    base = open(os.path.join(OUT, "placa-logo.svg"), encoding="utf-8").read()
    viejo = ('<stop offset="0%" stop-color="#FF8FC8"/>'
             '<stop offset="50%" stop-color="#FF69B4"/>'
             '<stop offset="100%" stop-color="#E0218A"/>')
    if viejo not in base:
        raise SystemExit("placa-logo.svg cambió: revisar las paradas del gradiente")
    return base.replace(viejo,
                        f'<stop offset="0%" stop-color="{FRAMBUESA}"/>'
                        f'<stop offset="52%" stop-color="{VINO}"/>'
                        f'<stop offset="100%" stop-color="{BORGONA}"/>')


# ---------------------------------------------------------------- cierre
def cierre(w=ANCHO, h=276):
    c = (marco_base(w, h, T_BORG) +
         encaje(46, w - 46, h - 42, T_BORG.filete, opacidad=0.5) +
         f'<g transform="translate({w/2},66) scale(0.78)">{lazo(T_BORG.acento, 2.2)}</g>' +
         f'<text x="{w/2}" y="150" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="36" letter-spacing="1.2" fill="{T_BORG.tinta}">Tu empresa ya tiene los datos.</text>'
         f'<text x="{w/2}" y="196" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="36" font-style="italic" letter-spacing="1.2" fill="{T_BORG.acento}">Yo pongo la inteligencia.</text>' +
         filete(w/2 - 110, w/2 + 110, 220, T_BORG) +
         rotulo(w/2, 248, "missyera.com", T_BORG.tinta, 16, 6))
    return envoltura(w, h, c, seda(T_BORG))


# ---------------------------------------------------------------- banner
def banner(w=ANCHO, h=152):
    c = (marco_base(w, h, T_FRAM) +
         f'<text x="{w/2}" y="78" text-anchor="middle" font-family="{SERIF}" '
         f'font-size="36" letter-spacing="1.4" fill="{T_FRAM.tinta}">Bienvenida a mi rinconcito rosa</text>' +
         filete(w/2 - 120, w/2 + 120, 100, T_FRAM) +
         rotulo(w/2, 126, "datos · inteligencia artificial · mucho cariño", T_FRAM.suave, 12.5, 3.4))
    return envoltura(w, h, c, seda(T_FRAM))


if __name__ == "__main__":
    print("separadores de encaje")
    escribir("sep-encaje-claro.svg", separador(T_NUDE))
    escribir("sep-encaje-oro.svg", separador(T_FRAM))

    print("cabeceras, alternando tono para dar ritmo")
    for nombre, titulo, t in [
        ("sec-facetas.svg",        "Mis dos facetas",        T_FRAM),
        ("sec-servicios.svg",      "Lo que hago por ti",     T_VINO),
        ("sec-como.svg",           "Cómo trabajamos juntas", T_NUDE),
        ("sec-fotos.svg",          "Mi mundo en rosa",       T_FRAM),
        ("sec-calendarios.svg",    "Mis calendarios 2026",   T_VINO),
        ("sec-ecosistema.svg",     "Mi ecosistema",          T_NUDE),
        ("sec-juguetes.svg",       "Mis herramientas",       T_FRAM),
        ("sec-redes.svg",          "Encuéntrame",            T_VINO),
        ("sec-numeros.svg",        "Mis números en GitHub",  T_NUDE),
        ("sec-contribuciones.svg", "Mis contribuciones",     T_FRAM),
        ("sec-viborita.svg",       "La viborita rosa",       T_VINO),
    ]:
        escribir(nombre, seccion(titulo, t))

    print("bloques de texto")
    escribir("sobre-mi.svg", bloque(
        "Hola, soy Yera", "ingeniera industrial con mba · trece años en datos",
        ["Enseño IA, ciencia de datos y análisis con humor y sin jerga",
         "Más de 200 mil pollitos y pollitas ya aprendieron conmigo",
         "Implemento IA, automatizaciones y dashboards con resultados medibles",
         "Speaker en conferencias de tecnología, datos y mujeres en STEM",
         "Modelo y anfitriona, con mi signature look pelirroja",
         "Lima, Perú, con el corazón en toda LATAM"],
        "“No necesitas saber programar, solo necesitas decidirte”", T_NUDE))

    escribir("faceta-consultora.svg", bloque(
        "La consultora", "ia · datos · automatización",
        ["Consultoría en IA", "Automatización", "Análisis predictivo", "Capacitación"],
        "“Tus datos ya saben la respuesta”", T_VINO, w=TARJETA, h=440, tam_titulo=36))
    escribir("faceta-modelo.svg", bloque(
        "La modelo", "campañas · editoriales · eventos",
        ["Campañas y editoriales", "Anfitriona de marca", "Look pelirroja", "Castings"],
        "“La misma que arma los modelos”", T_FRAM, w=TARJETA, h=440, tam_titulo=36))

    escribir("placa-logo-vino.svg", placa_vino())
    escribir("banner-frase.svg", banner())
    escribir("comp-card.svg", comp_card())

    print("cifras y ruta")
    escribir("banda-cifras.svg", cifras([
        ("+200 mil", "pollitos"),
        ("13", "años en datos"),
        ("+40 mil", "CVs analizados"),
        ("0", "líneas de código"),
    ]))
    escribir("ruta-trabajo.svg", ruta([
        ("Conversamos", "tu negocio"),
        ("Diagnóstico", "quick wins"),
        ("Implementamos", "lo que sirve"),
        ("Aprenden", "tu equipo"),
    ]))

    print("tarjetas de servicio")
    for nombre, rot, tit, lns, t in [
        ("card-consultoria.svg",    "consultoría",    "Inteligencia Artificial", ["Diagnóstico, quick wins y hoja", "de ruta para tu empresa."],    T_VINO),
        ("card-automatizacion.svg", "automatización", "Procesos sin fricción",   ["Adiós tareas repetitivas, hola", "flujos que se hacen solos."],  T_NUDE),
        ("card-agentes.svg",        "agentes",        "Asistentes de IA",        ["Trabajan mientras tú duermes,", "responden como tu equipo."],   T_FRAM),
        ("card-predictivo.svg",     "analítica",      "Análisis predictivo",     ["Modelos y dashboards que", "vuelven tu data en decisiones."],  T_NUDE),
        ("card-capacitacion.svg",   "capacitación",   "Tu equipo aprende",       ["Aprenden haciendo, con casos", "reales de su industria."],      T_FRAM),
        ("card-speaker.svg",        "escenario",      "Speaker y keynotes",      ["Charlas que hacen que la IA", "parezca fácil y divertida."],   T_VINO),
        ("card-modelo.svg",         "cámara",         "Modelo y anfitriona",     ["Campañas, editoriales y eventos", "con mi look pelirroja."],    T_FRAM),
    ]:
        escribir(nombre, tarjeta(rot, tit, lns, t))

    print("tarjetas de ecosistema")
    for nombre, rot, tit, lns, t in [
        ("eco-web.svg",      "mi casa digital", "missyera.com",    ["Consultoría, cursos, blog", "y recursos gratis."],       T_VINO),
        ("eco-fullday.svg",  "curso estrella",  "Full Day de IA",  ["Aprende IA desde cero en un", "día, sin programar."],     T_NUDE),
        ("eco-misscv.svg",   "gratis",          "misscv.com",      ["Crea y analiza tu CV con IA", "en minutos."],             T_FRAM),
        ("eco-blog.svg",     "lectura",         "El blog",         ["Guías de IA y datos", "explicadas sin tecnicismos."],    T_NUDE),
        ("eco-recursos.svg", "de regalo",       "Recursos gratis", ["Calendarios, guías y", "plantillas para mis pollitos."], T_VINO),
    ]:
        escribir(nombre, tarjeta(rot, tit, lns, t))

    print("redes y calendarios")
    for nombre, glifo, red, handle, t in [
        ("chip-tiktok.svg",    "tiktok",    "tiktok",    "@soymissyera", T_VINO),
        ("chip-instagram.svg", "instagram", "instagram", "@soymissyera", T_NUDE),
        ("chip-youtube.svg",   "youtube",   "youtube",   "@soymissyera", T_FRAM),
        ("chip-linkedin.svg",  "linkedin",  "linkedin",  "soymissyera",  T_NUDE),
        ("chip-x.svg",         "x",         "x",         "@soymissyera", T_FRAM),
        ("chip-web.svg",       "web",       "mi web",    "missyera.com", T_VINO),
    ]:
        escribir(nombre, chip(glifo, red, handle, t))

    print("herramientas y llamadas a la acción")
    escribir("herramientas.svg", herramientas([
        [("python", "Python"), ("sql", "SQL"), ("powerbi", "Power BI"), ("excel", "Excel")],
        [("ml", "Machine Learning"), ("ia", "IA generativa"), ("claude", "Claude"), ("git", "Git")],
    ]))
    escribir("cta-diagnostico.svg", boton_cta("agenda conmigo", "Tu diagnóstico", T_VINO))
    escribir("cta-fullday.svg", boton_cta("aprende en un día", "Full Day de IA", T_FRAM))
    escribir("cta-consultoria.svg", boton_cta("trabajemos juntos", "Consultoría en IA", T_FRAM))
    escribir("cta-portafolio.svg", boton_cta("mi portafolio", "Modelo y anfitriona", T_VINO))

    escribir("btn-calendario-1.svg", boton("Edición 1", T_VINO))
    escribir("btn-calendario-2.svg", boton("Edición 2", T_FRAM))

    print("pies editoriales y cierre")
    escribir("marco-charlas.svg", pie("miss yera · sobre el escenario", T_NUDE))
    escribir("marco-calendario.svg", pie("miss yera · calendario 2026 · lima, perú", T_NUDE))
    escribir("cta-final.svg", cierre())
    print("listo")
