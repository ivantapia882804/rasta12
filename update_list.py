import requests
import sys

# Configuración
LOCAL_FILE = 'prr.txt'
REMOTE_URL = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
OUTPUT_FILE = 'android.m3u'
HEADERS = {'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12'}

def main():
    final_lines = ["#EXTM3U\n"]
    
    # --- PARTE 1: LEER LOCAL ---
    try:
        with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if "#EXTM3U" not in line and line.strip():
                    final_lines.append(line.strip() + "\n")
        print("✅ Local prr.txt leído.")
    except Exception as e:
        print(f"⚠️ No se pudo leer local: {e}")

    # --- PARTE 2: LEER REMOTO ---
    print("Intentando conectar a ZeusPro...")
    try:
        # Timeout corto para que GitHub no se quede esperando infinitamente
        r = requests.get(REMOTE_URL, headers=HEADERS, timeout=15)
        if r.status_code == 200 and "#EXTINF" in r.text:
            lines = r.text.splitlines()
            for line in lines:
                if "#EXTM3U" not in line and line.strip():
                    final_lines.append(line.strip() + "\n")
            print(f"✅ ZeusPro integrado correctamente.")
        else:
            print(f"❌ ZeusPro respondió error {r.status_code} o lista vacía.")
    except Exception as e:
        print(f"❌ Fallo crítico al conectar a ZeusPro: {e}")

    # --- PARTE 3: ESCRITURA FINAL ---
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        print(f"🚀 Archivo {OUTPUT_FILE} guardado.")
    except Exception as e:
        print(f"🔥 Error al escribir archivo: {e}")
        sys.exit(1) # Solo aquí damos error real si no puede ni escribir

if __name__ == "__main__":
    main()
