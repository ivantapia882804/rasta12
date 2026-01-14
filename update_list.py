import requests

# Configuración
LOCAL_FILE = 'prr.txt'
REMOTE_URL = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
# EPG sugerido para canales latinos
EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}

def procesar_canales_vivo(texto_m3u):
    """Filtra el contenido para dejar SOLO canales en vivo, eliminando VOD (.mkv, .mp4)"""
    lineas = texto_m3u.splitlines()
    resultado = []
    
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url_siguiente = lineas[i+1].strip().lower()
                
                # REGLA: Si NO contiene .mkv y NO contiene .mp4, es un canal en vivo
                if ".mkv" not in url_siguiente and ".mp4" not in url_siguiente:
                    # Opcional: Asegurarnos de que no sea una línea vacía
                    if url_siguiente.startswith("http"):
                        resultado.append(linea)
                        resultado.append(lineas[i+1])
    return resultado

def main():
    # Cabecera con EPG
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Procesar prr.txt (Canales propios)
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            canales_locales = procesar_canales_vivo(f.read())
            final_lines.extend(canales_locales)
        print(f"✅ Canales en vivo de prr.txt: {len(canales_locales)//2}")
    except Exception as e:
        print(f"⚠️ Error local: {e}")

    # 2. Procesar ZeusPro (Canales remotos)
    try:
        r = requests.get(REMOTE_URL, headers=HEADERS, timeout=25)
        if r.status_code == 200:
            canales_remotos = procesar_canales_vivo(r.text)
            final_lines.extend(canales_remotos)
            print(f"✅ Canales en vivo de ZeusPro: {len(canales_remotos)//2}")
        else:
            print(f"❌ Error servidor: Status {r.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 3. Guardar archivo final
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_lines))
    
    print(f"🚀 Lista '{OUTPUT_FILE}' actualizada solo con TV en vivo.")

if __name__ == "__main__":
    main()
