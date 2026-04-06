╔════════════════════════════════════════════════════════════════════════════════╗
║           🚀 CONFIGURACIÓN DE GITHUB ACTIONS + GITHUB PAGES 🚀                 ║
║                   Deploy Automático para HTML Puro                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
                    📋 ARCHIVO DEPLOY.YML — EXPLICACIÓN LÍNEA A LÍNEA
════════════════════════════════════════════════════════════════════════════════

Este es el archivo `.github/workflows/deploy.yml` que se debe crear en tu repo.
Ya está creado. AQUÍ VAE LA EXPLICACIÓN COMPLETA:

```yaml
name: Deploy a GitHub Pages
```
→ Nombre del workflow (aparece en la sección "Actions" de GitHub)


```yaml
on:
  push:
    branches: [ main ]
  workflow_dispatch:
```
→ CUÁNDO se ejecuta:
   • "push branches main" = cada vez que hagas git push a main
   • "workflow_dispatch" = te permite ejecutarlo manualmente desde GitHub


```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```
→ PERMISOS necesarios para:
   • Leer contenido del repositorio
   • Escribir en GitHub Pages
   • Genera token de seguridad automático


```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```
→ CONTROL DE CONCURRENCIA:
   • Solo 1 deploy a la vez (evita conflictos)
   • Si hay 2 push rápidos, espera a que termine el primero


```yaml
jobs:
  deploy:
```
→ Declara el TRABAJO (job) llamado "deploy"


```yaml
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
```
→ ENTORNO:
   • name: github-pages = entorno de GitHub Pages
   • url: muestra la URL de tu sitio después de desplegar


```yaml
    runs-on: ubuntu-latest
```
→ MÁQUINA donde se ejecuta el workflow
   • ubuntu-latest = Linux (gratis, recomendado)


```yaml
      - name: Checkout
        uses: actions/checkout@v4
```
→ PASO 1: Descargar tu código
   • actions/checkout@v4 = acción oficial de GitHub
   • Descarga el contenido de tu repo


```yaml
      - name: Setup Pages
        uses: actions/configure-pages@v4
```
→ PASO 2: Configurar GitHub Pages
   • Setup Pages = activa GitHub Pages automáticamente
   • Prepara todo para publicar


```yaml
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
```
→ PASO 3: Subir archivos
   • path: '.' = sube TODO el contenido raíz (.)
   • Esto incluye: index.html, css/, js/, assets/, etc.
   • NO sube .github/, .git/, node_modules/, etc. (automáticamente ignorados)


```yaml
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
→ PASO 4: Publicar a GitHub Pages
   • id: deployment = guarda el resultado en esta variable
   • Publica en https://usuario.github.io/repo/ (o dominio personalizado)


════════════════════════════════════════════════════════════════════════════════
              🔧 CONFIGURACIÓN EN GITHUB — PASOS QUE DEBES HACER
════════════════════════════════════════════════════════════════════════════════

PASO 1: Verificar que el archivo .github/workflows/deploy.yml existe

1. Ve a tu repositorio: https://github.com/fabiancacuango1-dev/fismatt-store
2. Haz clic en "Add file" → "Create new file"
3. Escribe la ruta: `.github/workflows/deploy.yml`
4. Pega el contenido del archivo deploy.yml
5. Commit: "Create deploy workflow"

O si ya lo creé localmente (ya está hecho):

   git add .github/workflows/deploy.yml
   git commit -m "Add GitHub Actions deploy workflow"
   git push


PASO 2: Activar GitHub Pages en configuración

1. Ve a tu repositorio
2. Settings → Pages
3. Busca "Build and deployment"
4. Source: selecciona "GitHub Actions" (IMPORTANTE)
5. No toques nada más, guarda automáticamente


PASO 3: Verificar que index.html está en raíz

1. Abre tu repo en GitHub
2. Debe verse: index.html en la raíz (no dentro de carpeta)
   ✅ Correcto:
      /index.html
      /css/styles.css
      /js/main.js

   ❌ Incorrecto:
      /src/index.html (NO, debe estar en raíz)


PASO 4: Configurar dominio personalizado (si usas fis-matt.com)

1. Settings → Pages
2. Custom domain: escribe "fis-matt.com"
3. GitHub creará automáticamente un archivo CNAME
4. En tu registrador de dominio (donde compraste fis-matt.com):
   - Ve a DNS
   - Agrega CNAME record:
     Nombre: @ (o leave blank)
     Valor: fabiancacuango1-dev.github.io
   - Espera 24 horas para propagación


════════════════════════════════════════════════════════════════════════════════
                    ⚡ VERIFICAR QUE EL WORKFLOW FUNCIONA
════════════════════════════════════════════════════════════════════════════════

MÉTODO 1: Ver el workflow en GitHub (RECOMENDADO)

1. Ve a tu repo: https://github.com/fabiancacuango1-dev/fismatt-store
2. Haz clic en "Actions"
3. Busca "Deploy a GitHub Pages"
4. Si ves un ✅ verde, significa que funcionó
5. Si ves una ❌ roja, haz clic para ver el error

MÉTODO 2: Probar el deploy manualmente

1. Haz una pequeña modificación local:
   - Abre index.html
   - Cambia algo pequeño (ej: un comentario)
   
2. Push:
   git add .
   git commit -m "Test deploy workflow"
   git push

3. Ve a Actions y observa:
   • Debe mostrar "Deploy a GitHub Pages" en progreso
   • Espera 1-2 minutos
   • Debe cambiar a ✅ (check)

MÉTODO 3: Ejecutar workflow manualmente

1. Ve a Actions
2. Selecciona "Deploy a GitHub Pages"
3. Haz clic en "Run workflow"
4. Selecciona "main branch"
5. Haz clic en "Run workflow"
6. Observa en "In progress" → espera a que termine


════════════════════════════════════════════════════════════════════════════════
                    💚 ERRORES COMUNES Y CÓMO SOLUCIONARLOS
════════════════════════════════════════════════════════════════════════════════

ERROR 1: "❌ Deploy failed - index.html not found"

CAUSA: index.html no está en la raíz del repo

SOLUCIÓN:
1. Verifica carpeta raíz del repo
2. index.html DEBE estar aquí:
   /index.html (raíz)
   
3. NO debe estar aquí:
   /tienda-online/index.html (carpeta anidada)

Si está en carpeta anidada, debes mover los archivos a raíz.

───────────────────────────────────────────────────────────

ERROR 2: "❌ No such file or directory: .github/workflows/deploy.yml"

CAUSA: El archivo .github/workflows/deploy.yml no existe

SOLUCIÓN:
1. Crea la carpeta: mkdir -p .github/workflows
2. Crea el archivo: deploy.yml
3. Pega el contenido del workflow
4. git add .github/workflows/deploy.yml
5. git commit -m "Add deploy workflow"
6. git push

───────────────────────────────────────────────────────────

ERROR 3: "⏸️ Workflow not running on push"

CAUSA: Maybe:
   • GitHub Actions no está habilitado
   • Branch no es "main" (revisa nombre exacto)
   • Workflow está comentado o deshabilitado

SOLUCIÓN:
1. Settings → Actions → "Allow all actions and reusable workflows"
2. Verifica que la rama sea "main" (no "master" u otro nombre)
3. En deploy.yml, verifica: branches: [ main ]

───────────────────────────────────────────────────────────

ERROR 4: "📄 CSS/JS no cargan" (Página HTML abierta pero sin estilos)

CAUSA: Rutas relativas incorrectas o dominio personalizado mal configurado

SOLUCIÓN:
Opción A - Si usas GitHub Pages estándar:
   Abre DevTools (F12) → Console
   Revisa si aparecen errores 404 en css/ o js/
   Las rutas DEBEN ser relativas:
   • ✅ <link rel="stylesheet" href="css/styles.css">
   • ✅ <script src="js/main.js"></script>

Opción B - Si usas dominio personalizado (fis-matt.com):
   1. Settings → Pages → Custom domain: fis-matt.com
   2. En tu registrador DNS, configura:
      CNAME: fabiancacuango1-dev.github.io
   3. Espera 24 horas
   4. Las rutas relativas funcionarán automáticamente

───────────────────────────────────────────────────────────

ERROR 5: "⚠️ Workflow se ejecuta pero repo muestra 'Your site is ready to be published'"

CAUSA: GitHub Pages no está activado como fuente

SOLUCIÓN:
1. Ve a Settings → Pages
2. Build and deployment → Source: "GitHub Actions"
3. Guarda
4. Ejecuta workflow de nuevo (Actions → Run workflow)

───────────────────────────────────────────────────────────

ERROR 6: "❌ Dominio personalizado no funciona"

CAUSA: DNS no está configurado correctamente

SOLUCIÓN:
1. En tu registrador (GoDaddy, Namecheap, etc.):
   • Busca "DNS Settings"
   • Agrega/modifica CNAME:
     Name: @ o leave blank
     Value: fabiancacuango1-dev.github.io
   
2. Si necesitas @ (root):
   • Algunos registradores no permiten CNAME en @
   • Usa A records en su lugar:
     A Record: 185.199.110.153
     A Record: 185.199.111.153
     A Record: 185.199.112.153
     A Record: 185.199.113.153

3. En GitHub Settings → Pages:
   • Custom domain: fis-matt.com
   • Habilita "Enforce HTTPS"

4. Espera 24-48 horas para propagación DNS


════════════════════════════════════════════════════════════════════════════════
                    📊 FLUJO COMPLETO: QUÉ PASA CUANDO HACES GIT PUSH
════════════════════════════════════════════════════════════════════════════════

TÚ (en tu máquina local):
────────────────────────
$ git add .
$ git commit -m "cambios"
$ git push
        ↓
        ↓

GITHUB (automáticamente):
──────────────────────────
1. Recibe tu código
2. Detecta push a rama "main"
3. Ve archivo .github/workflows/deploy.yml
4. Inicia el workflow "Deploy a GitHub Pages"
   
   [✓] Checkout - Descarga código
   [✓] Setup Pages - Prepara GitHub Pages
   [✓] Upload artifact - Sube archivos (index.html, css/, js/, assets/)
   [✓] Deploy to GitHub Pages - Publica en línea

5. Se muestra en Actions tab con ✅ verde

RESULTADO:
──────────
Tu sitio estáactualizado en:
• https://fabiancacuango1-dev.github.io/fismatt-store/
  O
• https://fis-matt.com/ (si configuraste dominio)

TODO AUTOMÁTICO. Tú no haces nada.


════════════════════════════════════════════════════════════════════════════════
                    ✅ CHECKLIST FINAL — VERIFICACIÓN ANTES DE USAR
════════════════════════════════════════════════════════════════════════════════

ANTES DE HACER EL PRIMER GIT PUSH, VERIFICA:

Estructura del repositorio:
☐ index.html está en RAÍZ (no en carpeta)
☐ css/ está en RAÍZ
☐ js/ está en RAÍZ
☐ assets/ está en RAÍZ
☐ .github/workflows/deploy.yml existe

Contenido de index.html:
☐ <link rel="stylesheet" href="css/styles.css"> (ruta relativa)
☐ <script src="js/main.js"></script> (ruta relativa)
☐ Favicon: <link rel="icon" href="assets/img/favicon.svg">

Configuración local:
☐ Git inicializado: git init ✅
☐ Remoto configurado: git remote add origin https://github.com/fabiancacuango1-dev/fismatt-store.git ✅
☐ Rama principal es "main" (no "master"): git branch -M main ✅

Configuración en GitHub:
☐ Repositorio creado en GitHub ✅
☐ Code push realizado: git push -u origin main ✅
☐ Settings → Pages → Source: "GitHub Actions" ✅
☐ .github/workflows/deploy.yml presente en GitHub ✅

Dominio personalizado (opcional):
☐ Si usas fis-matt.com:
   ☐ Settings → Pages → Custom domain: fis-matt.com ✅
   ☐ DNS configurado en registrador ✅
   ☐ CNAME o A records agregados ✅


════════════════════════════════════════════════════════════════════════════════
                    🎯 PRÓXIMOS PASOS — AHORA QUÉ
════════════════════════════════════════════════════════════════════════════════

PASO 1: Asegúrate que .github/workflows/deploy.yml está en tu repo local

Si recibiste este archivo en local:
   ls -la .github/workflows/
   
Debe mostrar: deploy.yml

PASO 2: Haz push de los cambios

$ git add .
$ git commit -m "Configure GitHub Actions deploy workflow"
$ git push

PASO 3: Ve a Actions en GitHub

Abre: https://github.com/fabiancacuango1-dev/fismatt-store/actions

Busca: "Deploy a GitHub Pages"

Si ves ✅ verde = ¡FUNCIONA!

PASO 4 (Dominio personalizado)

Si usas fis-matt.com:

En GitHub:
   Settings → Pages → Custom domain → fis-matt.com → Save

En tu registrador de dominio:
   Agrega CNAME: fabiancacuango1-dev.github.io
   Espera 24 horas

PASO 5: Prueba con un cambio pequeño

1. Modifica index.html
2. git add .
3. git commit -m "Test deploy"
4. git push
5. Observa Actions
6. Tu web se actualiza automáticamente 🎉


════════════════════════════════════════════════════════════════════════════════
                         🎓 RESUMEN TÉCNICO
════════════════════════════════════════════════════════════════════════════════

QUÉ ES GITHUB ACTIONS:
─────────────────────
Servidor de GitHub que ejecuta scripts automáticamente cuando haces push.
En tu caso: copia tus archivos a GitHub Pages.

POR QUÉ ES MEJOR QUE HACER PUSH MANUALMENTE:
──────────────────────────────────────────
❌ Forma vieja: Tenías que compilar + publican por FTP/SFTP
✅ Forma nueva: git push = todo se actualiza automático

VENTAJAS:
─────────
✅ Zero-configuration
✅ Gratis
✅ Automático
✅ Rápido (1-2 minutos)
✅ Sin dependencias (HTML puro)
✅ Funciona con dominios personalizados
✅ Incluye HTTPS gratis

CÓMO FUNCIONA EN TU CASO:
────────────────────────
1. Haces cambios locales
2. git push
3. GitHub descarga tu código
4. Ejecuta la acción: checkout → setup pages → upload → deploy
5. Tu sitio está online (2 minutos después)
6. Al visitarlo, ves los cambios nuevos


════════════════════════════════════════════════════════════════════════════════
                         📞 SOPORTE Y RECURSOS
════════════════════════════════════════════════════════════════════════════════

Si algo no funciona:

1. Actions tab: https://github.com/fabiancacuango1-dev/fismatt-store/actions
   Haz clic en el workflow fallido para ver el error exacto

2. Documentación oficial:
   https://docs.github.com/en/pages/getting-started-with-github-pages/quickstart

3. GitHub Actions docs:
   https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-github-pages

4. Troubleshooting Pages:
   https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-custom-domains-and-github-pages


════════════════════════════════════════════════════════════════════════════════
                              IMPORTANTE
════════════════════════════════════════════════════════════════════════════════

❗ NO MODIFICAR deploy.yml en GitHub manualmente
   → Siempre edita localmente y haz git push

❗ NO Eliminar .github/ carpeta
   → La necesitas para que funcione el workflow

❗ Mantén index.html siempre en RAÍZ
   → No lo muevas a subcarpeta

❗ Si cambias nombre de rama (main → master, etc.)
   → Actualiza "branches: [ main ]" en deploy.yml

================================================== ========================

Configurado por: GitHub Copilot
Fecha: 29 de marzo de 2026
Versión: 1.0
Estado: ✅ LISTO PARA USO
