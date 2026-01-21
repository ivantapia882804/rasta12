import requests

# --- CONFIGURACIÓN DE FUENTES ---
LOCAL_FILE = 'prr.txt'

# Aquí puedes añadir todas las listas que quieras entre corchetes, separadas por comas
URLS_REMOTAS = [
    'http://tv.zeuspro.xyz:8080/get.php?username=mauricio6915&password=7f638d67eb53&type=m3u_plus','http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus' 
]

EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}

EXTENSIONES_PROHIBIDAS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv']

def procesar_canales(texto_m3u, es_remoto=False):
    lineas = texto_m3u.splitlines()
    resultado = []
    
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url = lineas[i+1].strip()
                url_lower = url.lower()
                
                # Filtro Anti-VOD
                if not any(ext in url_lower for ext in EXTENSIONES_PROHIBIDAS) and url.startswith("http"):
                    
                    # TRUCO PARA ROKU Y REPRODUCTORES ESTRICTOS:
                    # Si es remoto y no termina en .ts o .m3u8, forzamos formato TS
                    if es_remoto and not any(ext in url_lower for ext in ['.ts', '.m3u8']):
                        # Si la URL ya tiene parámetros (tiene un '?'), usamos '&'
                        separator = '&' if '?' in url else '?'
                        url = f"{url}{separator}output=ts"
                    
                    resultado.append(linea)
                    resultado.append(url)
    return resultado

def main():
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Local (prr.txt) - No tocamos nada porque ya usas .m3u8 oficiales
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            final_lines.extend(procesar_canales(f.read(), es_remoto=False))
    except: pass

    # 2. Remoto (ZeusPro) - Forzamos compatibilidad
    for url in URLS_REMOTAS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                final_lines.extend(procesar_canales(r.text, es_remoto=True))
        except: pass

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_lines))
    print("🚀 Lista unificada y optimizada para Roku/Smart TV.")

if __name__ == "__main__":
    main()
