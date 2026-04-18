#!/bin/zsh
# ============================================
# FISMATT SYSTEMS — Release Manager
# Sube nuevas versiones de instaladores a GitHub Releases
# ============================================
#
# USO:
#   ./scripts/release.sh <version>
#
# EJEMPLOS:
#   ./scripts/release.sh v2.1.0
#   ./scripts/release.sh v3.0.0
#
# REQUISITOS:
#   - gh CLI instalado y autenticado
#   - Archivos en carpeta /instaladores/
#   - Nombrar archivos así:
#       SistemaAcademico-v<VERSION>-Setup.exe    (Windows)
#       SistemaAcademico-v<VERSION>-macOS.dmg    (Mac)
#
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Check arguments
if [[ -z "$1" ]]; then
    echo "${RED}❌ Error: Debes especificar la versión${NC}"
    echo ""
    echo "Uso: ./scripts/release.sh v2.1.0"
    echo ""
    echo "Versiones existentes:"
    gh release list --limit 10
    exit 1
fi

VERSION="$1"
INSTALADORES_DIR="$PROJECT_DIR/instaladores"

echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${YELLOW}★ FISMATT SYSTEMS — Release Manager${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Versión: ${GREEN}$VERSION${NC}"
echo ""

# Check instaladores folder
if [[ ! -d "$INSTALADORES_DIR" ]]; then
    echo "${RED}❌ No existe la carpeta /instaladores/${NC}"
    exit 1
fi

# Find installer files
WINDOWS_FILE=$(find "$INSTALADORES_DIR" -name "*.exe" -type f | head -1)
MAC_FILE=$(find "$INSTALADORES_DIR" -name "*.dmg" -type f | head -1)

ASSETS=()

if [[ -n "$WINDOWS_FILE" ]]; then
    WIN_SIZE=$(du -h "$WINDOWS_FILE" | cut -f1 | tr -d ' ')
    echo "${GREEN}✓ Windows: $(basename "$WINDOWS_FILE") ($WIN_SIZE)${NC}"
    ASSETS+=("$WINDOWS_FILE")
else
    echo "${YELLOW}⚠ No se encontró instalador Windows (.exe)${NC}"
fi

if [[ -n "$MAC_FILE" ]]; then
    MAC_SIZE=$(du -h "$MAC_FILE" | cut -f1 | tr -d ' ')
    echo "${GREEN}✓ macOS:   $(basename "$MAC_FILE") ($MAC_SIZE)${NC}"
    ASSETS+=("$MAC_FILE")
else
    echo "${YELLOW}⚠ No se encontró instalador Mac (.dmg)${NC}"
fi

if [[ ${#ASSETS[@]} -eq 0 ]]; then
    echo "${RED}❌ No hay archivos para subir en /instaladores/${NC}"
    exit 1
fi

echo ""

# Check if release already exists
if gh release view "$VERSION" > /dev/null 2>&1; then
    echo "${YELLOW}⚠ La release $VERSION ya existe. Actualizando assets...${NC}"
    for asset in "${ASSETS[@]}"; do
        echo "  Subiendo $(basename "$asset")..."
        gh release upload "$VERSION" "$asset" --clobber
    done
else
    echo "${BLUE}📦 Creando release $VERSION...${NC}"
    
    NOTES="## 🎓 Sistema Académico Completo $VERSION

**Producto Estrella — Promoción de Apertura: \$35**

### Incluye:
- ✅ Control de Estudiantes y Asistencia (individual/grupal)
- ✅ Sistema de Notas (individuales, grupales, trimestrales, anuales)
- ✅ Módulo de Docentes (horarios, tareas, trabajos)
- ✅ Informes Personalizados por Institución
- ✅ Ficha del Estudiante y Respaldos Automáticos
- ✅ Personalización Completa

### Descargas:"

    if [[ -n "$WINDOWS_FILE" ]]; then
        NOTES="$NOTES
- **Windows**: $(basename "$WINDOWS_FILE") ($WIN_SIZE)"
    fi
    if [[ -n "$MAC_FILE" ]]; then
        NOTES="$NOTES
- **macOS**: $(basename "$MAC_FILE") ($MAC_SIZE)"
    fi

    NOTES="$NOTES

Basado en los lineamientos del Ministerio de Educación del Ecuador."

    gh release create "$VERSION" \
        --title "Sistema Académico Completo $VERSION — Windows + Mac" \
        --notes "$NOTES" \
        "${ASSETS[@]}"
fi

echo ""
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}✅ Release $VERSION subida exitosamente${NC}"
echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show download URLs
echo "${BLUE}URLs de descarga directa:${NC}"
gh release view "$VERSION" --json assets --jq '.assets[] | "  → \(.name): \(.url)"'

echo ""
echo "${YELLOW}📋 Próximos pasos:${NC}"
echo "  1. Actualiza los links en index.html si cambió el nombre del archivo"
echo "  2. Ejecuta: git add . && git commit -m 'Release $VERSION' && git push origin main"
echo ""
echo "${BLUE}Historial de releases:${NC}"
gh release list --limit 5
