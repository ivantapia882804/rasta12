import requests

# Fuentes corregidas
local_file = 'prr.txt'
remote_url = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
output_file = 'android.m3u'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def main():
    final_content = "#EXTM3U\n"
    
    # 1. Cargar lo que tienes en prr.txt
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.startswith("#EXTM3U") and line.strip():
                    final_content += line.strip() + "\n"
        print("✅ prr.txt añadido.")
    except Exception as e:
        print(f"⚠️ Nota: No se pudo leer prr.txt ({e})")

    # 2. Cargar lo de ZeusPro con el type correcto
    print("Conectando con ZeusPro...")
    try:
        response = requests.get(remote_url, headers=headers, timeout=20)
        if response.status_code == 200:
            lines = response.text.splitlines()
            count = 0
            for line in lines:
                if not line.startswith("#EXTM3U") and line.strip():
                    final_content += line + "\n"
                    if line.startswith("#EXTINF"): count += 1
            print(f"✅ ZeusPro añadido: {count} canales encontrados.")
        else:
            print(f"❌ Error ZeusPro: Código {response.status_code}")
    except Exception as e:
        print(f"❌ Fallo de conexión: {e}")

    # 3. Guardar el archivo final
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"✨ ¡Lista {output_file} creada exitosamente!")

if __name__ == "__main__":
    main()
