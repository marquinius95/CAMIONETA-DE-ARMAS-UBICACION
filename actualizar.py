import json
import math
from datetime import datetime, timezone
import requests

# Tus posibles ubicaciones con sus coordenadas en tu mapa de 4096px
# (El bot evaluará cuál es la más cercana a la detectada en la web)
MAPA_UBICACIONES = {
    "Elysian Island / Plaice Place": {"latitude": 3636, "longitude": 1865, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "El Burro Heights": {"latitude": 3460, "longitude": 2380, "weapons": ["Railgun", "Compact EMP Launcher", "Up-n-Atomizer", "Widowmaker"]},
    "La Mesa": {"latitude": 3329, "longitude": 2193, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Homing Launcher"]},
    "Davis": {"latitude": 3313, "longitude": 1936, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Compact EMP Launcher"]},
    "La Puerta": {"latitude": 3307, "longitude": 1689, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]},
    "San Andreas / Magellan Avenue": {"latitude": 3144, "longitude": 1441, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Stun Gun"]},
    "Pillbox Hill": {"latitude": 3018, "longitude": 1962, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Textile City": {"latitude": 3009, "longitude": 2028, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]},
    "La Mesa (Maquinitas)": {"latitude": 3015, "longitude": 2115, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "Murrieta Heights": {"latitude": 3212, "longitude": 2267, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]},
    "Mirror Park": {"latitude": 2869, "longitude": 2240, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]},
    "Centro de Vinewood": {"latitude": 2739, "longitude": 1977, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]},
    "Vinewood Oeste": {"latitude": 2747, "longitude": 1729, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Del Perro": {"latitude": 2906, "longitude": 1321, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]},
    "Chumash": {"latitude": 2403, "longitude": 833, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "Vinewood Hills": {"latitude": 2369, "longitude": 2139, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]},
    "Tataviam Mountains": {"latitude": 2578, "longitude": 2507, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]},
    "Central Palmer-Taylor": {"latitude": 2278, "longitude": 2760, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]},
    "Grand Senora Desert": {"latitude": 1852, "longitude": 2318, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Deshuesadero (Sandy Shores)": {"latitude": 1763, "longitude": 2650, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]},
    "Sandy Shores": {"latitude": 1479, "longitude": 2464, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Combat Shotgun"]},
    "Grapeseed": {"latitude": 1199, "longitude": 2446, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Sticky Bomb"]},
    "Alamo Sea": {"latitude": 1577, "longitude": 2169, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]},
    "Río Zancudo": {"latitude": 1760, "longitude": 1878, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Sticky Bomb"]},
    "Lago Zancudo / Fort Zancudo": {"latitude": 1882, "longitude": 1397, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]},
    "Chumash Norte": {"latitude": 1357, "longitude": 1161, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]},
    "Paleto Forest": {"latitude": 980, "longitude": 1604, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Stun Gun"]},
    "Paleto Bay": {"latitude": 642, "longitude": 1866, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]},
    "Mount Chiliad": {"latitude": 606, "longitude": 2358, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]}
}

def obtener_punto_gtaweb():
    try:
        # Petición a los datos públicos de marcadores que consume gtaweb
        url = "https://gtaweb.eu/data/gta5/markers.json"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Buscamos la Gun Van dentro del JSON de la web
            for marker in data.get("markers", []):
                if "gun-van" in marker.get("id", "").lower():
                    # gtaweb devuelve coordenadas de mapa o lat/lng internas
                    coords = marker.get("coords")
                    if coords:
                        return coords
    except Exception as e:
        print(f"Error consultando gtaweb: {e}")
    return None

if __name__ == "__main__":
    ahora_utc = datetime.now(timezone.utc)
    hoy_str = ahora_utc.strftime("%Y-%m-%d")
    
    # 1. Intentar obtener el punto actual de la web
    punto_web = obtener_punto_gtaweb()
    
    zona_elegida = "Del Perro" # Valor por defecto de respaldo
    
    if punto_web:
        # gtaweb provee coordenadas (lat, lng o x, y). Vamos a buscar la menor distancia euclidiana
        # contra tus puntos almacenados para encontrar el match perfecto.
        # (Si el formato de gtaweb usa otras keys, ajustamos la lectura de x e y aquí)
        web_x = punto_web.get("x", punto_web.get("lng", 0))
        web_y = punto_web.get("y", punto_web.get("lat", 0))
        
        menor_distancia = float("inf")
        for zona, info in MAPA_UBICACIONES.items():
            # Distancia matemática simple para ver cuál de tus puntos está más cerca del punto detectado
            distancia = math.sqrt((info["longitude"] - web_x)**2 + (info["latitude"] - web_y)**2)
            if distancia < menor_distancia:
                menor_distancia = distancia
                zona_elegida = zona

    datos_zona = MAPA_UBICACIONES[zona_elegida]

    datos_nuevos = {
        "date": hoy_str,
        "zone": zona_elegida,
        "latitude": datos_zona["latitude"],
        "longitude": datos_zona["longitude"],
        "weapons": datos_zona["weapons"]
    }
    
    with open("gun_van.json", "w", encoding="utf-8") as f:
        json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        
    print(f"Bot automático sincronizado con éxito para {hoy_str}: {zona_elegida}")
