# 🔧 PLAN DE CORRECCIONES INMEDIATAS

**Objetivo:** Convertir "sospechoso" → "profesional" en 3-4 horas de trabajo

---

## FASE 1: CREAR ARCHIVOS LEGALES (30 minutos)

### Archivo 1: `legal/privacidad.html`
**Descripción:** Política de privacidad según GDPR/RGPD + Ecuador

### Archivo 2: `legal/terminos.html`
**Descripción:** Términos y condiciones de uso

### Archivo 3: `legal/cookies.html` (bonus)
**Descripción:** Política de cookies

---

## FASE 2: CORRECCIONES EN index.html (1 hora)

### Cambio 1: Meta Tags & Schema Coherentes
```html
<!-- Cambiar og:description para ser consistente -->
<!-- Cambiar applicationCategory en schema -->
<!-- Cambiar operatingSystem en schema -->
```

### Cambio 2: Agregar Información Legal en Footer
```html
<!-- Enlaces a las nuevas páginas de legal -->
```

### Cambio 3: Hacer Funcional el Formulario
```javascript
<!-- Agregar handler de formulario -->
<!-- Conectar con email service (FormSubmit o Netlify) -->
```

### Cambio 4: Arreglar Links Externos
```html
<!-- Cambiar target="_blank" a abrir en misma ventana O -->
<!-- Cambiar de redirecciones a modals/previews locales -->
```

---

## FASE 3: CREAR ARCHIVOS TÉCNICOS (1 hora)

### Archivo 4: `/robots.txt`
```
User-agent: *
Allow: /
Sitemap: https://fis-matt.com/sitemap.xml
Disallow: /assets/    
```

### Archivo 5: `/sitemap.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Listado de URLs -->
</urlset>
```

### Archivo 6: Crear `og-image.png`
```
Imagen 1200x630px con:
- Logo FISMATT
- "Soluciones Educativas Ecuador"
- Colores: azul #1e40af, amarillo #fbbf24
```

---

## FASE 4: AGREGAR CREDIBILIDAD (30 minutos)

### Sección 1: Información Empresarial en Footer
```html
<footer>
  <div>
    <strong>FISMATT SYSTEMS</strong>
    <p>Empresa ecuatoriana de soluciones educativas</p>
    <p>RUC: [Tu RUC aquí]</p>
    <p>Ubicación: Ecuador</p>
  </div>
</footer>
```

### Sección 2: Testimonios Verificables
```html
<section id="testimonios">
  <!-- 3-5 testimonios reales con foto + nombre + institución -->
</section>
```

---

## TIMELINE

```
Hora 0:00 - 0:30    CREAR policies (copiar templates)
Hora 0:30 - 1:30    CORREGIR index.html meta tags + schema
Hora 1:30 - 1:45    IMPLEMENTAR formulario funcional
Hora 1:45 - 2:15    CREAR robots.txt + sitemap.xml
Hora 2:15 - 2:45    DISEÑAR og-image.png
Hora 2:45 - 3:00    TESTING Y VERIFICACIÓN

RESULTADO: Sitio listo para no-bloqueo en TikTok
```

---

## ORDEN DE IMPLEMENTACIÓN

✅ **PRIMERO:** Crear archivos legales (políticas)  
✅ **SEGUNDO:** Corregir meta tags y schema  
✅ **TERCERO:** Hacer funcional formulario  
✅ **CUARTO:** Crear robots.txt + sitemap.xml  
✅ **QUINTO:** Diseñar y agregar og-image  
✅ **SEXTO:** Agregar sección de testimoni os  
✅ **SÉPTIMO:** Verificar y testear todo  

---

**LISTO PARA COMENZAR?**

Esperando confirmación para generar archivos específicos.
