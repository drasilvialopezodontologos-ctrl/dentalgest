#!/usr/bin/env python3
"""
DentalGest — Migración de datos a Supabase
Toma el data.json local y lo sube a la tabla 'data' de Supabase.

Uso:
  python3 migrar_a_supabase.py
"""
import json, os, urllib.request, urllib.parse

# ═══════════════════════════════════════════════════════
#  COMPLETAR con los valores de tu proyecto en supabase.com
# ═══════════════════════════════════════════════════════
SUPABASE_URL = 'https://xrbppoeglcadzxolrfsc.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhyYnBwb2VnbGNhZHp4b2xyZnNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA0Mjg1NjksImV4cCI6MjA5NjAwNDU2OX0.NWN510mAkelRtAlq43MgG8M5rA9Ls1U2LElTmwePMao'
# ═══════════════════════════════════════════════════════

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def supabase_upsert(rows):
    url = f"{SUPABASE_URL}/rest/v1/data"
    body = json.dumps(rows).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        method='POST',
        headers={
            'apikey':          SUPABASE_KEY,
            'Authorization':   f'Bearer {SUPABASE_KEY}',
            'Content-Type':    'application/json',
            'Prefer':          'resolution=merge-duplicates',
        }
    )
    with urllib.request.urlopen(req) as r:
        return r.status

print('\n╔══════════════════════════════════════╗')
print('║  DentalGest — Migración a Supabase   ║')
print('╚══════════════════════════════════════╝\n')

if not os.path.exists(DATA_FILE):
    print('❌  No se encontró data.json')
    print('    Asegúrate de que el servidor Mac haya corrido al menos una vez.')
    exit(1)

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

if not data:
    print('⚠️  data.json está vacío — nada que migrar.')
    exit(0)

print(f'→ Encontradas {len(data)} claves en data.json:')
for k in data.keys():
    count = len(data[k]) if isinstance(data[k], list) else '(objeto)'
    print(f'   {k}: {count} registros')

print('\n→ Subiendo a Supabase...')

rows = [{'key': k, 'value': v} for k, v in data.items()]

# Supabase tiene límite de ~1000 rows por request — dividir si es necesario
BATCH = 100
for i in range(0, len(rows), BATCH):
    batch = rows[i:i+BATCH]
    status = supabase_upsert(batch)
    print(f'   Batch {i//BATCH + 1}: {status}')

print('\n✅  Migración completada')
print('   DentalGest ya puede funcionar desde GitHub Pages + Supabase\n')
