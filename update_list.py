import requests

# Configuración
LOCAL_FILE = 'prr.txt'
REMOTE_URL = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
# Aquí puedes poner varias URLs de EPG separadas por comas
EPG_URL = 'https://raw.githubusercontent.com/acidjesuz/EPGTalk/master/guide.xml' 
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}

def procesar_lista(texto_m3u):
    lineas = texto_m3u.splitlines()
    resultado = []
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url_siguiente = lineas[i+1].strip().lower()
                # Mantenemos el filtro de películas .mkv
                if ".mkv" in url_siguiente:
                    resultado.append(linea)
                    resultado.append(lineas[i+1])
    return resultado

def main():
    # Insertamos la fuente EPG en la cabecera
    final_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"\n']
    
    # --- PROCESAR LOCAL ---
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            final_lines.extend(procesar_lista(f.read()))
    except: pass

    # --- PROCESAR REMOTO ---
    try:
        r = requests.get(REMOTE_URL, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            final_lines.extend(procesar_lista(r.text))
    except: pass

    # --- GUARDAR ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_lines))
    print("🚀 Lista con EPG generada.")

if __name__ == "__main__":
    main()
