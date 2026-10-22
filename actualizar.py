import urllib.request
import json
from datetime import datetime, timezone

def obtener_ubicacion_real():
    # Nuevas fuentes activas de la comunidad para la Gun Van
    urls_a_probar = [
        "https://raw.githubusercontent.com/gta-tools/gunvan/main/gunvan.json",
        "https://gta-api.site/api/v1/gunvan", # Endpoint alternativo de la comunidad
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Cache-Control': 'no-cache'
    }

    for url in urls_a_probar:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                # Adaptamos según la estructura que devuelva la API activa
                if 'location' in data:
                    loc = data['location']
                    zone_name = loc.get('name', 'Ubicación actual')
                    raw_y = float(loc.get('y', 0))
                    raw_x = float(loc.get('x', 0))
                elif 'zone' in data:
                    zone_name = data.get('zone', 'Ubicación actual')
                    raw_y = float(data.get('latitude', 2048))
                    raw_x = float(data.get('longitude', 2048))
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
            
    # Si todo falla, imprimimos aviso pero mantenemos estructura
    print("Aviso: No se pudo conectar a las APIs externas. Se mantiene la última ubicación.")
    return None

if __name__ == "__main__":
    datos_nuevos = obtener_ubicacion_real()
    if datos_nuevos:
        with open("gun_van.json", "w", encoding="utf-8") as f:
            json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        print("¡Archivo gun_van.json actualizado con éxito!")
    else:
        print("No se realizaron cambios por falta de conexión con las fuentes.")
