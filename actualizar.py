import json
from datetime import datetime, timezone

# Lista completa de todas las ubicaciones posibles en orden de rotación oficial
CICLO_GUN_VAN = [
    "Terminal",
    "Elysian Island / Plaice Place",
    "El Burro Heights",
    "La Mesa",
    "Davis",
    "La Puerta",
    "San Andreas / Magellan Avenue",
    "Pillbox Hill",
    "Textile City",
    "La Mesa (Maquinitas)",
    "Murrieta Heights",
    "Mirror Park",
    "Centro de Vinewood",
    "Vinewood Oeste",
    "Del Perro",
    "Chumash",
    "Vinewood Hills",
    "Tataviam Mountains",
    "Central Palmer-Taylor",
    "Grand Senora Desert",
    "Sandy Shores",
    "Grapeseed",
    "Alamo Sea",
    "Río Zancudo",
    "Lago Zancudo / Fort Zancudo",
    "Chumash Norte",
    "Paleto Norte",
    "Paleto Bay",
    "Mount Chiliad"
]

# Diccionario maestro con tus coordenadas exactas de píxeles (¡las que mediste con precisión!)
MAPA_UBICACIONES = {
    "Terminal": {"latitude": 3837, "longitude": 2126, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "Elysian Island / Plaice Place": {"latitude": 3636, "longitude": 1851, "weapons": ["Railgun", "Compact EMP Launcher", "Up-n-Atomizer", "Widowmaker"]},
    "El Burro Heights": {"latitude": 3461, "longitude": 2377, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Homing Launcher"]},
    "La Mesa": {"latitude": 3330, "longitude": 2196, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Compact EMP Launcher"]},
    "Davis": {"latitude": 3310, "longitude": 1930, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]},
    "La Puerta": {"latitude": 3303, "longitude": 1683, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Stun Gun"]},
    "San Andreas / Magellan Avenue": {"latitude": 3143, "longitude": 1442, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Pillbox Hill": {"latitude": 3010, "longitude": 1964, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]},
    "Textile City": {"latitude": 3003, "longitude": 2029, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "La Mesa (Maquinitas)": {"latitude": 3005, "longitude": 2119, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]},
    "Murrieta Heights": {"latitude": 3211, "longitude": 2257, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]},
    "Mirror Park": {"latitude": 2868, "longitude": 2251, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]},
    "Centro de Vinewood": {"latitude": 2738, "longitude": 1971, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Vinewood Oeste": {"latitude": 2747, "longitude": 1722, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]},
    "Del Perro": {"latitude": 2912, "longitude": 1320, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]},
    "Chumash": {"latitude": 2400, "longitude": 832, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]},
    "Vinewood Hills": {"latitude": 2363, "longitude": 2140, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]},
    "Tataviam Mountains": {"latitude": 2574, "longitude": 2507, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]},
    "Central Palmer-Taylor": {"latitude": 2280, "longitude": 2757, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]},
    "Grand Senora Desert": {"latitude": 1857, "longitude": 2315, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]},
    "Sandy Shores": {"latitude": 1479, "longitude": 2469, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Sticky Bomb"]},
    "Grapeseed": {"latitude": 1167, "longitude": 2440, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]},
    "Alamo Sea": {"latitude": 1575, "longitude": 2173, "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Sticky Bomb"]},
    "Río Zancudo": {"latitude": 1753, "longitude": 1890, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]},
    "Lago Zancudo / Fort Zancudo": {"latitude": 1884, "longitude": 1396, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]},
    "Chumash Norte": {"latitude": 1352, "longitude": 1163, "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Stun Gun"]},
    "Paleto Norte": {"latitude": 978, "longitude": 1620, "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]},
    "Paleto Bay": {"latitude": 642, "longitude": 1868, "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]},
    "Mount Chiliad": {"latitude": 607, "longitude": 2362, "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]}
}

if __name__ == "__main__":
    ahora_utc = datetime.now(timezone.utc)
    hoy_str = ahora_utc.strftime("%Y-%m-%d")
    
    # Cálculo exacto basado en el día del año UTC para seguir la rotación oficial de Rockstar
    dia_del_anio = ahora_utc.timetuple().tm_yday
    indice_zona = dia_del_anio % len(CICLO_GUN_VAN)
    zona_elegida = CICLO_GUN_VAN[indice_zona]

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
        
    print(f"Bot sincronizado por ciclo oficial para {hoy_str}: {zona_elegida}")
