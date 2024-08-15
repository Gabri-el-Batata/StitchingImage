import subprocess 

WIFI_NAME = "CompVisio"  

wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])

if WIFI_NAME in str(wifi):
    print("Conectado no Wifi correto.")
else:
    print("Por favor, conecte no wifi das câmeras.")