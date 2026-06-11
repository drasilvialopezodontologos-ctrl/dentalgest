#!/bin/bash
# ============================================================
#  DentalGest — Copia archivos del Mac a la Raspberry Pi
#  Ejecutar desde tu Mac cuando tengas la Pi en la red
#
#  Uso:  bash copiar_a_pi.sh 192.168.1.XX
#        (reemplaza XX con la IP de tu Pi)
# ============================================================

PI_IP="${1}"

if [ -z "$PI_IP" ]; then
    echo "❌  Debes indicar la IP de la Pi"
    echo "    Uso: bash copiar_a_pi.sh 192.168.1.XX"
    exit 1
fi

CARPETA_LOCAL="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "→ Copiando DentalGest a la Raspberry Pi ($PI_IP)..."
echo "  (te pedirá la contraseña de la Pi — por defecto es 'raspberry')"
echo ""

# Crear carpeta en la Pi y copiar todo
ssh pi@$PI_IP "mkdir -p /home/pi/DentalGest"
rsync -avz --progress \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    "$CARPETA_LOCAL/" "pi@$PI_IP:/home/pi/DentalGest/"

echo ""
echo "✅  Archivos copiados"
echo ""
echo "→ Ahora en la Pi ejecuta:"
echo "   bash /home/pi/DentalGest/instalar_pi.sh"
echo ""
