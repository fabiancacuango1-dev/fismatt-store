# Guia de Despliegue a Produccion — SoftPlugin Pro

## Pre-Deploy Checklist

### 1. Archivos Listos
- [x] `index.html` — Estructura corregida y optimizada
- [x] `css/styles.css` — Estilos personalizados
- [x] `js/main.js` — JavaScript funcional con sanitizacion
- [x] `assets/downloads/ImportadorNotas-Setup.zip` — Archivo de descarga real
- [x] `assets/img/favicon.svg` — Favicon

### 2. Archivos Pendientes de Crear (Recomendado)
- [ ] `assets/img/og-image.png` — Imagen para redes sociales (1200x630px). Sin esta imagen, los links compartidos en redes no mostraran preview.

---

## Opcion A: Deploy en Netlify (Recomendado — Gratis)

1. Ve a [app.netlify.com](https://app.netlify.com)
2. Crea una cuenta o inicia sesion
3. Arrastra la carpeta completa `tienda online` al area de Deploy
4. Netlify te dara una URL tipo `https://tu-nombre.netlify.app`
5. En **Domain Settings** puedes conectar tu dominio `softpluginpro.com`

## Opcion B: Deploy en Vercel (Gratis)

1. Ve a [vercel.com](https://vercel.com)
2. Sube el proyecto desde GitHub o arrastra la carpeta
3. Obtendras una URL tipo `https://tu-proyecto.vercel.app`

## Opcion C: Deploy en GitHub Pages (Gratis)

1. Crea un repositorio en GitHub
2. Sube todos los archivos
3. Ve a Settings > Pages > Source: main branch
4. Tu sitio estara en `https://tu-usuario.github.io/tu-repo`

## Opcion D: Hosting Tradicional (cPanel, etc.)

1. Accede al panel de tu hosting via cPanel o FTP
2. Sube todos los archivos a la carpeta `public_html` o `www`
3. Asegurate de que `index.html` este en la raiz

---

## Post-Deploy Checklist

- [ ] Verificar que la pagina carga correctamente
- [ ] Probar el boton de descarga (debe descargar `ImportadorNotas-Setup.zip`)
- [ ] Probar el boton de WhatsApp (debe abrir chat con +593983274499)
- [ ] Probar el formulario de contacto (debe abrir cliente de correo)
- [ ] Verificar en movil que el menu hamburguesa funciona
- [ ] Abrir en Chrome DevTools > Lighthouse para ver puntuacion SEO
- [ ] Compartir la URL en WhatsApp/Facebook para verificar la preview (Open Graph)

---

## Configuracion de Dominio Personalizado

Si tienes el dominio `softpluginpro.com`:

1. En tu proveedor de dominio, configura los DNS:
   - **Para Netlify**: Agrega un registro CNAME apuntando a `tu-nombre.netlify.app`
   - **Para Vercel**: Agrega un registro CNAME apuntando a `cname.vercel-dns.com`
2. Activa HTTPS (gratuito en Netlify y Vercel)
3. Actualiza la URL canonica en `index.html` si es diferente

---

## Notas Importantes

- El sitio usa **Tailwind CSS via CDN** — funciona sin build process
- No requiere Node.js, npm ni ningun framework backend
- Todo es estatico: HTML + CSS + JS + archivos
- El archivo de descarga pesa lo que pese el ZIP — asegurate de que tu hosting permita ese tamano
