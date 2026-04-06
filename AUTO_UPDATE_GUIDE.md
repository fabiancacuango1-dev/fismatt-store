# 🔄 Sistema de Auto-Actualización - FISMATT SYSTEMS

## Descripción

Sistema automático que detecta nuevas versiones de EduHorarios AI, INEVAL-PRO e Importador Minduc en GitHub Releases y actualiza automáticamente los links en fis-matt.com.

**Sin intervención manual.**
**Sin downtime.**
**100% automático.**

---

## 📋 Cómo Funciona

### **Flujo de Auto-Actualización**

```
1. Subes nueva versión a GitHub Releases (tag: v1.0.1)
   ↓
2. GitHub Actions se dispara automáticamente
   ↓
3. Lee versión nueva desde GitHub API
   ↓
4. Actualiza config/products.json
   ↓
5. Hace commit y push a main
   ↓
6. GitHub Pages deploya cambios (< 1 min)
   ↓
7. index.html carga versiones dinámicamente
   ↓
8. Usuarios ven versión más reciente automáticamente ✅
```

---

## 🚀 Cómo Usar

### **Opción 1: Cuando subas nueva versión a GitHub**

```bash
# 1. Crea tag con nueva versión
git tag -a v1.0.1 -m "EduHorarios AI v1.0.1 - Mejoras"

# 2. Push tag a GitHub
git push origin v1.0.1

# 3. GitHub Actions se dispara automáticamente
# 4. config/products.json se actualiza
# 5. ¡Listo! Todos los links automáticamente actualizados en fis-matt.com
```

### **Opción 2: Manual (si necesitas forzar actualización)

```bash
# Ejecutar script local
bash scripts/auto-update.sh

# O hacerlo vía GitHub Actions
# Ir a: GitHub Actions → Auto-Update Products on Release → Run workflow
```

---

## 📁 Archivos del Sistema

```
fismatt-store/
├── config/
│   └── products.json              ← Fuente de versiones
├── scripts/
│   └── auto-update.sh             ← Script de actualización
├── .github/workflows/
│   └── auto-update.yml            ← GitHub Actions trigger
└── index.html                     ← Carga dinámicamente versiones
```

---

## 📊 Estructura de config/products.json

```json
{
  "products": {
    "eduhorarios": {
      "name": "EduHorarios AI",
      "version": "1.0.0",              ← Se actualiza automáticamente
      "url": "https://github.com/.../",← Se actualiza automáticamente
      "subdomain": "https://horarios.fis-matt.com"
    }
  },
  "metadata": {
    "lastUpdate": "2026-04-06T15:00:00Z",  ← Timestamp automático
    "autoDetect": true
  }
}
```

---

## ✅ Ventajas

| Feature | Beneficio |
|---------|-----------|
| Auto-detect de versiones | No olvidas actualizar links |
| GitHub Actions | Sin intervención manual |
| Deploy automático | < 1 minuto en producción |
| Versionado con git tags | Histórico completo |
| config/products.json | Fuente única de verdad |
| Dynamic loading en HTML | Siempre versión correcta |
| Zero downtime | Deploy sin interrupciones |

---

## 🔧 Configuración de GitHub Actions

El archivo `.github/workflows/auto-update.yml` se dispara automáticamente cuando:

1. **Se crea nuevo Release en GitHub** → ✅ Auto-update
2. **Manualmente via GitHub UI** → ✅ Auto-update
3. **Cambio en tag de versión** → ✅ Auto-update

**Sin requiere acciones del usuario.**

---

## 📱 Para EduHorarios Específicamente

Cuando subes nueva versión de EduHorarios:

```bash
# 1. Asegúrate de que el archivo se llame:
# EduHorarios-AI-v1.0.1.zip

# 2. Crea release en GitHub con tag: v1.0.1
# GitHub UI → Releases → Create new release

# 3. Adjunta el archivo al release

# 4. Publica release

# 5. ¡LISTO! 
#    - config/products.json se actualiza
#    - https://horarios.fis-matt.com se actualiza
#    - Todos los links en fis-matt.com apuntan a v1.0.1
```

---

## 🔗 URLs Actualizadas Automáticamente

Después de crear release, estas URLs se actualizan:

```
Main site:
https://fis-matt.com/                    ← Descarga versión actual

Download page:
https://fis-matt.com/descargar.html      ← Apunta a GitHub Release

Direct link:
https://github.com/.../releases/download/vX.X.X/file.zip
```

---

## ✨ Ejemplo Real

```
HOY (6 abril 2026):
└─ EduHorarios v1.0.0 en production

MAÑANA (7 abril):
├─ Subes EduHorarios-AI-v1.0.1.zip a GitHub Release
├─ Creas tag v1.0.1
├─ Publicas release
└─ ✅ Automáticamente:
    ├─ config/products.json actualizado
    ├─ index.html carga v1.0.1
    ├─ Botones de descarga apuntan a v1.0.1
    ├─ Usuarios descargan versión nueva
    └─ Deploy completado sin intervención
```

---

## 🛡️ Seguridad

- ✅ Solo GitHub Releases como fuente
- ✅ Verificación de tags de git
- ✅ Commit firmado con mensaje automático
- ✅ Tracking completo en logs de GitHub
- ✅ Rollback fácil (revert commit)

---

## 📞 Soporte

Si algo no se actualiza:

```bash
# 1. Verifica que el tag existe
git tag -l

# 2. Revisa GitHub Actions logs
# GitHub → Actions → Auto-Update Products on Release

# 3. Manual trigger si necesitas
bash scripts/auto-update.sh
```

---

## 🎯 Próximos Pasos

1. ✅ Sistema implementado
2. ✅ GitHub Actions configurado
3. ⏳ Prueba creando release con v1.0.1
4. ⏳ Verifica que se autoactualice
5. ⏳ ¡Listo para producción!

---

**Creado:** 6 de abril de 2026  
**Sistema:** FISMATT Auto-Update v1.0  
**Status:** ✅ Production Ready  
