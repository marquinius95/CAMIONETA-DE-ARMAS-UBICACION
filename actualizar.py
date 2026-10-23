import json
from datetime import datetime, timezone

# LISTA COMPLETA DE UBICACIONES OFICIALES DE LA GUN VAN CALIBRADAS PARA EL MAPA 4096x4096px
# (Eje Leaflet: lat 0=Norte/Arriba, lat 4096=Sur/Abajo)
UBICACIONES_OFICIALES = [
    {
        "zone": "Deshuesadero (Sandy Shores)",
        "latitude": 1150,
        "longitude": 2550,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Combat Shotgun"]
    },
    {
        "zone": "Grand Senora Desert",
        "latitude": 1450,
        "longitude": 2650,
        "weapons": ["Railgun", "Compact EMP Launcher", "Up-n-Atomizer", "Widowmaker"]
    },
    {
        "zone": "Ron Alternates Wind Farm",
        "latitude": 1800,
        "longitude": 3100,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Homing Launcher"]
    },
    {
        "zone": "Paleto Bay",
        "latitude": 450,
        "longitude": 1350,
        "weapons": ["Railgun", "Widowmaker", "Stun Gun", "Compact EMP Launcher"]
    },
    {
        "zone": "Grapeseed",
        "latitude": 900,
        "longitude": 2600,
        "weapons": ["Railgun", "Widowmaker", "Sticky Bomb", "Widowmaker"]
    },
    {
        "zone": "Pacific Bluffs",
        "latitude": 2750,
        "longitude": 1050,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Sticky Bomb"]
    },
    {
        "zone": "Tataviam Mountains",
        "latitude": 2200,
        "longitude": 3300,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Stun Gun"]
    },
    {
        "zone": "Vinewood Hills",
        "latitude": 2350,
        "longitude": 2050,
        "weapons": ["Railgun", "Widowmaker", "Homing Launcher", "Sticky Bomb"]
    },
    {
        "zone": "Downtown Los Santos",
        "latitude": 3100,
        "longitude": 2150,
        "weapons": ["Railgun", "Widowmaker", "Up-n-Atomizer", "Stun Gun"]
    },
    {
        "zone": "Los Santos International Airport (LSIA)",
        "latitude": 3650,
        "longitude": 1850,
        "weapons": ["Railgun", "Widowmaker", "Compact EMP Launcher", "Sticky Bomb"]
    }
]

if __name__ == "__main__":
    # Selecciona la ubicación automáticamente basándose en el día del año actual
    # Esto garantiza que cambie de forma autónoma y cíclica todos los días sin intervención manual.
    dia_del_anio = datetime.now(timezone.utc).timetuple().tm_yday
    indice = dia_del_anio % len(UBICACIONES_OFICIALES)
    
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
