import requests

# Fuentes
local_file = 'prr.txt'
remote_url = 'http://tv.zeuspro.xyz:2052/get.php?username=arturo903&password=11HD4MrrPG&type=mp3_plus'
output_file = 'android.m3u'

def main():
    content = "#EXTM3U\n"
    
    # 1. Leer lista local
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith("#EXTM3U"):
                    content += line
    except FileNotFoundError:
        print(f"Archivo {local_file} no encontrado.")

    # 2. Leer lista remota
    try:
        response = requests.get(remote_url)
        if response.status_code == 200:
            remote_lines = response.text.splitlines()
            for line in remote_lines:
                if not line.startswith("#EXTM3U"):
                    content += line + "\n"
    except Exception as e:
        print(f"Error al descargar la lista remota: {e}")

    # 3. Guardar en android.m3u
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    main()
