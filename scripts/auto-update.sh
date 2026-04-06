#!/bin/bash

# AUTO-UPDATE SCRIPT - FISMATT SYSTEMS
# Detecta nuevas versiones en GitHub y actualiza fis-matt.com automáticamente

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$PROJECT_DIR/config/products.json"
INDEX_HTML="$PROJECT_DIR/index.html"
GITHUB_API="https://api.github.com/repos/fabiancacuango1-dev/fismatt-store/releases"

echo -e "${YELLOW}🔄 FISMATT AUTO-UPDATE CHECKER${NC}"
echo "======================================="

# Función para obtener latest release de GitHub
get_latest_release() {
    local repo=$1
    curl -s "$GITHUB_API/latest" | grep '"tag_name"' | head -1 | sed -E 's/.*"([^"]+)".*/\1/'
}

# Función para actualizar products.json
update_version() {
    local product=$1
    local new_version=$2
    local new_url=$3
    
    echo -e "${YELLOW}Actualizando $product a versión $new_version${NC}"
    
    # Usar jq para actualizar JSON (si está instalado)
    if command -v jq &> /dev/null; then
        jq ".products.$product.version = \"$new_version\" | .products.$product.url = \"$new_url\" | .metadata.lastUpdate = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$CONFIG_FILE" > "${CONFIG_FILE}.tmp"
        mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
        echo -e "${GREEN}✅ $product actualizado en products.json${NC}"
    else
        echo -e "${RED}❌ jq no instalado. Actualización manual requerida.${NC}"
        return 1
    fi
}

# Función para hacer commit y push a GitHub
deploy_changes() {
    cd "$PROJECT_DIR"
    
    git add config/products.json
    git commit -m "🔄 Auto-update: EduHorarios y productos nuevas versiones

Detectadas nuevas versiones en GitHub Releases:
- Versiones actualizadas automáticamente
- config/products.json sincronizado
- Timestamp: $(date)

Changeset generado por: fismatt-auto-update-script"
    
    git push origin main
    echo -e "${GREEN}✅ Deploy a producción completado${NC}"
}

# Get latest release from GitHub
LATEST_TAG=$(get_latest_release "fismatt-store")
CURRENT_VERSION=$(grep -o '"version": "[^"]*"' "$CONFIG_FILE" | head -1 | sed 's/.*"\([^"]*\)".*/\1/')

echo -e "Versión actual: ${YELLOW}$CURRENT_VERSION${NC}"
echo -e "Última en GitHub: ${YELLOW}$LATEST_TAG${NC}"

if [ "$LATEST_TAG" != "$CURRENT_VERSION" ]; then
    echo -e "${GREEN}✅ Nueva versión detectada!${NC}"
    
    # Actualizar EduHorarios
    EDUHORARIOS_URL="https://github.com/fabiancacuango1-dev/fismatt-store/releases/download/${LATEST_TAG}/EduHorarios-AI-${LATEST_TAG}.zip"
    update_version "eduhorarios" "$LATEST_TAG" "$EDUHORARIOS_URL"
    
    # Actualizar otros productos
    IMPORTADOR_URL="https://github.com/fabiancacuango1-dev/fismatt-store/releases/download/${LATEST_TAG}/ImportadorNotas-Setup.zip"
    update_version "importador-minduc" "$LATEST_TAG" "$IMPORTADOR_URL"
    
    INEVAL_URL="https://github.com/fabiancacuango1-dev/fismatt-store/releases/download/${LATEST_TAG}/INEVAL-PRO-${LATEST_TAG}.zip"
    update_version "ineval-pro" "$LATEST_TAG" "$INEVAL_URL"
    
    # Deploy a producción
    deploy_changes
    
    echo -e "${GREEN}🚀 Auto-update completado y desplegado!${NC}"
else
    echo -e "${YELLOW}ℹ️  Sin cambios. Versión actual es la más reciente.${NC}"
fi

echo "======================================="
echo -e "${GREEN}Script finalizado exitosamente${NC}"
