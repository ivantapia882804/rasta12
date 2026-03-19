import requests
import time
from datetime import datetime
import sys

# --- CONFIGURACIÓN ---
LOCAL_FILE = 'prr.txt'
URLS_REMOTAS = [
    'http://tecnotv.club/18ma/lista.m3u',
    'http://tecnotv.club/18ma/lista1.m3u',
    'http://tecnotv.club/18ma/lista2.m3u',
    'http://tecnotv.club/18ma/lista3.m3u',
    'http://tecnotv.club/18ma/lista4.m3u',
    'http://tecnotv.club/18ma/lista5.m3u',
    'http://tecnotv.club/18ma/geomex.m3u',
    'http://tecnotv.club/18ma/android.m3u' 
]

EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.20 LibVLC/3.0.20'}
INTERVALO_HORAS = 6

def procesar_canales(texto_m3u, es_remoto=False):
    if not texto_m3u or not isinstance(texto_m3u, str):
        return []
        
    lineas = texto_m3u.splitlines()
    resultado = []
    
    for i in range(len(lineas)):
        try:
            linea = lineas[i].strip()
            if linea.startswith("#EXTINF"):
                if i + 1 < len(lineas):
                    url = lineas[i+1].strip()
                    if url and url.startswith("http"):
                        # Forzado de .ts para estabilidad en TecnoTV
                        if es_remoto and not any(ext in url.lower() for ext in ['.ts', '.m3u8']):
                            separator = '&' if '?' in url else '?'
                            url = f"{url}{separator}output=ts"
                        
                        resultado.append(linea)
                        resultado.append(url)
        except Exception:
            continue # Si una línea está rota, salta a la siguiente
    return resultado

def ejecutar_actualizacion():
    ahora = datetime.now().strftime('%H:%M:%S')
    print(f"[{ahora}] 🔄 Iniciando ciclo de limpieza...")
    
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']
    
    # 1. Intentar cargar Local
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            canales_locales = procesar_canales(f.read(), es_remoto=False)
            final_lines.extend(canales_locales)
            print(f"✅ Local OK: {len(canales_locales)//2} canales.")
    except Exception as e:
        print(f"⚠️ Aviso: Saltando local ({e})")

    # 2. Procesar Remotas
    for url_fuente in URLS_REMOTAS:
        try:
            r = requests.get(url_fuente, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                # Validamos que sea una lista M3U real antes de procesar
                if "#EXT" in r.text:
                    nuevos = procesar_canales(r.text, es_remoto=True)
                    final_lines.extend(nuevos)
                    print(f"✅ Cargada: {url_fuente[-12:]} | +{len(nuevos)//2}")
            else:
                print(f"❌ Error {r.status_code}: {url_fuente[-12:]}")
        except Exception as e:
            print(f"🚫 Error de red en {url_fuente[-12:]}: {e}")

    # 3. Guardado Seguro
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(final_lines))
        print(f"🚀 Archivo '{OUTPUT_FILE}' actualizado con éxito.")
    except Exception as e:
        print(f"🚨 Error al guardar archivo: {e}")

def main():
    while True:
        try:
            ejecutar_actualizacion()
        except Exception as e:
            print(f"🔥 Error inesperado en el bucle: {e}")
        
        print(f"⏳ Esperando {INTERVALO_HORAS} horas...")
        time.sleep(INTERVALO_HORAS * 3600)

if __name__ == "__main__":
    # Si lo corres en un entorno que no permite bucles infinitos (como GitHub Actions gratis),
    # quita el 'while True' y deja solo ejecutar_actualizacion()
    try:
        ejecutar_actualizacion()
    except:
        sys.exit(1) # Solo sale con error si falla TODO el proceso
        
