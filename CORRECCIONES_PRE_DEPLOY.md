╔════════════════════════════════════════════════════════════════════════════════╗
║                  🔧 CORRECCIONES PRE-DEPLOY — PASO A PASO 🔧                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
                       CORRECCIÓN 1: META TAG CANONICAL
════════════════════════════════════════════════════════════════════════════════

UBICACIÓN: index.html, línea 13
IMPORTANCIA: Media (Afecta SEO)

ESTADO ACTUAL:
──────────────────────────────────────────────────────────────────────────────
13│      <link rel="canonical" href="https://softpluginpro.com/">

PROBLEMA:
─────────
• El canonical apunta a un dominio viejo
• GitHub Pages usará URL diferente
• Confunde a Google sobre tu sitio "real"

SOLUCIÓN (Elige una):

OPCIÓN A - Si usarás GitHub Pages (RECOMENDADO AHORA):
──────────────────────────────────────────────────────────
Reemplaza:
    <link rel="canonical" href="https://softpluginpro.com/">

Por:
    <link rel="canonical" href="https://luisfabiancacuangoeugenio.github.io/tienda-online/">

OPCIÓN B - Si tienes dominio personalizado (FUTURO):
────────────────────────────────────────────────────
Reemplaza:
    <link rel="canonical" href="https://softpluginpro.com/">

Por:
    <link rel="canonical" href="https://fismatt-systems.com/">

OPCIÓN C - Si usarás Netlify:
──────────────────────────────
Reemplaza:
    <link rel="canonical" href="https://softpluginpro.com/">

Por:
    <link rel="canonical" href="https://fismatt-systems.netlify.app/">

════════════════════════════════════════════════════════════════════════════════
                    CORRECCIÓN 2: OPEN GRAPH META TAGS
════════════════════════════════════════════════════════════════════════════════

UBICACIÓN: index.html, líneas 17-20
IMPORTANCIA: Alta (Afecta preview en redes sociales)

ESTADO ACTUAL:
──────────────────────────────────────────────────────────────────────────────
17│    <!-- Open Graph -->
18│    <meta property="og:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
19│    <meta property="og:description" content="El plugin definitivo para navegadores Chromium. Automatiza tareas y mejora tu productividad.">
20│    <meta property="og:type" content="website">
21│    <meta property="og:url" content="https://softpluginpro.com/">
22│    <meta property="og:image" content="assets/img/og-image.png">

PROBLEMAS:
──────────
1. og:title: Menciona "plugin" pero ahora es "herramientas educativas"
2. og:description: Genérica, no refleja FISMATT SYSTEMS
3. og:url: Apunta a dominio viejo
4. og:image: Ruta relativa (debe ser URL absoluta para redes)

SOLUCIÓN:
────────

OPCIÓN A - Para GitHub Pages:
──────────────────────────────

Reemplaza LÍNEAS 18-22:

    <!-- Open Graph -->
    <meta property="og:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
    <meta property="og:description" content="El plugin definitivo para navegadores Chromium. Automatiza tareas y mejora tu productividad.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://softpluginpro.com/">
    <meta property="og:image" content="assets/img/og-image.png">

Por:

    <!-- Open Graph -->
    <meta property="og:title" content="FISMATT SYSTEMS — Herramientas para Docentes Ecuador">
    <meta property="og:description" content="Importador de Notas Minduc e INEVAL-PRO. Gestiona calificaciones y evalúa desempeño docente.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://luisfabiancacuangoeugenio.github.io/tienda-online/">
    <meta property="og:image" content="https://luisfabiancacuangoeugenio.github.io/tienda-online/assets/img/og-image.png">

════════════════════════════════════════════════════════════════════════════════
                      CORRECCIÓN 3: TWITTER CARD META TAGS
════════════════════════════════════════════════════════════════════════════════

UBICACIÓN: index.html, líneas 24-25
IMPORTANCIA: Media (Afecta preview en Twitter/X)

ESTADO ACTUAL:
──────────────────────────────────────────────────────────────────────────────
24│    <!-- Twitter Card -->
25│    <meta name="twitter:card" content="summary_large_image">
26│    <meta name="twitter:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
27│    <meta name="twitter:description" content="El plugin definitivo para navegadores Chromium. Automatiza tareas y mejora tu productividad.">

PROBLEMAS:
──────────
1. twitter:title: Genérica, no refleja la realidad
2. twitter:description: No menciona productos reales

SOLUCIÓN:

Reemplaza LÍNEAS 26-27:

    <meta name="twitter:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
    <meta name="twitter:description" content="El plugin definitivo para navegadores Chromium. Automatiza tareas y mejora tu productividad.">

Por:

    <meta name="twitter:title" content="FISMATT SYSTEMS — Herramientas para Docentes Ecuador">
    <meta name="twitter:description" content="Importador de Notas Minduc + INEVAL-PRO. Optimiza la gestión educativa.">

════════════════════════════════════════════════════════════════════════════════
                   CORRECCIÓN 4: CREAR IMAGEN og-image.png
════════════════════════════════════════════════════════════════════════════════

UBICACIÓN: assets/img/og-image.png (no existe, falta crear)
IMPORTANCIA: Alta (Sin esto, preview en redes no se ve bien)

ESPECIFICACIONES:
──────────────────
• Dimensiones: 1200 x 630 píxeles (EXACTO)
• Formato: PNG (recomendado) o JPG
• Peso: < 200KB preferiblemente
• Ubicación: /assets/img/og-image.png
• Contenido: Logo + branding FISMATT SYSTEMS

OPCIONES PARA CREAR:

A. FÁCIL - Usar Canva (Recomendado):
───────────────────────────────────
1. Ve a https://www.canva.com
2. Crea diseño nuevo: 1200x630
3. Añade:
   - Fondo: Gradiente azul #1e40af a amarillo #fbbf24
   - Texto: "FISMATT SYSTEMS"
   - Subtítulo: "Herramientas para Docentes Ecuador"
   - Iconos: Descarga stock (eduación, etc.)
4. Descarga como PNG
5. Guarda en: /assets/img/og-image.png

B. MÁS PROFESIONAL - Usar Figma:
─────────────────────────────────
1. Ve a https://www.figma.com
2. Crea artboard 1200x630
3. Mismo diseño que Canva
4. Exporta como PNG

C. RÁPIDO - Usar IA:
────────────────────
Comando para crear con ImageMagick (si tienes instalado):

convert -size 1200x630 \
  gradient:"#1e40af"-"#fbbf24" \
  -fill white \
  -gravity center \
  -pointsize 80 -font "Arial-Bold" \
  -annotate +0+0 "FISMATT SYSTEMS" \
  /path/to/assets/img/og-image.png

════════════════════════════════════════════════════════════════════════════════
        INSTRUCCIONES PARA APLICAR CORRECCIONES EN VS CODE
════════════════════════════════════════════════════════════════════════════════

PASO 1: Abrir archivo index.html

  Abre VS Code
  File → Open → index.html

PASO 2: Buscar y reemplazar (Ctrl+H en Windows/Linux, Cmd+H en Mac)

  BUSCAR:             https://softpluginpro.com/
  REEMPLAZAR POR:     https://luisfabiancacuangoeugenio.github.io/tienda-online/
  
  Esto reemplaza TODAS las instancias automáticamente

PASO 3: Editar og:title y og:description (líneas 18-19)

  Línea 18:
  De:     <meta property="og:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
  A:      <meta property="og:title" content="FISMATT SYSTEMS — Herramientas para Docentes Ecuador">

  Línea 19:
  De:     <meta property="og:description" content="El plugin definitivo para navegadores Chromium...">
  A:      <meta property="og:description" content="Importador de Notas Minduc e INEVAL-PRO. Gestiona calificaciones.">

PASO 4: Editar twitter:title y twitter:description (líneas 26-27)

  Línea 26:
  De:     <meta name="twitter:title" content="FISMATT SYSTEMS — Automatiza tu Navegador">
  A:      <meta name="twitter:title" content="FISMATT SYSTEMS — Herramientas para Docentes Ecuador">

  Línea 27:
  De:     <meta name="twitter:description" content="El plugin definitivo...">
  A:      <meta name="twitter:description" content="Importador de Notas Minduc + INEVAL-PRO. Optimiza educación.">

PASO 5: Guardar cambios

  Cmd+S (Mac) o Ctrl+S (Windows/Linux)

════════════════════════════════════════════════════════════════════════════════
              VERIFICACIÓN POST-CORRECCIÓN (OPCIONAL)
════════════════════════════════════════════════════════════════════════════════

VERIFICAR EN NAVEGADOR:

1. Abre index.html en Chrome
2. Botón derecho → Inspeccionar
3. Console (F12)
4. Busca en Sources la sección <head>
5. Verifica que los meta tags sean correctos

VERIFICAR EN REDES SOCIALES:

1. Ve a https://www.facebook.com/sharer/debugger
2. Pega tu URL de GitHub Pages
3. Verifica que preview se ve bien (título, descripción, imagen)

════════════════════════════════════════════════════════════════════════════════
                         RESUMEN DE CAMBIOS NECESARIOS
════════════════════════════════════════════════════════════════════════════════

ARCHIVO: index.html

CAMBIOS (en orden de aparición):

✏️ LÍNEA 13:   Cambiar canonical URL
✏️ LÍNEA 18:   Cambiar og:title
✏️ LÍNEA 19:   Cambiar og:description
✏️ LÍNEA 21:   Cambiar og:url
✏️ LÍNEA 22:   Cambiar og:image a URL absoluta
✏️ LÍNEA 26:   Cambiar twitter:title
✏️ LÍNEA 27:   Cambiar twitter:description

CREAR: assets/img/og-image.png (1200x630px)

════════════════════════════════════════════════════════════════════════════════
                              PASOS FINALES
════════════════════════════════════════════════════════════════════════════════

1. Guardar todos los cambios en index.html
2. Crear og-image.png en Canva
3. Guardar en carpeta: assets/img/
4. Hacer commit en git:
   
   git add .
   git commit -m "Fix: update meta tags and add og-image for production"
   git push

5. Esperar GitHub Pages recarge (1-5 minutos)
6. Verificar en redes que preview se ve bien

════════════════════════════════════════════════════════════════════════════════

Todos los cambios son simples búsqueda/reemplazo.
Tiempo estimado: 5-10 minutos
Dificultad: Muy fácil

¡Después de esto, tu sitio estará 100% listo para producción!
