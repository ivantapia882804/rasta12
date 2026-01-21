import requests

# Configuración
LOCAL_FILE = 'prr.txt'
REMOTE_URL = 'http://tv.zeuspro.xyz:8080/get.php?username=mauricio6915&password=7f638d67eb53&type=m3u_plus,http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}

# Extensiones de películas/series que queremos ocultar
EXTENSIONES_PROHIBIDAS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv']

def procesar_canales_vivo(texto_m3u):
    """Filtra el contenido eliminando formatos de video (VOD)"""
    lineas = texto_m3u.splitlines()
    resultado = []
    
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url_siguiente = lineas[i+1].strip().lower()
                
                # Comprobamos si la URL contiene alguna de las extensiones prohibidas
                es_pelicula = any(ext in url_siguiente for ext in EXTENSIONES_PROHIBIDAS)
                
                if not es_pelicula and url_siguiente.startswith("http"):
                    resultado.append(linea)
                    resultado.append(lineas[i+1])
    return resultado

def main():
    # Cabecera con EPG
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Procesar prr.txt
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            canales_locales = procesar_canales_vivo(f.read())
            final_lines.extend(canales_locales)
        print(f"✅ Local: {len(canales_locales)//2} canales filtrados.")
    except: pass

    # 2. Procesar ZeusPro
    try:
        r = requests.get(REMOTE_URL, headers=HEADERS, timeout=25)
        if r.status_code == 200:
            canales_remotos = procesar_canales_vivo(r.text)
            final_lines.extend(canales_remotos)
            print(f"✅ Remoto: {len(canales_remotos)//2} canales filtrados (sin .avi, .mkv, .mp4).")
    except: pass

    # 3. Guardar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_lines))
    
    print(f"🚀 Lista '{OUTPUT_FILE}' generada con éxito.")

if __name__ == "__main__":
    main()
