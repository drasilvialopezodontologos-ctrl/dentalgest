#!/usr/bin/env python3
"""
DentalGest — servidor local de red
Almacena los datos en data.json en esta misma carpeta.
Ambas computadoras acceden por http://<ip-del-servidor>:7890
Compatible con macOS y Linux (Raspberry Pi)
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, os, threading, sys, socket

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
_lock = threading.Lock()

class DGHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Silenciar logs de archivos estáticos, mostrar solo la API
        if '/api/' in (args[0] if args else ''):
            print(f'  {args[0]} {args[1]}')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        if self.path == '/api/data':
            with _lock:
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        body = f.read().encode('utf-8')
                else:
                    body = b'{}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(body))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/data':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                with _lock:
                    with open(DATA_FILE, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._cors()
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

def get_local_ip():
    """Obtiene la IP local de la red, compatible con macOS y Linux."""
    try:
        # Truco: conectar a una IP externa (no envía datos) para descubrir IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '(IP desconocida)'

if __name__ == '__main__':
    port = 7890
    os.chdir(os.path.dirname(__file__))
    server = HTTPServer(('0.0.0.0', port), DGHandler)
    ip = get_local_ip()
    print(f'\n✅  DentalGest corriendo en http://{ip}:{port}')
    print(f'   Este equipo → http://localhost:{port}')
    print(f'   Otros equipos en la red → http://{ip}:{port}')
    print(f'   Datos → {DATA_FILE}')
    print(f'\n   Presiona Ctrl+C para detener\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
