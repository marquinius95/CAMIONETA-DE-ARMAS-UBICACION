import urllib.request
import json
import datetime

def obtener_ubicacion_real():
    urls_a_probar = [
        "https://gta.pjra.dev/api/v1/gunvan",
        "https://raw.githubusercontent.com/Scianti/gta-gunvan-tracker/main/data.json"
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

                # CORRECCIÓN DE COORDENADAS: Usamos suma (+) para que el mapa oriente 
                # correctamente el norte hacia arriba y el este hacia la derecha en 4096x4096px
                lat = int(2048 + (raw_y / 4000) * 2048)
                lng = int(2048 + (raw_x / 4000) * 2048)

                # Si los valores ya vienen normalizados en escala 0-4096
                if 0 <= raw_y <= 4096 and 0 <= raw_x <= 4096:
                    lat = int(raw_y)
                    lng = int(raw_x)

                return {
                    "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                    "zone": zone_name,
                    "latitude": max(100, min(3996, lat)),
                    "longitude": max(100, min(3996, lng)),
                    "weapons": data.get('weapons', ["Railgun", "Widowmaker", "Sticky Bomb"])
                }
        except Exception as e:
            print(f"Fallo al consultar {url}: {e}")
            continue
            
    return {
        "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "zone": "Ubicación en tiempo real",
        "latitude": 2048,
        "longitude": 2048,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb"]
    }

if __name__ == "__main__":
    datos_nuevos = obtener_ubicacion_real()
    with open("gun_van.json", "w", encoding="utf-8") as f:
        json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
    print("¡Sincronizado con coordenadas corregidas!")
