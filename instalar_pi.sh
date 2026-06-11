#!/bin/bash
# ============================================================
#  DentalGest — Instalador para Raspberry Pi
#  Ejecutar UNA sola vez después de copiar la carpeta DentalGest
#  en /home/pi/DentalGest
#
#  Uso:  bash instalar_pi.sh
# ============================================================

set -e

CARPETA="/home/pi/DentalGest"
SERVICIO="dentalgest"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Instalando DentalGest en la Pi     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Verificar que estamos en la carpeta correcta
if [ ! -f "$CARPETA/server.py" ]; then
    echo "❌  No se encontró $CARPETA/server.py"
    echo "    Copia la carpeta DentalGest a /home/pi/ primero."
    exit 1
fi

# Instalar Python si no está
echo "→ Verificando Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "  Instalando Python 3..."
    sudo apt-get update -qq
    sudo apt-get install -y python3
fi
echo "  ✅ Python 3 listo"

# Copiar el servicio systemd
echo "→ Configurando auto-inicio..."
sudo cp "$CARPETA/dentalgest.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICIO
sudo systemctl restart $SERVICIO
echo "  ✅ Servicio instalado y activo"

# Obtener IP
IP=$(python3 -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()" 2>/dev/null || echo "desconocida")

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅  DentalGest instalado correctamente              ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║                                                      ║"
echo "║  Abre en cualquier computador de la red:             ║"
echo "║                                                      ║"
echo "║  ➜  http://$IP:7890"
echo "║                                                      ║"
echo "║  El servidor arranca automáticamente cuando          ║"
echo "║  se enciende la Raspberry Pi.                        ║"
echo "║                                                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Comandos útiles:"
echo "  Ver estado:   sudo systemctl status dentalgest"
echo "  Ver logs:     sudo journalctl -u dentalgest -f"
echo "  Reiniciar:    sudo systemctl restart dentalgest"
echo ""
