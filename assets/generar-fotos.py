#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compone las piezas del README que llevan foto.

Las fotos van incrustadas en base64 dentro del propio SVG. Es la única forma:
GitHub sirve los SVG en un entorno aislado que bloquea cualquier recurso
externo, así que un <image href="https://..."> no cargaría nunca.

A cambio, incrustar permite virar la foto a duotono vino con un filtro SVG y
componer tipografía encima, o sea maquetar de verdad en vez de solo enmarcar.
El base64 engorda un tercio, así que estas piezas son pocas y las fotos se
reescalan antes de incrustar.

Correlo con `python3 assets/generar-fotos.py` después de cambiar una foto.
"""
import base64
import glob
import io
import os

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = sorted(glob.glob(os.path.join(AQUI, "fotos", "*.jpeg")))

NUDE, BLUSH, FRAMBUESA = "#F7E7EC", "#F2D9DF", "#9B2F55"
VINO, BORGONA, ORO_C = "#6E1435", "#4A0C24", "#E3A886"
SERIF = "Didot, 'Bodoni MT', 'Playfair Display', Georgia, 'Times New Roman', serif"
SANS = "Trebuchet MS, Segoe UI, Verdana, sans-serif"

# duotono: las sombras van a borgoña y las luces a nude
D_SOMBRA = (0.290, 0.047, 0.141)
D_LUZ = (0.969, 0.906, 0.925)


def incrustar(idx, ancho_max=620, calidad=80):
    """Reescala la foto y la devuelve como data URI."""
    im = Image.open(FOTOS[idx]).convert("RGB")
    if im.width > ancho_max:
        im = im.resize((ancho_max, round(im.height * ancho_max / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=calidad, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


def filtro_duotono(idg="duo"):
    s, l = D_SOMBRA, D_LUZ
    return (f'<filter id="{idg}" color-interpolation-filters="sRGB">'
            f'<feColorMatrix type="saturate" values="0"/>'
            f'<feComponentTransfer>'
            f'<feFuncR type="table" tableValues="{s[0]} {l[0]}"/>'
            f'<feFuncG type="table" tableValues="{s[1]} {l[1]}"/>'
            f'<feFuncB type="table" tableValues="{s[2]} {l[2]}"/>'
            f'</feComponentTransfer></filter>')


def defs_oro(idg="oro"):
    return (f'<linearGradient id="{idg}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="#F6D9C7"/><stop offset="32%" stop-color="#E3A886"/>'
            f'<stop offset="52%" stop-color="#F9E8DB"/><stop offset="74%" stop-color="#DFA184"/>'
            f'<stop offset="100%" stop-color="#EFC3AB"/></linearGradient>')


def rotulo(x, y, texto, color, tam=12, esp=4.4, anclaje="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anclaje}" font-family="{SANS}" '
            f'font-size="{tam}" letter-spacing="{esp}" fill="{color}">{texto.upper()}</text>')


def escribir(nombre, cuerpo):
    ruta = os.path.join(AQUI, nombre)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(cuerpo)
    print(f"  -> {nombre}  {os.path.getsize(ruta)//1024} KB")


# ---------------------------------------------------------------- portada
def portada(idx, w=820, h=430):
    """Cubierta de revista: campo de color a la izquierda, foto a la derecha."""
    uri, _ = incrustar(idx, 620)
    fx, fy, fw, fh = 452, 16, 352, h - 32
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_oro()}{filtro_duotono()}
<clipPath id="rec"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}"/></clipPath>
<linearGradient id="fundido" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{VINO}" stop-opacity="0.92"/>
<stop offset="42%" stop-color="{VINO}" stop-opacity="0"/></linearGradient>
<radialGradient id="campo" cx="0.28" cy="0.4" r="0.85">
<stop offset="0%" stop-color="{FRAMBUESA}" stop-opacity="0.28"/>
<stop offset="100%" stop-color="{VINO}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{w}" height="{h}" fill="{VINO}"/>
<rect width="{w}" height="{h}" fill="url(#campo)"/>
<g clip-path="url(#rec)">
<image href="{uri}" x="{fx}" y="{fy}" width="{fw}" height="{fh}"
       preserveAspectRatio="xMidYMin slice" filter="url(#duo)"/>
<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="url(#fundido)"/>
</g>
<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="url(#oro)" stroke-width="1.4"/>
{rotulo(58, 128, "consultora de ia · modelo", ORO_C, 13.5, 5.6)}
<text x="58" y="212" font-family="{SERIF}" font-size="66" letter-spacing="5" fill="{NUDE}">MISS</text>
<text x="58" y="282" font-family="{SERIF}" font-size="66" letter-spacing="5" fill="{NUDE}">YERA</text>
<path d="M58 314H392" stroke="url(#oro)" stroke-width="1.4"/>
<text x="58" y="352" font-family="{SANS}" font-size="19" fill="{BLUSH}">Convierto datos en decisiones</text>
<text x="58" y="378" font-family="{SANS}" font-size="19" fill="{BLUSH}">y la IA en algo que no da miedo.</text>
{rotulo(58, 410, "lima, perú · latam", ORO_C, 12, 4.2)}
</svg>'''


# ---------------------------------------------------------------- retrato
def retrato(idx, rotulo_txt, titulo, lineas, cita, oscuro=True, w=380, h=470):
    """Tarjeta vertical con foto arriba y texto debajo."""
    uri, _ = incrustar(idx, 480)
    fondo = VINO if oscuro else NUDE
    tinta = NUDE if oscuro else VINO
    suave = BLUSH if oscuro else "#C17C8C"
    filete = "url(#oro)" if oscuro else "#DCA9B4"
    fh_ = 244
    cuerpo = "".join(
        f'<text x="{w/2}" y="{fh_ + 108 + i*27}" text-anchor="middle" font-family="{SANS}" '
        f'font-size="18" fill="{tinta}" opacity="0.88">{ln}</text>'
        for i, ln in enumerate(lineas))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_oro()}{filtro_duotono()}
<clipPath id="rec"><rect x="13" y="13" width="{w-26}" height="{fh_}"/></clipPath>
<linearGradient id="fundido" x1="0" y1="0" x2="0" y2="1">
<stop offset="55%" stop-color="{fondo}" stop-opacity="0"/>
<stop offset="100%" stop-color="{fondo}" stop-opacity="0.95"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" fill="{fondo}"/>
<g clip-path="url(#rec)">
<image href="{uri}" x="13" y="13" width="{w-26}" height="{fh_}"
       preserveAspectRatio="xMidYMin slice" filter="url(#duo)"/>
<rect x="13" y="13" width="{w-26}" height="{fh_}" fill="url(#fundido)"/>
</g>
<rect x="13" y="13" width="{w-26}" height="{h-26}" fill="none" stroke="{filete}" stroke-width="1.3"/>
{rotulo(w/2, fh_ + 34, rotulo_txt, suave, 12.5, 4.2, "middle")}
<text x="{w/2}" y="{fh_ + 76}" text-anchor="middle" font-family="{SERIF}" font-size="32"
      letter-spacing="1" fill="{tinta}">{titulo}</text>
<path d="M{w/2-34} {fh_+92}H{w/2+34}" stroke="{filete}" stroke-width="1.2"/>
{cuerpo}
<text x="{w/2}" y="{h-34}" text-anchor="middle" font-family="{SERIF}" font-size="19"
      font-style="italic" fill="{suave}">{cita}</text>
</svg>'''


if __name__ == "__main__":
    print("piezas con foto")
    # 26 = vestido vino sobre pared blanca, la más limpia de todas
    escribir("hero-portada.svg", portada(26))
    # 36 = escritorio con laptop y blazer  ·  28 = vestido largo, pared clara
    escribir("retrato-consultora.svg", retrato(
        36, "la consultora", "Datos e IA",
        ["Consultoría, automatización", "y análisis predictivo"],
        "“Tus datos ya saben la respuesta”", oscuro=True))
    escribir("retrato-modelo.svg", retrato(
        28, "la modelo", "Frente a cámara",
        ["Campañas, editoriales,", "anfitriona y embajadora"],
        "“La misma que arma los modelos”", oscuro=False))
    print("listo")
