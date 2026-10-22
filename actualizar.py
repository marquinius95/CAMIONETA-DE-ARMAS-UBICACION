import urllib.request
import json
import datetime

# URL de la API comunitaria que rastrea la Gun Van diariamente
URL_API = "https://gta.pjra.dev/api/v1/gunvan"

def obtener_datos():
    try:
        req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            datos = json.loads(response.read().decode())
            
            # Formateamos los datos para nuestro mapa (escala 0 a 2048)
            # Adaptamos las coordenadas automáticamente al lienzo de tu mapa
            lat = datos.get('location', {}).get('y', 1024)
            lng = datos.get('location', {}).get('x', 1024)
            
            # Mapeo aproximado a la escala del mapa si vienen en coordenadas reales de GTA
            if lat < 0 or lat > 2048:
                lat = int(((float(lat) + 4000) / 10000) * 2048)
            if lng < 0 or lng > 2048:
                lng = int(((float(lng) + 5000) / 10000) * 2048)

            resultado = {
                "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                "zone": datos.get('location', {}).get('name', 'Ubicación de hoy'),
                "latitude": lat,
                "longitude": lng,
                "weapons": datos.get('weapons', ["Railgun", "Widowmaker", "Sticky Bomb"])
            }
            return resultado
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None

if __name__ == "__main__":
    datos_nuevos = obtener_datos()
    if datos_nuevos:
        with open("gun_van.json", "w", encoding="utf-8") as f:
            json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        print("¡gun_van.json actualizado exitosamente!")
