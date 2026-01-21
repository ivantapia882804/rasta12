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

# Extensiones de películas/VOD que queremos ocultar
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
                # Solo guardamos si no es película y es una URL válida
                es_pelicula = any(ext in url_siguiente for ext in EXTENSIONES_PROHIBIDAS)
                if not es_pelicula and url_siguiente.startswith("http"):
                    resultado.append(linea)
                    resultado.append(lineas[i+1])
    return resultado

def main():
    # Cabecera con EPG
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Procesar prr.txt (Local)
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            final_lines.extend(procesar_canales_vivo(f.read()))
        print("✅ Local: prr.txt procesado.")
    except:
        print("⚠️ No se encontró prr.txt")

    # 2. Procesar Listas Remotas (Servidores)
    for url in URLS_REMOTAS:
        if not url.startswith("http"): continue # Salta si la URL está vacía
        
        print(f"Conectando a servidor: {url[:30]}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                canales = procesar_canales_vivo(r.text)
                final_lines.extend(canales)
                print(f"✅ Servidor procesado: {len(canales)//2} canales añadidos.")
            else:
                print(f"❌ Error en servidor: Status {r.status_code}")
        except Exception as e:
            print(f"❌ Fallo de conexión: {e}")

    # 3. Guardar archivo final unificado
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_lines))
    
    print(f"\n🚀 Lista '{OUTPUT_FILE}' unificada y filtrada con éxito.")

if __name__ == "__main__":
    main()
