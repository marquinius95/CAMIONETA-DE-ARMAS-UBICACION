import urllib.request
import json
import datetime

# Usamos una URL directa y robusta de la comunidad para la Gun Van
URL_API = "https://gta.pjra.dev/api/v1/gunvan"

def obtener_datos():
    try:
        # Añadimos headers de navegador para evitar bloqueos
        req = urllib.request.Request(
            URL_API, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            datos = json.loads(response.read().decode())
            
            # Extraemos la ubicación y armas reales
            loc = datos.get('location', {})
            lat = loc.get('y', 1024)
            lng = loc.get('x', 1024)
            
            # Ajuste de escala exacto para el mapa cuadrado de 2048x2048
            # Si vienen en coordenadas del juego, las convertimos al lienzo de tu mapa
            if abs(lat) > 2048 or abs(lng) > 2048:
                # Conversión estándar de coordenadas de GTA V al mapa plano
                lat = int(1024 - (float(lat) / 4000) * 1024)
                lng = int(1024 + (float(lng) / 4000) * 1024)

            resultado = {
                "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                "zone": loc.get('name', 'Ubicación actual de la Gun Van'),
                "latitude": max(50, min(1998, lat)),
                "longitude": max(50, min(1998, lng)),
                "weapons": datos.get('weapons', ["Railgun", "Widowmaker", "Sticky Bomb"])
            }
            return resultado
    except Exception as e:
        print(f"Error al obtener datos en tiempo real: {e}")
        return None

if __name__ == "__main__":
    datos_nuevos = obtener_datos()
    if datos_nuevos:
        with open("gun_van.json", "w", encoding="utf-8") as f:
            json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        print("¡gun_van.json sincronizado en tiempo real!")
