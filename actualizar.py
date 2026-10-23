import urllib.request
import json
from datetime import datetime, timezone

def obtener_ubicacion_real():
    # Lista ampliada de espejos y fuentes comunitarias activas
    urls_a_probar = [
        "https://raw.githubusercontent.com/Scianti/gta-gunvan-tracker/main/data.json",
        "https://raw.githubusercontent.com/gta-tools/gunvan/main/data.json",
        "https://gtaweb.eu/data/gta5/gun-van.json"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json'
    }

    for url in urls_a_probar:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                # Extracción flexible según el formato de la fuente que responda
                if 'location' in data:
                    loc = data['location']
                    zone_name = loc.get('name', loc.get('zone', 'Ubicación actual'))
                    raw_y = float(loc.get('y', loc.get('latitude', 2048)))
                    raw_x = float(loc.get('x', loc.get('longitude', 2048)))
                elif 'zone' in data:
                    zone_name = data.get('zone', 'Ubicación actual')
                    raw_y = float(data.get('latitude', 2048))
                    raw_x = float(data.get('longitude', 2048))
                elif isinstance(data, list) and len(data) > 0:
                    item = data[0]
                    zone_name = item.get('zone', item.get('name', 'Ubicación actual'))
                    raw_y = float(item.get('y', item.get('latitude', 2048)))
                    raw_x = float(item.get('x', item.get('longitude', 2048)))
                else:
                    continue

                # Conversión matemática para el mapa de 4096x4096px
                if abs(raw_y) <= 4000 and abs(raw_x) <= 4000:
                    lat = int(1600 + (raw_y / 3800.0) * 1600.0)
                    lng = int(2048 + (raw_x / 3800.0) * 2048.0)
                else:
                    lat = int(raw_y)
                    lng = int(raw_x)

                return {
                    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "zone": zone_name,
                    "latitude": max(100, min(3996, lat)),
                    "longitude": max(100, min(3996, lng)),
                    "weapons": data.get('weapons', ["Railgun", "Widowmaker", "Sticky Bomb"])
                }
        except Exception as e:
            print(f"Fallo al consultar {url}: {e}")
            continue
            
    # Si ninguna API responde, devolvemos una estructura base segura para evitar bloqueos
    print("Aviso: Fuentes externas no disponibles. Usando coordenadas por defecto.")
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "zone": "Ubicación en actualización",
        "latitude": 2048,
        "longitude": 2048,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb"]
    }

if __name__ == "__main__":
    datos_nuevos = obtener_ubicacion_real()
    with open("gun_van.json", "w", encoding="utf-8") as f:
        json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
    print("¡Archivo gun_van.json sincronizado correctamente!")
