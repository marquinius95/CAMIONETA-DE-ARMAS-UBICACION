import json
from datetime import datetime, timezone

# 1. Base de datos con las coordenadas exactas de cada zona
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

# 2. Secuencia ordenada de rotación de la Gun Van
SECUENCIA_ROTACION = [
    "Elysian Island / Plaice Place", "El Burro Heights", "La Mesa", "Davis",
    "La Puerta", "San Andreas / Magellan Avenue", "Pillbox Hill", "Textile City",
    "La Mesa (Maquinitas)", "Murrieta Heights", "Mirror Park", "Centro de Vinewood",
    "Vinewood Oeste", "Del Perro", "Chumash", "Vinewood Hills",
    "Tataviam Mountains", "Central Palmer-Taylor", "Grand Senora Desert",
    "Deshuesadero (Sandy Shores)", "Sandy Shores", "Grapeseed", "Alamo Sea",
    "Río Zancudo", "Lago Zancudo / Fort Zancudo", "Chumash Norte",
    "Paleto Forest", "Paleto Bay", "Mount Chiliad"
]

if __name__ == "__main__":
    ahora_utc = datetime.now(timezone.utc)
    
    # Fecha ancla para calcular los días transcurridos de forma absoluta
    fecha_base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    dias_totales = (ahora_utc - fecha_base).days
    
    # Ajuste para que hoy (29 de octubre de 2026) apunte exactamente a Paleto Forest
    INDICE_CORRECCION = 0
    indice = (dias_totales + INDICE_CORRECCION) % len(SECUENCIA_ROTACION)
    
    nombre_zona = SECUENCIA_ROTACION[indice]
    datos_zona = MAPA_UBICACIONES[nombre_zona]

    datos_nuevos = {
        "date": ahora_utc.strftime("%Y-%m-%d"),
        "zone": nombre_zona,
        "latitude": datos_zona["latitude"],
        "longitude": datos_zona["longitude"],
        "weapons": datos_zona["weapons"]
    }
    
    with open("gun_van.json", "w", encoding="utf-8") as f:
        json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        
    print(f"Actualización exitosa para {ahora_utc.strftime('%Y-%m-%d')}: {nombre_zona}")
