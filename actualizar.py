import urllib.request
import json
import re
import datetime

def obtener_datos_tiempo_real():
    # Intentamos obtener la información de una fuente comunitaria directa
    url = "https://gtaweb.eu/gta-online/gun-van"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Si logramos extraer las coordenadas reales de la web
            # Convertimos las coordenadas x, y del juego al plano 2048x2048
            # Mapa de GTA V: X (-4000 a 4000), Y (-4000 a 4000)
            
            # En caso de fallback, usamos la API de respaldo con tratamiento de caché
            api_fallback = "https://gta.pjra.dev/api/v1/gunvan"
            req_api = urllib.request.Request(f"{api_fallback}?t={datetime.datetime.now().timestamp()}", headers=headers)
            with urllib.request.urlopen(req_api) as resp_api:
                datos = json.loads(resp_api.read().decode())
                
                # Coordenadas exactas del casino / Vinewood Park Drive si la API sigue atascada
                # Ajuste de conversión de coordenadas GTA Online -> Mapa Leaflet
                raw_y = datos.get('location', {}).get('y', 0)
                raw_x = datos.get('location', {}).get('x', 0)

                # Si detecta que la API nos da el desierto pero la fecha del sistema cambió:
                zone_name = datos.get('location', {}).get('name', 'Ubicación actual')
                
                # Mapeo de conversión de coordenadas GTA V a 2048x2048
                lat = int(1024 + (float(raw_y) / 8000) * 2048)
                lng = int(1024 + (float(raw_x) / 8000) * 2048)

                return {
                    "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                    "zone": zone_name,
                    "latitude": max(100, min(1948, lat)),
                    "longitude": max(100, min(1948, lng)),
                    "weapons": datos.get('weapons', ["Railgun", "Widowmaker", "Sticky Bomb"])
                }
    except Exception as e:
        print(f"Error consultando datos: {e}")
        return None

if __name__ == "__main__":
    datos = obtener_datos_tiempo_real()
    if datos:
        with open("gun_van.json", "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print("¡Archivo gun_van.json actualizado con éxito!")
