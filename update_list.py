import requests
import re

# Fuentes
local_file = 'prr.txt'
remote_url = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=mp3_plus'
output_file = 'android.m3u'

def organizar_canal(linea_info):
    """
    Mejora la línea #EXTINF asignando grupos basados en palabras clave.
    """
    # Ejemplo de personalización por palabras clave
    if "HBO" in linea_info.upper() or "CINEMAX" in linea_info.upper():
        linea_info = linea_info.replace('group-title=""', 'group-title="CINE PREMIUM"')
    elif "FOX" in linea_info.upper() or "STAR" in linea_info.upper():
        linea_info = linea_info.replace('group-title=""', 'group-title="SERIES"')
    elif "DEPORTES" in linea_info.upper() or "ESPN" in linea_info.upper():
        linea_info = linea_info.replace('group-title=""', 'group-title="DEPORTES"')
    
    # Si la línea no tiene grupo, asignamos uno general
    if 'group-title=""' in linea_info or 'group-title' not in linea_info:
        linea_info = linea_info.replace('group-title="', 'group-title="VARIEDADOS') # Opcional
        
    return linea_info

def main():
    final_content = "#EXTM3U\n"
    
    # --- PROCESAR LISTA LOCAL (prr.txt) ---
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#EXTINF"):
                    final_content += organizar_canal(line.strip()) + "\n"
                elif not line.startswith("#EXTM3U") and line.strip():
                    final_content += line.strip() + "\n"
    except FileNotFoundError:
        print("Archivo local no encontrado.")

    # --- PROCESAR LISTA REMOTA (ZeusPro) ---
    try:
        r = requests.get(remote_url, timeout=10)
        if r.status_code == 200:
            lines = r.text.splitlines()
            for i in range(len(lines)):
                line = lines[i].strip()
                if line.startswith("#EXTINF"):
                    # Añadimos la info del canal procesada
                    final_content += organizar_canal(line) + "\n"
                elif line.startswith("http"):
                    # Añadimos la URL del streaming
                    final_content += line + "\n"
    except Exception as e:
        print(f"Error con ZeusPro: {e}")

    # --- GUARDAR RESULTADO ---
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("¡Lista android.m3u actualizada con éxito!")

if __name__ == "__main__":
    main()
