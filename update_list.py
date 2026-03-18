import requests
import time
from datetime import datetime

# --- CONFIGURACIÓN ---
LOCAL_FILE = 'prr.txt'
URLS_REMOTAS = [
    'http://tecnotv.club/ma1003/lista.m3u',
    'http://tecnotv.club/ma1003/lista1.m3u',
    'http://tecnotv.club/ma1003/lista2.m3u',
    'http://tecnotv.club/ma1003/lista3.m3u',
    'http://tecnotv.club/ma1003/lista4.m3u',
    'http://tecnotv.club/ma1003/lista5.m3u',
    'http://tecnotv.club/ma1003/geomex.m3u',
    'http://tecnotv.club/ma1003/android.m3u' 
]

EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.20 LibVLC/3.0.20'}
INTERVALO_HORAS = 6

def procesar_canales(texto_m3u, es_remoto=False):
    lineas = texto_m3u.splitlines()
    resultado = []
    
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url = lineas[i+1].strip()
                if url:
                    # Forzado de formato .ts para estabilidad en remotas
                    if es_remoto and not any(ext in url.lower() for ext in ['.ts', '.m3u8']):
                        separator = '&' if '?' in url else '?'
                        url = f"{url}{separator}output=ts"
                    
                    resultado.append(linea)
                    resultado.append(url)
    return resultado

def ejecutar_actualizacion():
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{ahora}] 🔄 Iniciando actualización de listas...")
    
    # Cabecera con EPG
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Procesar Local (Siempre prioritario)
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            final_lines.extend(procesar_canales(f.read(), es_remoto=False))
            print(f"✅ Archivo local '{LOCAL_FILE}' cargado.")
    except Exception as e:
        print(f"⚠️ No se pudo cargar el archivo local: {e}")

    # 2. Procesar Remotas (Sin limitaciones)
    canales_totales = 0
    for url_fuente in URLS_REMOTAS:
        try:
            # Timeout largo para evitar cortes por saturación del servidor
            r = requests.get(url_fuente, headers=HEADERS, timeout=45)
            if r.status_code == 200:
                canales_nuevos = procesar_canales(r.text, es_remoto=True)
                final_lines.extend(canales_nuevos)
                conteo = len(canales_nuevos) // 2
                canales_totales += conteo
                print(f"✅ {url_fuente} -> {conteo} canales.")
            else:
                print(f"❌ Error {r.status_code} en: {url_fuente}")
        except Exception as e:
            print(f"⚠️ Error de conexión en {url_fuente}: {e}")

    # Guardar resultado
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(final_lines))
        print(f"🚀 Lista unificada guardada en '{OUTPUT_FILE}'. Total: {canales_totales} canales remotos.")
    except Exception as e:
        print(f"🚨 Error crítico al escribir el archivo: {e}")

def main():
    print(f"--- SCRIPT DE AUTO-ACTUALIZACIÓN IPTV (Cada {INTERVALO_HORAS}h) ---")
    while True:
        ejecutar_actualizacion()
        
        proxima_hora = INTERVALO_HORAS * 3600
        print(f"⏳ Esperando {INTERVALO_HORAS} horas para la siguiente actualización...")
        time.sleep(proxima_hora)

if __name__ == "__main__":
    main()
                    
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
