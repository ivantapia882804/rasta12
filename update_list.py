import requests

local_file = 'prr.txt'
remote_url = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=m3u_plus'
output_file = 'android.m3u'

# Usamos el User-Agent de VLC, que es el más aceptado por servidores IPTV
headers = {
    'User-Agent': 'VLC/3.0.12 LibVLC/3.0.12',
    'Accept': '*/*'
}

def main():
    final_content = "#EXTM3U\n"
    
    # 1. Leer prr.txt
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.startswith("#EXTM3U") and line.strip():
                    final_content += line.strip() + "\n"
        print("✅ Local: prr.txt cargado.")
    except Exception as e:
        print(f"❌ Error Local: {e}")

    # 2. Intentar descargar ZeusPro
    print(f"DEBUG: Conectando a ZeusPro...")
    try:
        # Añadimos verify=False por si hay problemas de certificados SSL
        response = requests.get(remote_url, headers=headers, timeout=30, verify=False)
        
        print(f"DEBUG: Status Code: {response.status_code}")
        
        if response.status_code == 200:
            raw_text = response.text
            if "#EXTINF" in raw_text:
                lines = raw_text.splitlines()
                count = 0
                for line in lines:
                    if not line.startswith("#EXTM3U") and line.strip():
                        final_content += line + "\n"
                        if line.startswith("#EXTINF"): count += 1
                print(f"✅ Remoto: {count} canales agregados.")
            else:
                print("❌ Error: El servidor respondió pero la lista está vacía o el formato es incorrecto.")
                # Imprimimos los primeros 100 caracteres para ver qué respondió
                print(f"Respuesta del servidor: {raw_text[:100]}")
        else:
            print(f"❌ Error: El servidor ZeusPro rechazó la conexión (Código {response.status_code}).")

    except Exception as e:
        print(f"❌ Error de red: {e}")

    # 3. Guardar
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

if __name__ == "__main__":
    main()
