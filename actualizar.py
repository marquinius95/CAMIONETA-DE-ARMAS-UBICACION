import json
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

# Tu diccionario maestro con coordenadas exactas de píxeles
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

def obtener_zona_con_navegador():
    with sync_playwright() as p:
        # Lanzamos el navegador con argumentos estrictos para evitar detección de bot
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--window-size=1920,1080"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        # Ocultamos la marca de automatización
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        page = context.new_page()
        captured_data = []
        
        def handle_response(response):
            if any(k in response.url for k in ["marker", "json", "data", "gta5"]):
                try:
                    captured_data.append(response.json())
                except:
                    pass

        page.on("response", handle_response)
        
        try:
            print("Conectando a gtaweb.eu con navegador protegido...")
            page.goto("https://gtaweb.eu/gta-map/s/gun-van", timeout=60000, wait_until="domcontentloaded")
            # Damos tiempo a que renderice la interfaz y pase cualquier verificación interna
            page.wait_for_timeout(10000)
            
            # Extraemos todo el texto visible en la página actual
            page_text = page.evaluate("() => document.body.innerText").lower()
            
            # Verificamos si alguna zona de tu lista aparece directamente en el texto de la pantalla
            for zona in MAPA_UBICACIONES.keys():
                palabras = [p for p in zona.lower().split() if len(p) > 3]
                if zona.lower() in page_text or (palabras and any(p in page_text for p in palabras)):
                    print(f"¡Zona detectada visualmente en la web: {zona}!")
                    browser.close()
                    return zona

        except Exception as e:
            print(f"Advertencia durante la ejecución del navegador: {e}")
        
        # Como respaldo secundario, escaneamos la red interceptada
        for data in captured_data:
            markers = []
            if isinstance(data, dict):
                markers = data.get("markers", data.get("data", []))
                if not markers and "features" in data:
                    markers = data["features"]
            elif isinstance(data, list):
                markers = data
                
            for marker in markers:
                if isinstance(marker, dict):
                    texto = str(marker).lower()
                    if "gun-van" in texto or "gun van" in texto or "armas" in texto:
                        for zona in MAPA_UBICACIONES.keys():
                            palabras = [p for p in zona.lower().split() if len(p) > 3]
                            if zona.lower() in texto or (palabras and any(p in texto for p in palabras)):
                                browser.close()
                                return zona
                                
        browser.close()
        return None

if __name__ == "__main__":
    ahora_utc = datetime.now(timezone.utc)
    hoy_str = ahora_utc.strftime("%Y-%m-%d")
    
    zona_elegida = obtener_zona_con_navegador()
    
    if not zona_elegida:
        raise ValueError("Error crítico: El navegador no pudo superar la protección o extraer la ubicación de gtaweb.eu.")

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
        
    print(f"¡Sincronización real exitosa mediante navegador para {hoy_str}: {zona_elegida}!")
