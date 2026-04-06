# 🎯 Restructuración de Tienda Virtual - SoftPlugin Pro

## ✨ Cambios Principales

### 1. **Navegación Actualizada**
La barra de navegación ahora incluye:
- **Inicio** → Sección hero
- **Productos** → ⭐ NUEVA: Tienda virtual con ambos productos
- **Demo en Vivo** → ⭐ NUEVA: Demostraciones en vivo
- **Características** → Características generales
- **Soporte** → Canales de atención
- **FAQ** → Preguntas frecuentes

---

## 📦 Nueva Sección: Tienda Virtual

### Localización
- **URL anchor**: `#productos`
- **Posición**: Después del hero, antes de características

### Estructura
```
TIENDA VIRTUAL
├── Encabezado
├── Producto 1: INEVAL-PRO
│   ├── Icono (Analytics Chart)
│   ├── Badge: "Simulador"
│   ├── Título y descripción
│   ├── 4 Características clave
│   └── Botón CTA → https://ineval-pro.web.app
│
└── Producto 2: SoftPlugin Pro
    ├── Icono (Lightning Bolt)
    ├── Badge: "Extensión"
    ├── Título y descripción
    ├── 4 Características clave
    └── Botón CTA → https://chromewebstore.google.com/...
```

### Diseño
- **Layout**: Grid responsivo (2 columnas en desktop, 1 en mobile)
- **Tarjetas**: Glassmorphism con backdrop blur
- **Efectos Hover**: Glow colorido + shadow elevation
- **Colores**:
  - INEVAL-PRO: Primario (Indigo) → Acento (Purple)
  - SoftPlugin: Acento (Purple) → Secundario (Cyan)

---

## 🎬 Nueva Sección: Demo en Vivo

### Localización
- **URL anchor**: `#live`
- **Posición**: Después de productos, antes de características

### Estructura
```
DEMO EN VIVO
├── Encabezado
├── Tarjeta 1: INEVAL-PRO
│   ├── Thumbnail con icono play
│   ├── Descripción
│   └── "Acceder Ahora" → https://ineval-pro.web.app
│
└── Tarjeta 2: SoftPlugin Pro
    ├── Thumbnail con icono play
    ├── Descripción
    └── "Instalar Ahora" → https://chromewebstore.google.com/...
```

---

## 🔗 URLs de los Productos

### INEVAL-PRO (Simulador)
```
https://ineval-pro.web.app
```
**Características:**
- Miles de preguntas actualizadas
- Análisis detallado de resultados
- Acceso desde cualquier dispositivo
- Interfaz intuitiva y moderna

### SoftPlugin Pro (Plugin/Extensión)
```
https://chromewebstore.google.com/detail/pjdakeeclfpkheobgmenlonbbpmokbbh
```
**Características:**
- Automatización inteligente
- Compatible con todos los navegadores Chromium
- 100% Seguro y con privacidad
- Soporte dedicado 24/7

---

## 📊 Flujo de Navegación

```
INICIO (Hero)
    ↓
[Click "Ir a Tienda"] o [Navbar "Productos"]
    ↓
TIENDA VIRTUAL (#productos)
├── Producto 1 → Click → https://ineval-pro.web.app
├── Producto 2 → Click → https://chromewebstore.google.com/...
    ↓
[Opcional: Ver Demo en Vivo]
    ↓
DEMO EN VIVO (#live)
├── INEVAL-PRO → Click → https://ineval-pro.web.app
├── SoftPlugin → Click → https://chromewebstore.google.com/...
    ↓
[Opcional: Explorar más características]
    ↓
CARACTERÍSTICAS (#caracteristicas)
```

---

## 🎨 Estilos Visuales

### Colores Primarios
- **Primario**: #6366f1 (Indigo)
- **Acento**: #8b5cf6 (Purple)
- **Secundario**: #0ea5e9 (Cyan)
- **Fondo**: #0f172a (Dark Blue)

### Efectos en Hover
1. Glow box-shadow con color del gradiente
2. Border highlight (+/20 opacity)
3. Elevación suave (-translate-y-0.5)
4. Escala de icono (1.1x)

### Animaciones
- Fade-in al scroll (Intersection Observer)
- Stagger delay por elemento
- Smooth transitions (300ms)

---

## 📱 Responsive

- **Desktop**: 2 columnas en grid
- **Tablet**: Ajuste automático
- **Mobile**: 1 columna, full width

---

## 🚀 Cómo Ver los Cambios

1. **Abre** `index.html` en tu navegador
2. **Navega** a "Productos" desde el menú
3. **Explora** las tarjetas interactivas
4. **Haz clic** en los botones para acceder a cada producto
5. **Prueba** en móvil para ver diseño responsive

---

## 📝 Archivos Modificados

- ✅ `index.html` - Agregar secciones, actualizar navbar/footer
- ✅ `js/main.js` - Compatible (sin cambios necesarios)
- ✅ `css/styles.css` - Compatible (sin cambios necesarios)

---

## ✅ Checklist del Proyecto

- ✅ Sección #productos creada
- ✅ Sección #live creada
- ✅ Navbar actualizado (Productos, Demo)
- ✅ Footer actualizado
- ✅ CTA principal apunta a #productos
- ✅ Ambos URLs de productos funcionales
- ✅ Características listadas en tarjetas
- ✅ Diseño elegante y productivo
- ✅ Responsive (mobile + desktop)
- ✅ Animaciones suaves

---

## 💡 Ideas Futuras

1. Agregar carrito de compras (si hay versiones de pago)
2. Sistema de reviews/testimonios de usuarios
3. Comparativa lado-a-lado de productos
4. Newsletter signup integrado
5. Blog con tutoriales de cada producto
6. Programa de afiliados

---

**Última actualización:** 28 de marzo de 2026  
**Versión**: 2.0 (Con tienda virtual)
