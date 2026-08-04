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
import io
import os
import re

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_FOTOS = os.path.join(AQUI, "fotos")

NUDE, BLUSH, FRAMBUESA = "#F7E7EC", "#F2D9DF", "#9B2F55"
VINO, BORGONA, ORO_C = "#6E1435", "#4A0C24", "#E3A886"
SERIF = "Didot, 'Bodoni MT', 'Playfair Display', Georgia, 'Times New Roman', serif"
SANS = "Trebuchet MS, Segoe UI, Verdana, sans-serif"

# duotono: las sombras van a borgoña y las luces a nude
D_SOMBRA = (0.290, 0.047, 0.141)
D_LUZ = (0.969, 0.906, 0.925)


def incrustar(nombre, ancho_max=620, calidad=80):
    """Reescala la foto y la devuelve como data URI."""
    im = Image.open(os.path.join(DIR_FOTOS, nombre + ".jpeg")).convert("RGB")
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


def defs_oro(w=1000, h=1000, idg="oro"):
    """Oro rosa en coordenadas de usuario: ver la nota en generar-assets.py."""
    return (f'<linearGradient id="{idg}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="{w}" y2="{h}">'
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


# ---------------------------------------------------------------- logotipo
# Caja del lettering dentro del lienzo 900x340 de placa-logo.svg, medida
# renderizando el grupo aislado y buscando los píxeles pintados.
LOGO_CAJA = (275, 57, 626, 253)


def logotipo(x, y, alto):
    """Devuelve el lettering de la marca, extraído de placa-logo.svg.

    Se lee del original en cada ejecución en vez de copiarlo, para que el
    logotipo tenga una sola fuente de verdad: si algún día se retoca la placa,
    la portada se actualiza sola.
    """
    fuente = io.open(os.path.join(AQUI, "placa-logo.svg"), encoding="utf-8").read()
    marca = '<g transform="translate(171.2,-94.5) scale(0.5)">'
    if marca not in fuente:
        raise SystemExit("placa-logo.svg cambió: no encuentro el grupo del lettering")
    ini = fuente.index(marca)
    prof, i = 0, ini
    while True:
        m = re.compile(r"</?g\b[^>]*>").search(fuente, i)
        etiqueta = m.group(0)
        prof += -1 if etiqueta.startswith("</") else (0 if etiqueta.endswith("/>") else 1)
        i = m.end()
        if prof == 0:
            break
    grupo = fuente[ini:i]
    x0, y0, x1, y1 = LOGO_CAJA
    k = alto / (y1 - y0)
    return (f'<g transform="translate({x - x0*k:.2f},{y - y0*k:.2f}) scale({k:.4f})">'
            f'{grupo}</g>'), (x1 - x0) * k


# ---------------------------------------------------------------- portada
def portada(foto, w=820, h=430):
    """Cubierta de revista: campo de color a la izquierda, foto a la derecha."""
    uri, _ = incrustar(foto, 620)
    fx, fy, fw, fh = 452, 16, 352, h - 32
    marca, ancho_marca = logotipo(58, 100, 150)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_oro(w, h)}{filtro_duotono()}
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
{rotulo(58, 78, "consultora de ia · modelo", ORO_C, 13.5, 5.6)}
{marca}
<path d="M58 302H{58 + max(ancho_marca, 260):.0f}" stroke="url(#oro)" stroke-width="1.4"/>
<text x="58" y="340" font-family="{SANS}" font-size="19" fill="{BLUSH}">Convierto datos en decisiones</text>
<text x="58" y="366" font-family="{SANS}" font-size="19" fill="{BLUSH}">y la IA en algo que no da miedo.</text>
{rotulo(58, 400, "lima, perú · latam", ORO_C, 12, 4.2)}
</svg>'''


# ---------------------------------------------------------------- retrato
def retrato(foto, rotulo_txt, titulo, lineas, cita, oscuro=True, w=380, h=470):
    """Tarjeta vertical con foto arriba y texto debajo."""
    uri, _ = incrustar(foto, 480)
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
<defs>{defs_oro(w, h)}{filtro_duotono()}
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


# ---------------------------------------------------------------- tira editorial
def tira(fotos, rotulo_txt, titulo, w=820, h=360):
    """Varias fotos en duotono, en fila, al modo de un desplegable de revista."""
    hueco = 10
    fw = (w - 26 - hueco * (len(fotos) - 1)) / len(fotos)
    fh_ = h - 118
    piezas, recortes, imagenes = "", "", ""
    for i, foto in enumerate(fotos):
        uri, _ = incrustar(foto, 360, 74)
        x = 13 + (fw + hueco) * i
        recortes += f'<clipPath id="r{i}"><rect x="{x:.1f}" y="13" width="{fw:.1f}" height="{fh_}"/></clipPath>'
        imagenes += (f'<g clip-path="url(#r{i})"><image href="{uri}" x="{x:.1f}" y="13" '
                     f'width="{fw:.1f}" height="{fh_}" preserveAspectRatio="xMidYMid slice" '
                     f'filter="url(#duo)"/></g>'
                     f'<rect x="{x:.1f}" y="13" width="{fw:.1f}" height="{fh_}" fill="none" '
                     f'stroke="url(#oro)" stroke-width="1.2"/>')
    piezas = imagenes
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_oro(w, h)}{filtro_duotono()}{recortes}</defs>
<rect width="{w}" height="{h}" fill="{VINO}"/>
{piezas}
{rotulo(w/2, h - 68, rotulo_txt, ORO_C, 12.5, 4.6, "middle")}
<text x="{w/2}" y="{h-30}" text-anchor="middle" font-family="{SERIF}" font-size="30"
      letter-spacing="1.4" fill="{NUDE}">{titulo}</text>
</svg>'''


if __name__ == "__main__":
    print("piezas con foto")
    # 26 = vestido vino sobre pared blanca, la más limpia de todas
    escribir("hero-portada.svg", portada("retrato-vestido-vino"))
    # 36 = escritorio con laptop y blazer  ·  28 = vestido largo, pared clara
    escribir("retrato-consultora.svg", retrato(
        "retrato-escritorio", "la consultora", "Datos e IA",
        ["Consultoría, automatización", "y análisis predictivo"],
        "“Tus datos ya saben la respuesta”", oscuro=True))
    escribir("retrato-modelo.svg", retrato(
        "retrato-vestido-largo", "la modelo", "Frente a cámara",
        ["Campañas, editoriales,", "anfitriona y embajadora"],
        "“La misma que arma los modelos”", oscuro=False))
    escribir("tira-editorial.svg", tira(
        ["editorial-playa-1", "editorial-yate", "editorial-playa-2"],
        "verano · lima, perú", "Fuera de la oficina"))
    print("listo")
