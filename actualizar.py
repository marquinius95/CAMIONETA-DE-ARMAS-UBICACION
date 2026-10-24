import json
from datetime import datetime, timezone

# LISTA MAESTRA DE UBICACIONES CALIBRADAS CON PIXELES REALES (Mapa 4096x4096px)
UBICACIONES_OFICIALES = [
    {
        "zone": "Elysian Island / Plaice Place",
        "latitude": 3636,
        "longitude": 1865,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]
    },
    {
        "zone": "El Burro Heights",
        "latitude": 3460,
        "longitude": 2380,
        "weapons": ["Railgun", "Compact EMP Launcher", "Up-n-Atomizer", "Widowmaker"]
    },
    {
        "zone": "La Mesa",
        "latitude": 3329,
        "longitude": 2193,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Homing Launcher"]
    },
    {
        "zone": "Davis",
        "latitude": 3313,
        "longitude": 1936,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Compact EMP Launcher"]
    },
    {
        "zone": "La Puerta",
        "latitude": 3307,
        "longitude": 1689,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]
    },
    {
        "zone": "San Andreas / Magellan Avenue",
        "latitude": 3144,
        "longitude": 1441,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Stun Gun"]
    },
    {
        "zone": "Pillbox Hill",
        "latitude": 3018,
        "longitude": 1962,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]
    },
    {
        "zone": "Textile City",
        "latitude": 3009,
        "longitude": 2028,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]
    },
    {
        "zone": "La Mesa (Arcade / Maquinitas)",
        "latitude": 3015,
        "longitude": 2115,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]
    },
    {
        "zone": "Murrieta Heights",
        "latitude": 3212,
        "longitude": 2267,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]
    },
    {
        "zone": "Mirror Park",
        "latitude": 2869,
        "longitude": 2240,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]
    },
    {
        "zone": "Centro de Vinewood",
        "latitude": 2739,
        "longitude": 1977,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]
    },
    {
        "zone": "Vinewood Oeste",
        "latitude": 2747,
        "longitude": 1729,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]
    },
    {
        "zone": "Del Perro",
        "latitude": 2906,
        "longitude": 1321,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]
    },
    {
        "zone": "Chumash",
        "latitude": 2403,
        "longitude": 833,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]
    },
    {
        "zone": "Vinewood Hills",
        "latitude": 2369,
        "longitude": 2139,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Compact EMP Launcher"]
    },
    {
        "zone": "Tataviam Mountains",
        "latitude": 2578,
        "longitude": 2507,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]
    },
    {
        "zone": "Central Palmer-Taylor",
        "latitude": 2278,
        "longitude": 2760,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Homing Launcher"]
    },
    {
        "zone": "Grand Senora Desert",
        "latitude": 1852,
        "longitude": 2318,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]
    },
    {
        "zone": "Deshuesadero (Sandy Shores)",
        "latitude": 1763,
        "longitude": 2650,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Up-n-Atomizer"]
    },
    {
        "zone": "Sandy Shores",
        "latitude": 1479,
        "longitude": 2464,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Combat Shotgun"]
    },
    {
        "zone": "Grapeseed",
        "latitude": 1199,
        "longitude": 2446,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Sticky Bomb"]
    },
    {
        "zone": "Alamo Sea",
        "latitude": 1577,
        "longitude": 2169,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]
    },
    {
        "zone": "Río Zancudo",
        "latitude": 1760,
        "longitude": 1878,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Sticky Bomb"]
    },
    {
        "zone": "Lago Zancudo / Fort Zancudo Approach",
        "latitude": 1882,
        "longitude": 1397,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]
    },
    {
        "zone": "Chumash Norte",
        "latitude": 1357,
        "longitude": 1161,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Up-n-Atomizer"]
    },
    {
        "zone": "Paleto Forest",
        "latitude": 980,
        "longitude": 1604,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Stun Gun"]
    },
    {
        "zone": "Paleto Bay",
        "latitude": 642,
        "longitude": 1866,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Combat Shotgun"]
    },
    {
        "zone": "Mount Chiliad",
        "latitude": 606,
        "longitude": 2358,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]
    }
]

if __name__ == "__main__":
    dia_del_anio = datetime.now(timezone.utc).timetuple().tm_yday
    
    # Desfase de +3 para alinear el cálculo con el día real de Mirror Park
    DESFASE = 3
    indice = (dia_del_anio + DESFASE) % len(UBICACIONES_OFICIALES)
    
    ubicacion_hoy = UBICACIONES_OFICIALES[indice]

    datos_nuevos = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "zone": ubicacion_hoy["zone"],
        "latitude": ubicacion_hoy["latitude"],
        "longitude": ubicacion_hoy["longitude"],
        "weapons": ubicacion_hoy["weapons"]
    }
    
    with open("gun_van.json", "w", encoding="utf-8") as f:
        json.dump(datos_nuevos, f, ensure_ascii=False, indent=2)
        
    print(f"¡Sincronización automática exitosa! Ubicación de hoy: {ubicacion_hoy['zone']}")
