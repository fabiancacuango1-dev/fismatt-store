#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera todas las páginas de fis-matt.com.

    python3 scripts/generar_sitio.py

⚠️ LAS PÁGINAS NO SE EDITAN A MANO. Se cambia este archivo y se vuelve a
generar. Así la cabecera, el pie, los precios y la versión son los mismos en
todas, y cambiar de versión es tocar UNA línea (VERSION, más abajo).

Qué garantiza este generador, y por qué:
  · Ninguna página carga nada de fuera para dibujarse: ni Tailwind, ni
    fuentes de Google, ni YouTube. La portada anterior pedía un compilador
    de 407 KB y 3,6 MB de imágenes; en la red de un colegio no cargaba.
  · Todo el contenido se lee sin JavaScript. El JavaScript solo añade la
    cotización de la tienda y el video al pulsar.
  · Los precios viven aquí (PLANES, COMPLEMENTOS, HERRAMIENTAS). La tienda
    los lee del HTML generado; no hay un segundo sitio donde cambiarlos.

Solo usa la biblioteca estándar de Python 3.
"""
import io
import json
import os
import re
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ════════════════════════════════════════════════════════════════════════
#  DATOS — lo único que cambia de una versión a otra
# ════════════════════════════════════════════════════════════════════════
VERSION = '4.95.0'
FAMILIA_VERSION = '2.0.0'
FECHA = '2026-10-06'
ESTILO_V = '20261006'           # cambia para que el navegador suelte la caché

_REL = 'https://github.com/fabiancacuango1-dev/fismatt-store/releases/download/v%s/' % VERSION
DESCARGAS = {
    'win': {'url': _REL + 'SistemaAcademico-v%s-Windows-Setup.exe' % VERSION, 'mb': '48 MB'},
    'mac': {'url': _REL + 'SistemaAcademico-v%s-macOS.dmg' % VERSION, 'mb': '33 MB'},
    'apk': {'url': _REL + 'SistemaAcademico-v%s-Android.apk' % VERSION, 'mb': '64 MB'},
    'familia': {'url': _REL + 'SAI-Familia-PortalPadres-%s.apk' % FAMILIA_VERSION, 'mb': '20 MB'},
    'sha': {'url': _REL + 'SHA256SUMS-Windows.txt'},
}

WHATSAPP = '593983274499'
WHATSAPP_BONITO = '+593 983 274 499'
CORREO = 'rectores_federal09@icloud.com'
PORTAL_FAMILIAS = 'https://portal-padres-sai.web.app'

# Precios individuales, por docente, en dólares.
PLANES = [
    {'id': 'mensual', 'nombre': 'plan mensual', 'titulo': 'Mensual', 'precio': 3.99, 'periodo': 'mes',
     'para': 'Para empezar sin comprometerse. Deja de pagar cuando quiera.'},
    {'id': 'anual', 'nombre': 'plan anual', 'titulo': 'Anual', 'precio': 35, 'periodo': 'año',
     'para': 'El año lectivo completo por menos de $3 al mes. El que elige la mayoría.'},
    {'id': 'unico', 'nombre': 'pago único', 'titulo': 'Pago único', 'precio': 120, 'periodo': 'único',
     'para': 'Un solo pago y el sistema es suyo, sin renovaciones.'},
]
COMPLEMENTOS = [
    {'id': 'celular', 'nombre': 'Complemento Celular', 'corto': 'Celular', 'precio': 15, 'periodo': 'año',
     'frase': 'El SAI también en su teléfono Android, conectado a su computadora.'},
    {'id': 'computadora', 'nombre': 'Complemento Otra computadora', 'corto': 'Otra computadora', 'precio': 15, 'periodo': 'año',
     'frase': 'Una segunda computadora —la laptop de la casa— con el mismo trabajo.'},
    {'id': 'familias', 'nombre': 'Complemento Familias', 'corto': 'Familias', 'precio': 10, 'periodo': 'año',
     'frase': 'Los representantes ven notas y asistencia en el portal y en la app SAI Familia.'},
]
HERRAMIENTAS = [
    {'id': 'simulador', 'nombre': 'Simulador Ser Maestro', 'precio': 10, 'periodo': 'año',
     'pagina': 'productos/simulador-ser-maestro.html', 'frase': 'Las cuatro fases de la evaluación docente, con la clase corregida por IA.'},
    {'id': 'importador', 'nombre': 'Importador de Notas', 'precio': 10, 'periodo': 'año',
     'pagina': 'productos/importador-notas.html', 'frase': 'Sube las calificaciones al portal del Ministerio sin copiar y pegar.'},
    {'id': 'horarios', 'nombre': 'EduHorarios', 'precio': 10, 'periodo': 'año',
     'pagina': 'productos/eduhorarios.html', 'frase': 'El horario de toda la institución, sin choques de docente ni de aula.'},
    {'id': 'boletines', 'nombre': 'Boletines Online', 'precio': 5, 'periodo': 'año',
     'pagina': 'productos/boletines-online.html', 'frase': 'Boletines con las plantillas oficiales, desde el navegador.'},
]


# ════════════════════════════════════════════════════════════════════════
#  UTILIDADES
# ════════════════════════════════════════════════════════════════════════
def usd(v):
    v = round(v * 100) / 100
    return '$' + (str(int(v)) if v == int(v) else ('%.2f' % v).replace('.', ','))


def per(periodo):
    return {'mes': '/mes', 'año': '/año', 'único': ''}[periodo]


def wa(texto=''):
    base = 'https://wa.me/' + WHATSAPP
    return base + ('?text=' + quote(texto) if texto else '')


def escribir(ruta, html):
    destino = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(destino) or RAIZ, exist_ok=True)
    io.open(destino, 'w', encoding='utf-8').write(html)
    print('  %-40s %5.1f KB' % (ruta, len(html.encode('utf-8')) / 1024))


# nombre → (anchos disponibles, ancho original, alto original)
IMAGENES = {
    'estudiantes': ((640, 1100), 1116, 716),
    'notas': ((640, 1100), 1116, 716),
    'registro-notas': ((640, 1100), 1600, 1028),
    'planificador': ((640, 1100), 1600, 1028),
    'cualitativas': ((640, 1100), 1600, 1028),
    'orientacion': ((640, 1100), 1600, 1028),
    'horarios': ((640, 1100), 1600, 962),
    'boletines': ((480, 900), 1874, 1790),
    'portal-familias': ((560, 1000), 1500, 936),
    'cloud': ((560, 1000), 1500, 936),
    'simulador': ((480, 900), 1498, 1418),
    'importador': ((560, 1000), 2672, 1670),
    'eduhorarios': ((560, 1000), 1498, 1030),
}


def img(nombre, alt, raiz='', clase='captura', primera=False, sizes='(min-width: 900px) 540px, 92vw'):
    """Imagen WebP en dos medidas. Lleva ancho y alto para que la página no
    salte al cargar; solo la primera de la portada se pide con prioridad."""
    anchos, w0, h0 = IMAGENES[nombre]
    grande = anchos[-1]
    alto = round(grande * h0 / w0)
    srcset = ', '.join('%sassets/img/web/%s-%d.webp %dw' % (raiz, nombre, a, a) for a in anchos)
    carga = 'fetchpriority="high"' if primera else 'loading="lazy" decoding="async"'
    return ('<img class="%s" src="%sassets/img/web/%s-%d.webp" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" %s>'
            % (clase, raiz, nombre, grande, srcset, sizes, grande, alto, alt, carga))


ISOTIPO = ('<svg viewBox="0 0 54 54" aria-hidden="true"><rect width="54" height="54" rx="11" fill="#d40000"/>'
           '<path fill="#fff" d="M13 11h31l-5 7H22v6h15l-5 7H22v12h-9z"/></svg>')
SVG_MOVIL = '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/></svg>'
SVG_PORTATIL = '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4.5" width="16" height="11" rx="1.6"/><path d="M2 19.5h20"/></svg>'
SVG_MONITOR = '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3.5" width="18" height="12.5" rx="1.6"/><path d="M9 20.5h6M12 16v4.5"/></svg>'
SVG_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'


# ════════════════════════════════════════════════════════════════════════
#  ARMAZÓN COMÚN
# ════════════════════════════════════════════════════════════════════════
def cabecera(raiz, activa=''):
    enlaces = [
        ('como', 'Cómo funciona', raiz + 'index.html#como-funciona'),
        ('modulos', 'Módulos', raiz + 'modulos.html'),
        ('complementos', 'Complementos', raiz + 'index.html#complementos'),
        ('precio', 'Precios', raiz + 'index.html#precio'),
        ('descargar', 'Descargar', raiz + 'descargar.html'),
    ]
    nav = ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if k == activa else '', t)
                  for k, t, u in enlaces)
    return f'''<header class="cab">
  <div class="wrap cab-fila">
    <a class="marca" href="{raiz}index.html" aria-label="FISMATT, inicio">{ISOTIPO}<span><b>FISMATT</b><small>Sistemas educativos</small></span></a>
    <nav class="nav" aria-label="Principal">{nav}</nav>
    <div class="cab-acc">
      <a class="btn-carrito" href="{raiz}tienda.html">Cotización <span class="n"></span></a>
      <details class="menu">
        <summary aria-label="Menú"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary>
        <div class="menu-panel">{nav}<a href="{raiz}tienda.html">Tienda y cotización</a></div>
      </details>
    </div>
  </div>
</header>'''


def pie(raiz, flota=True):
    burbuja = f'<a class="wa-flota" href="{wa()}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{SVG_WA}</a>' if flota else ''
    return f'''<footer class="pie">
  <div class="wrap">
    <div class="pie-grid">
      <div>
        <a class="marca" href="{raiz}index.html">{ISOTIPO}<span><b>FISMATT</b><small>Sistemas educativos</small></span></a>
        <p style="margin-top:14px;max-width:300px">Tecnología educativa hecha en Ecuador para docentes e instituciones.</p>
        <a href="{wa()}" target="_blank" rel="noopener" style="margin-top:10px">WhatsApp {WHATSAPP_BONITO}</a>
        <a href="mailto:{CORREO}">{CORREO}</a>
      </div>
      <div>
        <h4>Sistema SAI</h4>
        <a href="{raiz}index.html#como-funciona">Cómo funciona</a>
        <a href="{raiz}modulos.html">Todos los módulos</a>
        <a href="{raiz}index.html#complementos">Complementos</a>
        <a href="{raiz}index.html#precio">Precios</a>
        <a href="{raiz}tienda.html">Tienda y cotización</a>
        <a href="{raiz}descargar.html">Descargar</a>
      </div>
      <div>
        <h4>Otras herramientas</h4>
        <a href="{raiz}productos/simulador-ser-maestro.html">Simulador Ser Maestro</a>
        <a href="{raiz}productos/importador-notas.html">Importador de Notas</a>
        <a href="{raiz}productos/eduhorarios.html">EduHorarios</a>
        <a href="{raiz}productos/boletines-online.html">Boletines Online</a>
      </div>
      <div>
        <h4>Legal</h4>
        <a href="{raiz}legal/privacidad.html">Política de privacidad</a>
        <a href="{raiz}legal/terminos.html">Términos y condiciones</a>
      </div>
    </div>
    <div class="fin"><span>&copy; 2026 FISMATT SYSTEMS &middot; Proyecto independiente, sin afiliación al Ministerio de Educación.</span><span>Hecho en Ecuador</span></div>
  </div>
</footer>
{burbuja}'''


def pagina(ruta, titulo, descripcion, cuerpo, activa='', guiones=('sai',), extra_cabeza='', indexar=True, despues='', flota=True, clase_cuerpo=''):
    raiz = '../' * ruta.count('/')
    canon = 'https://fis-matt.com/' + ('' if ruta == 'index.html' else ruta)
    scripts = ''.join('<script src="%sjs/%s.js?v=%s" defer></script>\n' % (raiz, g, ESTILO_V) for g in guiones)
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<meta name="theme-color" content="#050505">
{'' if indexar else '<meta name="robots" content="noindex, follow">'}
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://fis-matt.com/assets/img/productos/app-estudiantes.png">
<meta property="og:site_name" content="FISMATT">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{raiz}assets/img/favicon.svg">
<link rel="stylesheet" href="{raiz}css/sai.css?v={ESTILO_V}">
{extra_cabeza}</head>
<body{(' class="' + clase_cuerpo + '"') if clase_cuerpo else ''}>
{cabecera(raiz, activa)}
<main>
{cuerpo}
</main>
{pie(raiz, flota)}
{despues}{scripts}</body>
</html>
'''
    html = re.sub(r'\n{3,}', '\n\n', html)
    escribir(ruta, html)


# ════════════════════════════════════════════════════════════════════════
#  BLOQUES QUE SE REPITEN
# ════════════════════════════════════════════════════════════════════════
def bloque_diagrama():
    c, o = COMPLEMENTOS[0], COMPLEMENTOS[1]
    return f'''<div class="red" role="img" aria-label="El celular y una segunda computadora se conectan con su computadora principal por la red WiFi.">
      <div class="red-nodo">{SVG_MOVIL}<b>Celular</b><span>Android &middot; en el aula</span><i>Complemento &middot; {usd(c['precio'])}/año</i></div>
      <div class="red-lazo"><span>QR &middot; misma WiFi</span></div>
      <div class="red-nodo centro-n">{SVG_PORTATIL}<b>Su computadora</b><span>Windows o Mac</span><i>Incluida en el SAI</i></div>
      <div class="red-lazo"><span>Código &middot; misma WiFi</span></div>
      <div class="red-nodo">{SVG_MONITOR}<b>Otra computadora</b><span>La de la casa o la del colegio</span><i>Complemento &middot; {usd(o['precio'])}/año</i></div>
    </div>'''


def bloque_planes(raiz=''):
    tarjetas = []
    for p in PLANES:
        dest = p['id'] == 'anual'
        tarjetas.append(f'''<div class="plan{' destacado' if dest else ''}">
        {'<span class="cinta">El más elegido</span>' if dest else ''}
        <h3>{p['titulo']}</h3>
        <div class="cifra">{usd(p['precio'])} <small>{per(p['periodo'])}</small></div>
        <p>{p['para']}</p>
        <a class="btn {'btn-rojo' if dest else 'btn-borde'} btn-ancho" href="{raiz}tienda.html?plan={p['id']}">Elegir {p['titulo'].lower()}</a>
      </div>''')
    return '<div class="g g3">' + '\n      '.join(tarjetas) + '</div>'


def bloque_tabla_complementos():
    filas = ''.join(
        f'<tr><td><b>{c["corto"]}</b></td><td>{c["frase"]}</td><td class="p">+ {usd(c["precio"])} <small>/año</small></td></tr>'
        for c in COMPLEMENTOS)
    anual = PLANES[1]['precio']
    return f'''<div class="tabla-caja">
      <table class="tabla">
        <caption class="oculto-visual">Qué incluye el SAI y qué se añade aparte</caption>
        <thead><tr><th scope="col">Qué</th><th scope="col">Para qué sirve</th><th scope="col">Precio</th></tr></thead>
        <tbody>
          <tr class="res"><td><b>Sistema SAI</b></td><td>El sistema completo, con todos sus módulos, en <b>una computadora</b> con Windows o Mac.</td><td class="p">{usd(anual)} <small>/año</small></td></tr>
          {filas}
        </tbody>
      </table>
    </div>'''


def bloque_ejemplos():
    a = PLANES[1]['precio']
    cel, pc, fam = (c['precio'] for c in COMPLEMENTOS)
    return f'''<div class="ejemplos">
      <div class="ejemplo"><b>Solo en mi computadora</b><span>El SAI, sin complementos</span><strong>{usd(a)} <small>al año</small></strong></div>
      <div class="ejemplo"><b>Computadora y celular</b><span>SAI + Celular</span><strong>{usd(a + cel)} <small>al año</small></strong></div>
      <div class="ejemplo"><b>Todo conectado</b><span>SAI + Celular + Otra computadora + Familias</span><strong>{usd(a + cel + pc + fam)} <small>al año</small></strong></div>
    </div>'''


def bloque_pagos():
    return '''<div class="pagos">
      <div class="tarjeta"><h3>Transferencia bancaria</h3><p>Transfiere desde su banco y nos envía el comprobante por WhatsApp.</p></div>
      <div class="tarjeta"><h3>Depósito o efectivo</h3><p>Depósito en ventanilla o en un corresponsal, o pago en efectivo.</p></div>
      <div class="tarjeta"><h3>Tarjeta o PayPal</h3><p>Le enviamos un enlace de cobro para pagar con tarjeta o con su cuenta de PayPal.</p></div>
    </div>'''


def bloque_descargas(raiz=''):
    d = DESCARGAS
    return f'''<div class="g g3">
      <a class="bajar" href="{d['win']['url']}"><span class="so">WIN</span><span><b>Windows</b><small>Windows 10 y 11 &middot; v{VERSION} &middot; {d['win']['mb']}</small></span><span class="fl" aria-hidden="true">&darr;</span></a>
      <a class="bajar" href="{d['mac']['url']}"><span class="so">MAC</span><span><b>Mac</b><small>Chip Apple &middot; macOS 12+ &middot; v{VERSION} &middot; {d['mac']['mb']}</small></span><span class="fl" aria-hidden="true">&darr;</span></a>
      <a class="bajar" href="{d['apk']['url']}"><span class="so">APK</span><span><b>Android</b><small>Complemento Celular &middot; v{VERSION} &middot; {d['apk']['mb']}</small></span><span class="fl" aria-hidden="true">&darr;</span></a>
    </div>'''


# ════════════════════════════════════════════════════════════════════════
#  PORTADA
# ════════════════════════════════════════════════════════════════════════
def portada():
    anual = PLANES[1]['precio']
    jsonld = json.dumps({
        '@context': 'https://schema.org', '@type': 'SoftwareApplication',
        'name': 'FISMATT Sistema Académico Institucional (SAI)',
        'operatingSystem': 'Windows, macOS, Android',
        'applicationCategory': 'EducationalApplication',
        'softwareVersion': VERSION,
        'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'USD', 'lowPrice': '3.99', 'highPrice': '120',
                   'offerCount': '3',
                   'description': 'Por docente: USD 3,99 al mes, USD 35 al año o USD 120 en un solo pago. '
                                  'Complementos anuales: celular USD 15, otra computadora USD 15, familias USD 10.'},
        'publisher': {'@type': 'Organization', 'name': 'FISMATT SYSTEMS', 'url': 'https://fis-matt.com'},
    }, ensure_ascii=False, indent=1)

    comp_tarjetas = ''.join(f'''<div class="tarjeta">
          <span class="etiqueta clara">+ {usd(c['precio'])} al año</span>
          <h3>{c['corto']}</h3>
          <p>{d}</p>
        </div>''' for c, d in zip(COMPLEMENTOS, [
        'Instala la app del SAI en su teléfono Android y la empareja <b>una sola vez</b> con el código QR que muestra su computadora. Desde ahí se sincronizan solos cuando están en la misma WiFi: pasa lista en el aula y aparece en su computadora.',
        'El escritorio del colegio y la laptop de la casa comparten el mismo trabajo. Se emparejan una vez copiando un código y después se mantienen al día solas, aunque el router cambie de dirección.',
        'Usted publica notas y asistencia desde el SAI. El representante las ve en el portal web o en la app <b>SAI Familia</b>, con una pantalla «Hoy» que le dice qué hay que recuperar y avisos de notas y faltas.',
    ]))

    cuerpo = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="ceja" style="color:#ff5a5a">Sistema Académico Institucional &middot; SAI</p>
      <h1>El sistema que mueve <em>toda una institución.</em></h1>
      <p class="lead">Estudiantes, calificaciones, asistencia, planificaciones e informes en un solo programa para su computadora. Funciona sin internet y sus datos se quedan con usted.</p>
      <div class="hero-btns">
        <a class="btn btn-rojo" href="tienda.html">Armar mi cotización</a>
        <a class="btn btn-borde-claro" href="descargar.html">Descargar v{VERSION}</a>
      </div>
      <p class="hero-precio">Desde <b>{usd(anual)} al año</b> por docente &middot; Windows y Mac</p>
    </div>
    <div>{img('estudiantes', 'El SAI con la lista de estudiantes de un curso', clase='hero-img', primera=True, sizes='(min-width: 960px) 560px, 92vw')}</div>
  </div>
</section>

<div class="franja"><div class="wrap"><ul>
  <li>Funciona sin internet</li><li>Windows y Mac</li><li>Sus datos, en su computadora</li><li>Hecho para la normativa del Ecuador</li><li>Soporte por WhatsApp</li>
</ul></div></div>

<section class="sec" id="que-compra">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Qué se compra</p>
      <h2 class="titulo">Un sistema, y tres complementos <br>que se añaden solo si los necesita.</h2>
      <p class="bajada">El SAI trae todos sus módulos en una computadora. El celular, una segunda computadora y el portal para las familias son complementos aparte: usted paga por lo que usa.</p>
    </div>
    {bloque_tabla_complementos()}
    <p class="nota">Precios individuales, por docente. El SAI también se puede pagar por mes ({usd(PLANES[0]['precio'])}) o en un solo pago ({usd(PLANES[2]['precio'])}). Los complementos son anuales.</p>
    <div style="margin-top:22px">{bloque_ejemplos()}</div>
    <p style="margin-top:26px"><a class="btn btn-negro" href="tienda.html">Armar mi cotización</a></p>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="como-funciona">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Cómo funciona</p>
      <h2 class="titulo">De la descarga a su primera clase, <br>en cuatro pasos.</h2>
    </div>
    <div class="g g4">
      <div class="tarjeta"><span class="num">1</span><h3>Descargue e instale</h3><p>El instalador es gratuito, para Windows o Mac. Se instala en unos minutos, sin técnico.</p></div>
      <div class="tarjeta"><span class="num">2</span><h3>Active su licencia</h3><p>Al pagar recibe su clave por WhatsApp. La escribe una vez y ese equipo queda activado.</p></div>
      <div class="tarjeta"><span class="num">3</span><h3>Suba su lista</h3><p>En Excel, PDF, CSV, Word o el archivo del Ministerio. El sistema arma el curso por usted.</p></div>
      <div class="tarjeta"><span class="num">4</span><h3>Trabaje</h3><p>Asistencia, notas, planificaciones e informes en PDF. Todo se respalda solo cada media hora.</p></div>
    </div>
    <p style="margin-top:22px"><a class="btn btn-borde" href="descargar.html">Ver la instalación paso a paso</a></p>
  </div>
</section>

<section class="sec" id="modulos"><span id="producto"></span>
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Qué hace</p>
      <h2 class="titulo">Todo el trabajo del docente, <br>y el de quienes lo acompañan.</h2>
      <p class="bajada">Todos los módulos vienen incluidos en el SAI. Aquí, lo principal; cada uno está explicado a detalle en su página.</p>
    </div>
    <div class="dos" style="margin-bottom:34px">
      <div>{img('registro-notas', 'Registro de calificaciones por insumos en el SAI')}</div>
      <div>
        <h3 style="font-size:22px;font-weight:900;color:var(--tinta);letter-spacing:-.02em">El aula, al día</h3>
        <ul class="lista" style="margin-top:8px">
          <li><b>Estudiantes:</b> suba la nómina en el archivo que tenga; el sistema arma el curso.</li>
          <li><b>Asistencia:</b> el tablero le dice qué corresponde hacer según la normativa.</li>
          <li><b>Calificaciones:</b> insumos, proyecto y examen, con los promedios hechos.</li>
          <li><b>Boletines e informes:</b> en PDF, listos para imprimir o enviar.</li>
        </ul>
      </div>
    </div>
    <div class="g g3">
      <a class="tarjeta" href="modulos.html#planificador"><h3>Planificador</h3><p>PUD, PCA, clase diaria y micro-curricular en tres pasos. Elija la destreza y se llenan los indicadores.</p><span class="mas">Ver a detalle &rarr;</span></a>
      <a class="tarjeta" href="modulos.html#tutor"><h3>Tutor de Curso</h3><p>Las notas y la asistencia de los docentes de su curso le llegan solas, actividad por actividad.</p><span class="mas">Ver a detalle &rarr;</span></a>
      <a class="tarjeta" href="modulos.html#eneis"><h3>ENEIS</h3><p>El plan del año se arma solo, con las 54 fichas oficiales por destreza y los informes en su formato.</p><span class="mas">Ver a detalle &rarr;</span></a>
      <a class="tarjeta" href="modulos.html#inspeccion"><h3>Inspección y Convivencia</h3><p>Asistencia de toda la institución, control del personal y una guía de 27 situaciones con sus actas.</p><span class="mas">Ver a detalle &rarr;</span></a>
      <a class="tarjeta" href="modulos.html#vicerrectorado"><h3>Vicerrectorado, Rectorado y Secretaría</h3><p>Las notas de todos los docentes, el libro de avales, los indicadores y las actas.</p><span class="mas">Ver a detalle &rarr;</span></a>
      <a class="tarjeta" href="modulos.html#respaldo"><h3>Respaldo</h3><p>Guarda todos los módulos, cada media hora y al cerrar. Restaurar suma; no pisa lo que ya tiene.</p><span class="mas">Ver a detalle &rarr;</span></a>
    </div>
    <p style="margin-top:24px"><a class="btn btn-negro" href="modulos.html">Ver todos los módulos a detalle</a></p>
  </div>
</section>

<section class="sec sec-negra" id="complementos"><span id="conexion"></span>
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Complementos</p>
      <h2 class="titulo">Su trabajo, también en el celular, <br>en otra computadora y con las familias.</h2>
      <p class="bajada">El celular y la segunda computadora se conectan por su propia red WiFi, de un equipo al otro: sin internet y sin que sus datos pasen por un servidor.</p>
    </div>
    {bloque_diagrama()}
    <div class="g g3">{comp_tarjetas}</div>
    <p style="margin-top:26px"><a class="btn btn-blanco" href="tienda.html">Añadir complementos a mi cotización</a></p>
  </div>
</section>

<section class="sec" id="autoridades"><span id="inspeccion"></span>
  <div class="wrap dos">
    <div>
      <p class="ceja">Para la institución</p>
      <h2 class="titulo">Lo que registra cada docente llega a su autoridad.</h2>
      <p class="bajada">Inspección, Vicerrectorado, Rectorado, Secretaría y DECE tienen su propio módulo, que se abre con la licencia de la autoridad. Un solo código conecta a todos los docentes del colegio.</p>
      <ul class="lista" style="margin-top:14px">
        <li><b>Inspección:</b> asistencia de toda la institución, justificaciones y control del personal.</li>
        <li><b>Vicerrectorado:</b> las notas de todos los docentes y el libro de avales.</li>
        <li><b>Rectorado y Secretaría:</b> indicadores reales, actas y certificados.</li>
      </ul>
      <p style="margin-top:22px"><a class="btn btn-negro" href="{wa('Hola, escribo por una institución y quiero una propuesta del Sistema Académico SAI')}" target="_blank" rel="noopener">Pedir propuesta para mi institución</a></p>
    </div>
    <div>{img('horarios', 'Horarios institucionales por curso en el SAI')}</div>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="precio">
  <div class="wrap">
    <div class="cabeza centro">
      <p class="ceja">Precios</p>
      <h2 class="titulo">Elija cómo pagar el SAI.</h2>
      <p class="bajada">El sistema es el mismo en los tres planes: cambia cuánto dura y cómo lo paga. Precio por docente, para una computadora.</p>
    </div>
    {bloque_planes()}
    <h3 style="font-size:20px;font-weight:900;color:var(--tinta);margin:40px 0 14px">Y los complementos, si los necesita</h3>
    <div class="g g3">
      {''.join(f'<div class="tarjeta"><h3>{c["corto"]}</h3><p>{c["frase"]}</p><p style="font-size:24px;font-weight:900;color:var(--tinta);margin-top:8px">+ {usd(c["precio"])} <small style="font-size:13px;color:var(--gris);font-weight:600">al año</small></p></div>' for c in COMPLEMENTOS)}
    </div>
    <p class="nota">Para instituciones preparamos una propuesta según el número de docentes: <a href="{wa('Hola, escribo por una institución y quiero una propuesta del Sistema Académico SAI')}" target="_blank" rel="noopener" style="color:var(--rojo);font-weight:700">escríbanos por WhatsApp</a>.</p>
  </div>
</section>

<section class="sec" id="como-comprar">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Cómo se compra</p>
      <h2 class="titulo">Cotice, pague y reciba su clave.</h2>
    </div>
    <div class="g g4" style="margin-bottom:26px">
      <div class="tarjeta"><span class="num">1</span><h3>Arme su cotización</h3><p>En la tienda elige el plan y los complementos. Ve el total al instante.</p></div>
      <div class="tarjeta"><span class="num">2</span><h3>Envíe el pedido</h3><p>Con un botón, por WhatsApp o por correo. También puede guardar la cotización en PDF.</p></div>
      <div class="tarjeta"><span class="num">3</span><h3>Pague</h3><p>Le enviamos los datos para pagar y usted nos manda el comprobante.</p></div>
      <div class="tarjeta"><span class="num">4</span><h3>Reciba su clave</h3><p>Su clave de licencia y la guía de instalación le llegan por WhatsApp.</p></div>
    </div>
    {bloque_pagos()}
    <p class="nota">30 días de garantía. Los datos para pagar se envían por WhatsApp al confirmar el pedido.</p>
    <p style="margin-top:22px"><a class="btn btn-rojo" href="tienda.html">Ir a la tienda</a></p>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="video"><span id="tutoriales"></span>
  <div class="wrap dos">
    <div>
      <p class="ceja">Véalo funcionando</p>
      <h2 class="titulo">Mire cómo trabaja un docente con el SAI.</h2>
      <p class="bajada">Un recorrido por el sistema antes de instalarlo. El video se carga solo cuando usted lo pide.</p>
    </div>
    <div class="video" data-yt="ak2QLxrOCpg" data-titulo="El sistema que todo docente necesita">
      {img('notas', '', clase='', sizes='(min-width: 900px) 540px, 92vw')}
      <button type="button"><span aria-hidden="true">&#9654;</span>Ver el video</button>
    </div>
  </div>
</section>

<section class="sec" id="descargar"><span id="descargas"></span>
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Descargas &middot; versión {VERSION}</p>
      <h2 class="titulo">Instálelo ahora.</h2>
      <p class="bajada">La descarga es gratuita; el sistema se activa con su licencia.</p>
    </div>
    {bloque_descargas()}
    <p class="nota">¿Ya lo tiene instalado? Se actualiza cuando usted quiera, desde <b>Respaldo &rarr; Buscar actualizaciones</b>. El sistema no interrumpe para avisar. <a href="descargar.html" style="color:var(--rojo);font-weight:700">Instalación paso a paso &rarr;</a></p>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="faq">
  <div class="wrap angosto">
    <div class="cabeza centro"><p class="ceja">Preguntas frecuentes</p><h2 class="titulo">Lo que más nos preguntan.</h2></div>
    <div class="faq">
      <details><summary>¿Qué incluye el SAI de {usd(anual)} al año?</summary><p>El sistema completo, con todos sus módulos, para una computadora con Windows o Mac: estudiantes, asistencia, calificaciones, boletines, planificador, tutoría, ENEIS, respaldo y los demás. Lo único aparte son los tres complementos.</p></details>
      <details><summary>¿Qué son los complementos y cuánto cuestan?</summary><p>Son tres añadidos opcionales, que se pagan por año: <b>Celular</b> ({usd(COMPLEMENTOS[0]['precio'])}) para usar el SAI en su teléfono Android; <b>Otra computadora</b> ({usd(COMPLEMENTOS[1]['precio'])}) para trabajar también en una segunda computadora; y <b>Familias</b> ({usd(COMPLEMENTOS[2]['precio'])}) para que los representantes vean notas y asistencia. Puede empezar solo con el SAI y añadirlos después.</p></details>
      <details><summary>¿Funciona sin internet?</summary><p>Sí. El trabajo diario no necesita conexión, y el celular y la segunda computadora se conectan por su WiFi sin salir a internet. Solo hacen falta datos para activar la licencia, publicar a las familias y buscar una actualización.</p></details>
      <details><summary>¿Cómo pago y cómo recibo mi licencia?</summary><p>Arme su cotización en la tienda y envíe el pedido por WhatsApp. Le respondemos con los datos para pagar por transferencia, depósito o efectivo, tarjeta o PayPal. Con el comprobante recibe su clave y la guía de instalación.</p></details>
      <details><summary>¿Se actualiza solo? ¿Me va a interrumpir?</summary><p>No. El sistema nunca se actualiza por su cuenta ni muestra avisos mientras trabaja. Cuando usted quiera, entra a Respaldo &rarr; Buscar actualizaciones.</p></details>
      <details><summary>¿Pierdo mis datos al actualizar?</summary><p>No. La actualización no toca su carpeta de datos, y el sistema guarda una copia de respaldo cada media hora y al cerrar.</p></details>
      <details><summary>¿Y para toda una institución?</summary><p>Preparamos una propuesta según el número de docentes, con los módulos de las autoridades. Escríbanos por WhatsApp.</p></details>
      <details><summary>Mi Mac dice que la aplicación «está dañada»</summary><p>No está dañada: macOS bloquea las aplicaciones que no pasan por la tienda de Apple.</p><ol><li>Abra el .dmg y arrastre la aplicación a Aplicaciones.</li><li>Abra Terminal y ejecute: <code>xattr -cr /Applications/sistema_institucional.app</code></li><li>Vuelva a abrirla desde Aplicaciones.</li></ol></details>
    </div>
  </div>
</section>

<section class="sec" id="mas">
  <div class="wrap">
    <p class="ceja">También de FISMATT</p>
    <div class="indice">
      {''.join(f'<a href="{h["pagina"]}">{h["nombre"]} &middot; {usd(h["precio"])}/año</a>' for h in HERRAMIENTAS)}
    </div>
  </div>
</section>'''
    pagina('index.html',
           'FISMATT SAI · Sistema Académico Institucional para docentes del Ecuador',
           'Sistema Académico Institucional (SAI): estudiantes, asistencia, calificaciones, planificaciones e informes en su computadora, sin internet. Desde $35 al año. Complementos: celular, otra computadora y familias.',
           cuerpo, extra_cabeza='<script type="application/ld+json">\n' + jsonld + '\n</script>\n')


# ════════════════════════════════════════════════════════════════════════
#  TIENDA
# ════════════════════════════════════════════════════════════════════════
def control(etiqueta):
    return (f'<div class="cant" role="group" aria-label="{etiqueta}">'
            '<button type="button" data-paso="-1" aria-label="Quitar uno">&minus;</button>'
            '<output aria-live="polite">0</output>'
            '<button type="button" data-paso="1" aria-label="Añadir uno">+</button></div>')


def tienda():
    radios = ''.join(
        f'<label><input type="radio" name="plan" value="{p["id"]}" data-nombre="{p["nombre"]}" data-precio="{p["precio"]}" data-periodo="{p["periodo"]}"{" checked" if p["id"] == "anual" else ""}>'
        f'<b>{p["titulo"]}</b><strong>{usd(p["precio"])}</strong> <small>{per(p["periodo"]) or "una sola vez"}</small></label>'
        for p in PLANES)

    def articulo(a, extra=''):
        return f'''<div class="item" data-item="{a['id']}" data-nombre="{a['nombre']}" data-precio="{a['precio']}" data-periodo="{a['periodo']}">
        <div><h3>{a['nombre']}</h3><p>{a['frase']}{extra}</p></div>
        <div class="pr">{usd(a['precio'])}<small>al año, c/u</small></div>
        <div class="ctl"><span style="font-size:13px;color:var(--gris)">Cantidad</span>{control(a['nombre'])}</div>
      </div>'''

    comps = ''.join(articulo(c) for c in COMPLEMENTOS)
    herrs = ''.join(articulo(h, f' <a href="{h["pagina"]}" style="color:var(--rojo);font-weight:700">Ver &rarr;</a>') for h in HERRAMIENTAS)
    pagos = ''.join(
        f'<label style="display:flex;gap:9px;align-items:center;padding:6px 0;font-size:14px;cursor:pointer"><input type="radio" name="pago" value="{v}"{" checked" if i == 0 else ""}> {v}</label>'
        for i, v in enumerate(['Transferencia bancaria', 'Depósito o efectivo', 'Tarjeta o PayPal']))

    cuerpo = f'''<section class="sec" style="padding-top:44px">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Tienda</p>
      <h1 class="titulo">Arme su cotización.</h1>
      <p class="bajada">Elija el plan del SAI y, si los necesita, los complementos. El total se calcula solo; después envía el pedido por WhatsApp o guarda la cotización en PDF.</p>
    </div>

    <noscript><p class="aviso" style="margin-bottom:20px">Para calcular el total hace falta JavaScript. Mientras tanto, estos son los precios; puede hacer su pedido por <a href="{wa('Hola, quiero hacer un pedido del Sistema Académico SAI')}">WhatsApp</a>.</p></noscript>

    <div class="tienda" id="tienda">
      <div>
        <div class="grupo-tienda">
          <h2>1. Sistema Académico SAI</h2>
          <p>El sistema completo, con todos sus módulos, para una computadora con Windows o Mac. Elija cómo pagarlo y para cuántos docentes.</p>
          <div class="item en" data-base>
            <div><h3>Sistema Académico SAI</h3><p>Una licencia por docente.</p></div>
            <div class="pr" style="font-size:14px;color:var(--gris)">Docentes</div>
            <div class="ctl" style="justify-content:flex-end">{control('Número de docentes')}</div>
            <div class="planes-radio" style="grid-column:1/-1">{radios}</div>
          </div>
        </div>

        <div class="grupo-tienda">
          <h2>2. Complementos</h2>
          <p>Opcionales y anuales. Añada uno por cada docente que lo vaya a usar.</p>
          {comps}
        </div>

        <div class="grupo-tienda">
          <h2>3. Otras herramientas FISMATT</h2>
          <p>Funcionan aparte del SAI, desde el navegador. Cada una tiene su página.</p>
          {herrs}
        </div>
      </div>

      <aside class="resumen" id="resumen" aria-label="Su cotización">
        <h2>Su cotización</h2>
        <p class="vacio" id="r-vacio" hidden>Todavía no ha elegido nada.</p>
        <ul class="lineas" id="r-lineas"></ul>
        <div class="total"><span>Total a pagar ahora</span><strong id="r-total">$0</strong></div>
        <p class="renueva" id="r-renueva"></p>
        <p class="priv" id="r-institucion" hidden style="color:#ffd27a;margin:0 0 12px">Con 5 docentes o más preparamos una propuesta para su institución: envíe el pedido y se la hacemos llegar.</p>

        <fieldset style="border:0;padding:0;margin:0 0 6px"><legend style="font-size:12px;font-weight:700;color:#b8b8bd;margin-bottom:2px">¿Cómo prefiere pagar?</legend>{pagos}</fieldset>

        <label class="campo"><span>Su nombre (opcional)</span><input id="c-nombre" type="text" autocomplete="name" placeholder="Nombre y apellido"></label>
        <label class="campo"><span>Institución (opcional)</span><input id="c-institucion" type="text" autocomplete="organization" placeholder="Unidad educativa"></label>
        <label class="campo"><span>Ciudad (opcional)</span><input id="c-ciudad" type="text" autocomplete="address-level2" placeholder="Ciudad"></label>

        <a class="btn btn-wa btn-ancho" id="b-wa" href="{wa()}" target="_blank" rel="noopener">Enviar pedido por WhatsApp</a>
        <a class="btn btn-blanco btn-ancho" id="b-pdf" href="#">Guardar cotización en PDF</a>
        <a class="btn btn-borde-claro btn-ancho" id="b-correo" href="mailto:{CORREO}">Enviar por correo</a>
        <p class="priv">Lo que escribe aquí no sale de su navegador hasta que usted pulsa enviar.</p>
      </aside>
    </div>
  </div>
</section>

<section class="sec sec-suave sec-borde">
  <div class="wrap">
    <div class="cabeza"><p class="ceja">Formas de pago</p><h2 class="titulo">Pague como le quede más fácil.</h2>
      <p class="bajada">Al confirmar su pedido por WhatsApp le enviamos los datos para pagar. Con el comprobante recibe su clave de licencia y la guía de instalación.</p></div>
    {bloque_pagos()}
    <p class="nota">30 días de garantía. Precios en dólares, individuales por docente.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap angosto">
    <div class="cabeza"><p class="ceja">Antes de pedir</p><h2 class="titulo">Dudas de la compra.</h2></div>
    <div class="faq">
      <details><summary>¿Necesito algún complemento para empezar?</summary><p>No. El SAI funciona completo en su computadora. Los complementos son para quien quiere usarlo además en el celular, en una segunda computadora, o compartir notas con las familias.</p></details>
      <details><summary>¿Puedo añadir un complemento más adelante?</summary><p>Sí. Nos escribe, paga el complemento y se añade a su misma licencia.</p></details>
      <details><summary>Tengo el plan mensual. ¿Puedo tener complementos?</summary><p>Sí. Los complementos se pagan por año aunque el SAI lo pague por mes.</p></details>
      <details><summary>¿La cotización me compromete a algo?</summary><p>No. Es un cálculo para que sepa cuánto pagaría; el pedido se confirma por WhatsApp.</p></details>
    </div>
  </div>
</section>'''
    pagina('tienda.html', 'Tienda y cotización · FISMATT SAI',
           'Arme su cotización del Sistema Académico SAI: plan mensual, anual o pago único, y los complementos de celular, otra computadora y familias. Envíe el pedido por WhatsApp.',
           cuerpo, guiones=('sai', 'tienda'), flota=False, clase_cuerpo='con-barra',
           despues='<a class="barra-total" href="#resumen"><span>Total<strong id="r-total-2">$0</strong></span><b>Ver y enviar pedido</b></a>\n'
                   '<div id="cotizacion" aria-hidden="true"></div>\n')


# ════════════════════════════════════════════════════════════════════════
#  MÓDULOS A DETALLE
# ════════════════════════════════════════════════════════════════════════
MODULOS = [
    ('El día a día del docente', [
        ('estudiantes', 'Estudiantes', 'La lista de su curso, sin teclearla.', [
            'Suba la nómina en Excel, PDF, CSV, una tabla de Word o los «.xls» del Ministerio.',
            'El sistema deduce qué es apellido y qué es nombre, y usted puede corregirlo antes de guardar.',
            'Ficha de cada estudiante, con los datos de su representante.',
            'Nómina y hoja de firmas en PDF.']),
        ('cursos', 'Cursos y Materias', 'Sus cursos, paralelos y asignaturas, de Inicial a Bachillerato.', [
            'Los porcentajes de calificación se ponen una sola vez y valen para todo el curso.',
            'Períodos semanales tomados de las horas de cada asignatura.']),
        ('asistencia', 'Asistencia', 'Pasar lista, y saber qué hacer con cada falta.', [
            'Toma diaria por curso y asignatura; un día registrado por error se puede eliminar.',
            'El tablero agrupa a los estudiantes por lo que exige la normativa y avisa cuántas faltas quedan antes de que el caso suba de instancia.',
            'Los feriados vienen puestos, y avisa si el día no era jornada.',
            'Un recordatorio discreto de las clases de su horario que quedaron sin asistencia.',
            'Informe de inasistencia numerado, con las actuaciones anteriores. Los informes cuentan días, no registros.']),
        ('calificaciones', 'Calificaciones', 'Insumos, proyecto y examen, con los promedios hechos.', [
            'Registro por actividad, con cálculo automático según el nivel.',
            'Calificación cualitativa para los subniveles que la usan.',
            'Un reloj en cada nota para dejar anotado el trabajo que se entregó con atraso, sin cambiar la nota.',
            'Recuperación e informes por parcial y por trimestre.']),
        ('boletines', 'Boletines', 'Parciales, trimestrales y de promoción.', [
            'Para todos los niveles, con la estructura que pide el Ministerio.',
            'En PDF, listos para imprimir o enviar al representante.']),
        ('planificador', 'Planificador', 'Todas las planificaciones en tres pasos.', [
            'PUD, PCA, clase diaria y planificación micro-curricular por unidad.',
            'Elija la destreza y se llenan solos los indicadores y las inserciones curriculares.',
            'Una sola planificación para varios paralelos del mismo curso.',
            'Los estudiantes con NEE se traen del módulo Estudiantes y se planifican a detalle.',
            'El sistema prepara las indicaciones para ChatGPT; usted pega el resultado y sale el documento con el formato de su institución, fórmulas incluidas.']),
        ('biblioteca', 'Biblioteca', 'Sus libros y documentos, en una estantería.', [
            'Una percha por área, con «En lectura» arriba y la página en que se quedó.',
            'Lectura pasando las hojas, apuntes, subrayados y «Mi resumen».',
            'El buscador encuentra también lo que usted escribió en sus apuntes.',
            'Desde la ficha del libro se envía al Planificador.']),
    ]),
    ('Tutoría y acompañamiento', [
        ('tutor', 'Tutor de Curso', 'Lo que entregan los docentes de su curso, sin pedirlo.', [
            'Las notas y la asistencia de cada asignatura le llegan solas, con la nota de cada actividad.',
            'Informe para el representante con las actividades por recuperar y las entregadas con atraso.',
            'Carta de compromiso, autorización de uso de imagen y ficha de datos, con su cuadro de firmas.',
            'Convocatoria general para todo el curso, junta de curso y actas de reunión.',
            'Convivencia con «Guía rápida»: elija qué pasó y el sistema dice qué corresponde y quién actúa.']),
        ('expediente', 'Expediente y Respaldos', 'Cómo está el curso, de un vistazo.', [
            'Estudiantes, promedio, en riesgo, expedientes al día y NEE.',
            'Qué documentos faltan más y a quién atender primero, con una tarjeta por estudiante.']),
        ('inclusion', 'Inclusión Educativa', 'Los estudiantes con necesidades educativas, bien atendidos.', [
            'Suba el informe de NEE y reciba orientaciones de cómo trabajar con el estudiante.',
            'Sus adaptaciones entran en la planificación.']),
        ('eneis', 'ENEIS', 'La Educación Integral en Sexualidad, sin armarla desde cero.', [
            '«Armar el plan del año» reparte las etapas y las herramientas en los meses que quedan.',
            'Las 54 fichas oficiales, por destreza, y un botón para acoplar ENEIS a una destreza del Planificador.',
            '«En el aula» solo le pide las fotos: el informe sale con el formato oficial, las firmas y los anexos.',
            'Encuestas en línea para docentes y estudiantes, con respuestas anónimas.']),
    ]),
    ('Autoridades de la institución', [
        ('inspeccion', 'Inspección y Convivencia', 'La asistencia y la convivencia de todo el colegio.', [
            'Toma diaria curso por curso y control diario de toda la institución.',
            'Buzón: las faltas que marca cada docente le llegan al inspector.',
            'Justificaciones y resoluciones que vuelven al registro de cada docente.',
            'Informes y certificados de asistencia, por curso y por estudiante.',
            'Control del personal docente: asistencia por jornada, permisos y licencias según la ley, y hoja de ruta.',
            'Convivencia: guía rápida de 27 situaciones con su base legal, y las actas de compromiso listas para firmar.']),
        ('vicerrectorado', 'Vicerrectorado', 'Las calificaciones de todos los docentes, y los avales.', [
            'Ve las notas que envía cada docente, sin recalcularlas.',
            'Libro de avales, con el documento numerado y su base legal.',
            'Un reloj avisa de los avales que están por vencer su plazo.']),
        ('rectorado', 'Rectorado', 'La institución, con números reales.', [
            'Indicadores armados con lo que registran los docentes.',
            'Reparte el código de la institución que conecta a todos los equipos.']),
        ('secretaria', 'Secretaría', 'Todos los estudiantes y todas sus notas.', [
            'Las actas de los docentes reposan en Secretaría.',
            'Certificados con la firma de la máxima autoridad.']),
        ('dece', 'DECE', 'Casos y protocolos, en su propio módulo.', [
            'Separado del trabajo del aula, para el personal del departamento.']),
    ]),
    ('El sistema', [
        ('sincronizar', 'Sincronizar', 'El mismo trabajo en más de un equipo.', [
            'Con el complemento <b>Celular</b>: su teléfono Android, emparejado una vez por código QR.',
            'Con el complemento <b>Otra computadora</b>: una segunda computadora, emparejada una vez por código.',
            'Viajan todos los módulos; lo que se trabajó en los dos equipos se suma, no se pisa.',
            'Por su propia red WiFi, sin internet. Las dos partes necesitan la misma versión del sistema.']),
        ('respaldo', 'Respaldo', 'Que nada se pierda.', [
            'Copia automática cada media hora y al cerrar, en su equipo y sin internet.',
            'El respaldo guarda todos los módulos; restaurar suma lo del respaldo a lo que ya tiene.',
            'Las actualizaciones se buscan aquí, cuando usted quiere. El sistema no interrumpe para avisar.']),
        ('configuracion', 'Configuración', 'Los datos de su institución.', [
            'Nombre, autoridades y logos, que salen en todos los documentos.',
            'Centro legal: términos, privacidad y constancia de aceptación en PDF.']),
    ]),
]


def modulos():
    indice = ''.join(f'<a href="#{i}">{n}</a>' for _, ms in MODULOS for i, n, _, _ in ms)
    bloques = []
    for grupo, ms in MODULOS:
        bloques.append(f'<h2 class="grupo-t">{grupo}</h2>')
        for i, nombre, que, puntos in ms:
            lis = ''.join(f'<li>{p}</li>' for p in puntos)
            bloques.append(f'<article class="modulo" id="{i}"><div><h3>{nombre}</h3><p class="que">{que}</p></div><ul class="lista">{lis}</ul></article>')
    cuerpo = f'''<section class="sec" style="padding-top:44px">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Módulos del SAI &middot; versión {VERSION}</p>
      <h1 class="titulo">Todo lo que hace el sistema, <br>módulo por módulo.</h1>
      <p class="bajada">Todos vienen incluidos en el SAI. Los de las autoridades se abren con la licencia de cada autoridad.</p>
    </div>
    <nav class="indice" aria-label="Módulos">{indice}</nav>
    {''.join(bloques)}
    <div class="dos" style="margin-top:40px">
      <div>{img('planificador', 'Planificador curricular del SAI')}</div>
      <div>{img('cualitativas', 'Calificaciones cualitativas en el SAI')}</div>
    </div>
  </div>
</section>

<section class="sec sec-negra">
  <div class="wrap centro">
    <h2 class="titulo">¿Listo para verlo en su computadora?</h2>
    <p class="bajada">Descárguelo gratis, o arme su cotización con los complementos que necesite.</p>
    <p style="margin-top:24px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn-rojo" href="tienda.html">Armar mi cotización</a>
      <a class="btn btn-borde-claro" href="descargar.html">Descargar</a>
    </p>
  </div>
</section>'''
    pagina('modulos.html', 'Módulos del SAI, a detalle · FISMATT',
           'Todo lo que hace el Sistema Académico SAI: estudiantes, asistencia, calificaciones, boletines, planificador, tutor, ENEIS, inspección, convivencia, vicerrectorado, secretaría y respaldo.',
           cuerpo, activa='modulos')


# ════════════════════════════════════════════════════════════════════════
#  DESCARGAR
# ════════════════════════════════════════════════════════════════════════
def descargar():
    d = DESCARGAS
    cuerpo = f'''<section class="sec" style="padding-top:44px">
  <div class="wrap">
    <div class="cabeza">
      <p class="ceja">Descargas &middot; versión {VERSION}</p>
      <h1 class="titulo">Descargue el SAI.</h1>
      <p class="bajada">La descarga es gratuita. El sistema se activa con su clave de licencia; si aún no la tiene, <a href="tienda.html" style="color:var(--rojo);font-weight:700">arme su cotización</a>.</p>
    </div>
    {bloque_descargas()}
    <p class="nota">El instalador de Mac es para equipos con chip Apple (M1 o posterior) y macOS 12 o superior. La app de Android se usa con el complemento Celular.
      ¿Quiere comprobar el archivo de Windows? Compare su huella con <a href="{d['sha']['url']}" style="color:var(--rojo);font-weight:700">SHA256SUMS-Windows.txt</a>.</p>

    <div class="g g2" style="margin-top:30px">
      <a class="bajar" href="{d['familia']['url']}"><span class="so" style="background:var(--rojo)">FAM</span><span><b>SAI Familia</b><small>Para representantes &middot; Android &middot; v{FAMILIA_VERSION} &middot; {d['familia']['mb']}</small></span><span class="fl" aria-hidden="true">&darr;</span></a>
      <a class="bajar" href="{PORTAL_FAMILIAS}" target="_blank" rel="noopener"><span class="so" style="background:var(--rojo)">WEB</span><span><b>Portal de Familias</b><small>Desde cualquier navegador, sin instalar nada</small></span><span class="fl" aria-hidden="true">&rarr;</span></a>
    </div>
    <p class="nota">SAI Familia y el portal son para los representantes de los docentes que tienen el complemento Familias.</p>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="instalar">
  <div class="wrap dos" style="align-items:start">
    <div>
      <p class="ceja">Instalación en Windows</p>
      <h2 class="titulo">Seis pasos.</h2>
      <ol class="pasos-inst" style="margin-top:22px">
        <li><b>Descargue</b> el instalador con el botón de Windows. Queda en su carpeta Descargas.</li>
        <li><b>Ábralo</b> con clic derecho &rarr; «Ejecutar como administrador». Un doble clic normal también sirve.</li>
        <li>Elija <b>«Instalar solo para mí»</b>. Esa opción no pide contraseña de administrador.</li>
        <li>Pulse <b>Siguiente</b> y después <b>Instalar</b>. Tarda menos de un minuto.</li>
        <li>Al abrirse, <b>escriba su clave</b> y pulse «Activar Licencia».</li>
        <li><b>Complete los datos</b> de su institución y ya puede trabajar.</li>
      </ol>
      <p class="aviso"><b>Si Windows muestra «Windows protegió su PC»:</b> pulse «Más información» y luego «Ejecutar de todas formas». Sale porque el instalador no lleva un certificado de firma de pago, no porque el archivo tenga algo malo.</p>
    </div>
    <div>
      <p class="ceja">Mac y Android</p>
      <h2 class="titulo">En los otros equipos.</h2>
      <div class="tarjeta" style="margin-top:22px"><h3>Mac</h3><p>Abra el archivo .dmg y arrastre el sistema a la carpeta Aplicaciones. La primera vez ábralo con clic derecho &rarr; Abrir. Si macOS dice que «está dañado», la solución está en las <a href="index.html#faq" style="color:var(--rojo);font-weight:700">preguntas frecuentes</a>.</p></div>
      <div class="tarjeta" style="margin-top:12px"><h3>Android (complemento Celular)</h3><p>Descargue el archivo .apk desde el teléfono y ábralo. Si el teléfono pide permiso para instalar desde esa aplicación, concédalo. Luego emparéjelo con su computadora desde Sincronizar, con el código QR.</p></div>
      <div class="tarjeta" style="margin-top:12px"><h3>¿Ya lo tiene instalado?</h3><p>No hace falta descargar nada de aquí: entre a <b>Respaldo &rarr; Buscar actualizaciones</b>. Sus datos no se tocan al actualizar.</p></div>
    </div>
  </div>
</section>'''
    pagina('descargar.html', 'Descargar el SAI v%s · FISMATT' % VERSION,
           'Descargue el Sistema Académico SAI v%s para Windows, Mac y Android, y la app SAI Familia. Instalación paso a paso.' % VERSION,
           cuerpo, activa='descargar')


# ════════════════════════════════════════════════════════════════════════
#  LAS OTRAS HERRAMIENTAS
# ════════════════════════════════════════════════════════════════════════
PRODUCTOS = [
    dict(slug='simulador-ser-maestro', id='simulador', titulo='Simulador Ser Maestro 2026', imagen='simulador',
         ceja='Con IA', h1='Llegue a la evaluación habiéndola dado ya.',
         lead='Simula las <b>cuatro fases reales</b> de la evaluación docente del Ministerio, con la clase demostrativa corregida por inteligencia artificial.',
         enlace='https://simulador-2026-9cfaa.web.app/#/login', cta='Probar el simulador', mensual='1,50', ahorro='$8',
         que='Una plataforma web. No se instala nada: entra con su cuenta desde cualquier computador.',
         puntos=[('Fase 1 — Prueba de conocimientos.', '99 preguntas, con el mismo formato y el mismo tiempo que el día de la evaluación.'),
                 ('Fase 2 — Autoinforme socioemocional.', 'El cuestionario tipo Likert, tal como se responde en la plataforma oficial.'),
                 ('Fase 3 — Responsabilidad profesional.', 'Los casos de ética y normativa que suelen dejar en blanco a quien no los practicó.'),
                 ('Fase 4 — Clase demostrativa evaluada por IA.', 'Sube su clase y recibe la corrección.'),
                 ('Practique las veces que quiera.', 'El año completo, sin límite de intentos.'),
                 ('Desde cualquier dispositivo.', 'Computadora, tablet o celular.')]),
    dict(slug='importador-notas', id='importador', titulo='Importador de Notas', imagen='importador',
         ceja='Extensión de Chrome', h1='Las notas al portal en segundos, no en horas.',
         lead='Sube las calificaciones desde Excel al portal docente del Ministerio <b>emparejando los nombres solo</b>.',
         enlace='https://chromewebstore.google.com/detail/pjdakeeclfpkheobgmenlonbbpmokbbh', cta='Instalar la extensión', mensual='1,50', ahorro='$8',
         que='Una extensión de Chrome. Se instala desde la tienda de Google y aparece cuando usted entra al portal del Ministerio.',
         puntos=[('Excel, CSV, TXT o PDF.', 'Sube el archivo que ya tenga.'),
                 ('Empareja los nombres por usted.', 'Reconoce al estudiante aunque en su archivo esté escrito distinto que en el portal.'),
                 ('Paginación automática.', 'Los cursos largos ya no obligan a ir página por página.'),
                 ('Modo «un clic».', 'Revisa, confirma y sube el curso entero.'),
                 ('Cualquier formato de calificación.', 'Cuantitativa o cualitativa.'),
                 ('Se actualiza sola.', 'Desde Chrome, cuando el portal cambia.')]),
    dict(slug='eduhorarios', id='horarios', titulo='EduHorarios', imagen='eduhorarios',
         ceja='Con IA · Para toda la institución', h1='El horario de todo el colegio, en un clic.',
         lead='Asigna materias, docentes, aulas y bloques <b>sin un solo choque</b>.',
         enlace='https://horarios.fis-matt.com', cta='Generar un horario', mensual='1,50', ahorro='$8',
         que='Una plataforma web en horarios.fis-matt.com. La usa quien arma el horario; los docentes reciben el resultado.',
         puntos=[('Detecta y resuelve los conflictos.', 'Un docente en dos aulas a la misma hora deja de descubrirse en octubre.'),
                 ('Restricciones que usted pone.', 'Por docente, por aula y por carga horaria.'),
                 ('Tres vistas del mismo horario.', 'Por curso, por docente o el cuadro institucional.'),
                 ('Exporta a PDF y a Excel.', 'Listo para imprimir o publicar.'),
                 ('Rehacerlo no cuesta nada.', 'Si entra un docente nuevo, se genera otra vez.'),
                 ('Sin instalar nada.', 'Se abre en el navegador.')]),
    dict(slug='boletines-online', id='boletines', titulo='Boletines Online', imagen='boletines',
         ceja='100% web', h1='Boletines listos, sin instalar nada.',
         lead='Genera los boletines desde el navegador con las <b>plantillas oficiales</b>.',
         enlace='https://generador.fis-matt.com', cta='Crear un boletín', mensual='0,90', ahorro='$5,80',
         que='Una plataforma web en generador.fis-matt.com. Entra, carga las notas y descarga el boletín.',
         puntos=[('Plantillas oficiales.', 'El formato que le van a pedir.'),
                 ('Computadora, tablet o celular.', 'El mismo boletín desde donde esté.'),
                 ('PDF listo para imprimir o enviar.', 'Se manda por WhatsApp al representante.'),
                 ('Guardado en la nube, si quiere.', 'Opcional.'),
                 ('El más económico.', 'Para el docente que solo necesita esto.'),
                 ('Sin instalar ni actualizar nada.', 'Siempre en la última versión.')]),
]


def productos():
    precio = {h['id']: h['precio'] for h in HERRAMIENTAS}
    for p in PRODUCTOS:
        anual = precio[p['id']]
        puntos = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in p['puntos'])
        otros = ''.join(f'<a href="{o["slug"]}.html">{o["titulo"]}</a>' for o in PRODUCTOS if o is not p)
        cuerpo = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="ceja" style="color:#ff5a5a">{p['ceja']}</p>
      <h1 style="font-size:clamp(1.9rem,5vw,3.1rem)">{p['h1']}</h1>
      <p class="lead">{p['lead']}</p>
      <div class="hero-btns">
        <a class="btn btn-rojo" href="{p['enlace']}" target="_blank" rel="noopener">{p['cta']}</a>
        <a class="btn btn-borde-claro" href="../tienda.html">Añadir a mi cotización</a>
      </div>
      <p class="hero-precio"><b>{usd(anual)}</b> al año &middot; o <b>${p['mensual']}</b> al mes</p>
    </div>
    <div>{img(p['imagen'], p['titulo'], raiz='../', clase='hero-img', primera=True, sizes='(min-width: 960px) 560px, 92vw')}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap angosto">
    <p style="font-size:17px"><b style="color:var(--tinta)">Qué es.</b> {p['que']}</p>
    <h2 class="titulo" style="margin-top:36px">Lo que le resuelve.</h2>
    <ul class="lista" style="margin-top:14px">{puntos}</ul>
  </div>
</section>

<section class="sec sec-suave sec-borde" id="precio">
  <div class="wrap angosto">
    <div class="cabeza"><p class="ceja">Precio</p><h2 class="titulo">Dos formas de pagarlo.</h2></div>
    <div class="tabla-caja"><table class="tabla">
      <thead><tr><th scope="col">Plan</th><th scope="col">Precio</th><th scope="col">Ideal para</th></tr></thead>
      <tbody>
        <tr><td><b>Mensual</b></td><td class="p">${p['mensual']} <small>/mes</small></td><td>Probarlo sin comprometerse</td></tr>
        <tr class="res"><td><b>Anual</b></td><td class="p">{usd(anual)} <small>/año</small></td><td>El año lectivo completo &mdash; ahorra {p['ahorro']}</td></tr>
      </tbody></table></div>
    <p style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn btn-negro" href="../tienda.html">Añadir a mi cotización</a>
      <a class="btn btn-borde" href="{wa('Hola, quiero información de ' + p['titulo'])}" target="_blank" rel="noopener">Preguntar por WhatsApp</a>
    </p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="ceja">También de FISMATT</p>
    <div class="indice"><a href="../index.html">Sistema Académico SAI</a>{otros}</div>
  </div>
</section>'''
        pagina('productos/%s.html' % p['slug'], '%s · FISMATT' % p['titulo'],
               re.sub(r'<[^>]+>', '', p['lead']) + ' %s al año.' % usd(anual), cuerpo)

    filas = ''.join(f'<a class="tarjeta" href="{h["pagina"].split("/")[1]}"><h3>{h["nombre"]}</h3><p>{h["frase"]}</p><span class="mas">{usd(h["precio"])} al año &rarr;</span></a>' for h in HERRAMIENTAS)
    pagina('productos/index.html', 'Productos FISMATT',
           'Los productos FISMATT para el docente ecuatoriano: Sistema Académico SAI, Simulador Ser Maestro, Importador de Notas, EduHorarios y Boletines Online.',
           f'''<section class="sec" style="padding-top:44px"><div class="wrap">
  <div class="cabeza"><p class="ceja">FISMATT</p><h1 class="titulo">Todos los productos.</h1></div>
  <div class="g g2"><a class="tarjeta" href="../index.html"><h3>Sistema Académico SAI</h3><p>Estudiantes, asistencia, calificaciones, planificaciones e informes, en su computadora.</p><span class="mas">Desde {usd(PLANES[1]['precio'])} al año &rarr;</span></a>{filas}</div>
</div></section>''')


# ════════════════════════════════════════════════════════════════════════
#  LEGALES — se conserva el texto, cambia el armazón
# ════════════════════════════════════════════════════════════════════════
def legales():
    for nombre, titulo in (('privacidad', 'Política de privacidad'), ('terminos', 'Términos y condiciones')):
        ruta = 'legal/%s.html' % nombre
        actual = io.open(os.path.join(RAIZ, ruta), encoding='utf-8').read()
        m = re.search(r'<main[^>]*>(.*?)</main>', actual, re.S)
        assert m, 'no encuentro <main> en ' + ruta
        texto = m.group(1)
        # Se queda solo el artículo si la página ya fue generada antes.
        art = re.search(r'<article class="prosa">(.*?)</article>', texto, re.S)
        if art:
            texto = art.group(1)
        texto = re.sub(r'\s+class="[^"]*"', '', texto).strip()
        cuerpo = f'<section class="sec" style="padding-top:44px"><div class="wrap angosto"><article class="prosa">\n{texto}\n</article></div></section>'
        pagina(ruta, '%s · FISMATT' % titulo, '%s de FISMATT SYSTEMS.' % titulo, cuerpo)


# ════════════════════════════════════════════════════════════════════════
#  CATÁLOGO Y MAPA DEL SITIO
# ════════════════════════════════════════════════════════════════════════
def catalogo():
    datos = {
        'sistema': {
            'nombre': 'Sistema Académico Institucional (SAI)', 'version': VERSION, 'actualizado': FECHA,
            'descargas': {k: v['url'] for k, v in DESCARGAS.items()},
            'planes': [{'id': p['id'], 'precio': p['precio'], 'periodo': p['periodo']} for p in PLANES],
            'complementos': [{'id': c['id'], 'nombre': c['nombre'], 'precio': c['precio'], 'periodo': c['periodo']} for c in COMPLEMENTOS],
            'nota': 'Precios en USD, individuales por docente. El SAI incluye una computadora; los complementos son anuales.',
        },
        'familia': {'nombre': 'SAI Familia', 'version': FAMILIA_VERSION, 'descarga': DESCARGAS['familia']['url'], 'portal': PORTAL_FAMILIAS},
        'herramientas': [{'id': h['id'], 'nombre': h['nombre'], 'precio': h['precio'], 'periodo': h['periodo'],
                          'pagina': '/' + h['pagina']} for h in HERRAMIENTAS],
        'pagos': ['Transferencia bancaria', 'Depósito o efectivo', 'Tarjeta o PayPal'],
        'generado_por': 'scripts/generar_sitio.py',
    }
    escribir('config/products.json', json.dumps(datos, indent=2, ensure_ascii=False) + '\n')

    urls = [('', '1.0'), ('tienda.html', '0.9'), ('modulos.html', '0.9'), ('descargar.html', '0.8'),
            ('productos/', '0.6')] + [('productos/%s.html' % p['slug'], '0.7') for p in PRODUCTOS] + \
           [('legal/privacidad.html', '0.3'), ('legal/terminos.html', '0.3')]
    cuerpo = ''.join('  <url><loc>https://fis-matt.com/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (u, FECHA, p)
                     for u, p in urls)
    escribir('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + cuerpo + '</urlset>\n')


if __name__ == '__main__':
    print('Generando fis-matt.com · SAI v%s' % VERSION)
    portada()
    tienda()
    modulos()
    descargar()
    productos()
    legales()
    catalogo()
    print('Listo.')
