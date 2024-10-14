import cv2 as cv
import os
import numpy as np
from CAMERA_IPS import (CAMERA01, CAMERA02)
import time
from utils import check_wifi
from pythonping import ping
import matplotlib.pyplot as plt

WIFI_NAME = "CompVisio"

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000" # 5 seconds

def ping_camera(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        print(f"{ip} is reachable.")
        return True
    else:
        print(f"{ip} is not reachable.")
        return False

def clear_buffer_two(cap1, cap2, frames_to_clear) -> None:
    # Limpa os frames do buffer chamando grab() múltiplas vezes
    for _ in range(frames_to_clear):
        cap1.grab()
        cap2.grab()

def clear_buffer_one(cap, frames_to_clear) -> None:
    # Limpa os frames do buffer chamando grab() múltiplas vezes
    for _ in range(frames_to_clear):
        cap.grab()

def draw_horizontal_line(img):
    #h, w = img.shape[:2]
    h = 1080
    w = 1920
    center_y = h // 2
    color = (0, 0, 255)  # Verde
    thickness = 2
   
    img_with_line = img.copy()
    cv.line(img_with_line, (0, center_y), (w, center_y), color, thickness)
    cv.line(img_with_line, (0, center_y + 110), (w, center_y + 110), (0, 255, 0), thickness)
    cv.line(img_with_line, (0, center_y - 110), (w, center_y - 110), (255, 0, 0), thickness)

    return img_with_line

def getImage(ip: str, choice: str) -> None:
    
    FPS = 1
    
    address = f'rtsp://admin:cepetro1234@{ip}?tcp&fps={FPS}'

    # Estabelecendo conexao
    cap = cv.VideoCapture(address,cv.CAP_FFMPEG)

    # Mudando o fps
    cap.set(cv.CAP_PROP_FPS, FPS)

    # Mudando o tamanho do buffer
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)

    if not cap.isOpened():
        print("Erro ao conectar ao fluxo RTSP. Verifique se as câmeras estão ligadas.")
        return
    
    num = int(input("Digite o número da foto:\n"))

    
    segundos = 3
    for i in range(segundos, -1, -1):
        print(f"Começando a filmagem em {i+1} segundos...")
        time.sleep(1)
        
    frames = 0
    
    print("\nCâmera pronta para tirar fotos.\n")
    
    tempos = []
    
    frames_ate_limpar = 30
    contador_de_frames = 0
    
    intervalo_de_frames = 50
    
    while cap.isOpened():
        tempo_inicio = time.time()
        ret, img = cap.read()
        
        if not ret:
            print("Erro ao conectar ao fluxo RTSP. Tentando reconectar...")
            cap.release()
            cap = cv.VideoCapture(address, cv.CAP_FFMPEG)
            cap.grab()
            time.sleep(1)
            continue
        
        tempo_passado = time.time() - tempo_inicio
        
        tempos.append(tempo_passado)
        
        if frames % 10 == 0: # Mostrar frame a cada 10 frames   
            cv.imshow('RTSP Frame', img)

        k = cv.waitKey(10)
        
        if k == 27:  # Pressione 'esc' para sair
            break

        if k == ord('r'):
            #print(ping(ip[:11]))
            print("Limpando Buffer...")
            cap.grab()
              
        elif k == ord('s'):  # Pressione 's' para salvar as imagens
            filename = f'img{num}_Camera{choice}.png'
            cv.imwrite(filename, img)
            print(f"Imagem salva: {filename}")
            num += 1
            
        if contador_de_frames >= frames_ate_limpar:
            for _ in range(5):
                cap.grab()
            contador_de_frames = 0
        
        
        frames += 1
        contador_de_frames += 1
                    
    # Apos fechar o video, todas as janelas são destruidas e a variavel reiniciada
    cap.release()
    cv.destroyAllWindows()
    
    
def plotar_grafico_tempos(tempos: list) -> None:
    plt.plot(tempos, marker='o', color='b', linestyle='-', markersize=8, markerfacecolor='red', markeredgewidth=2, markeredgecolor='red')
    plt.title("Gráfico dos tempos entre cada leitura de frame")
    plt.xlabel("Frames")
    plt.ylabel("Tempo")
    plt.grid(True)
    plt.show()

def getTwoImage(ip1: str, ip2:str, choice: str) -> None:
    address1 = 'rtsp://admin:cepetro1234@' + ip1 + '?tcp&fps=1'
    address2 = 'rtsp://admin:cepetro1234@' + ip2 + '?tcp&fps=1'
    cap1 = cv.VideoCapture(address1, cv.CAP_FFMPEG)
    cap2 = cv.VideoCapture(address2, cv.CAP_FFMPEG)
    cap1.set(cv.CAP_PROP_FPS, 1)
    cap2.set(cv.CAP_PROP_FPS, 1)

    if (not cap1.isOpened() or not cap2.isOpened()):
        print("Erro ao conectar ao fluxo RTSP. Verifique se as câmeras estão ligadas.")
        return
    
    # Buffer de Captura
    cap1.set(cv.CAP_PROP_BUFFERSIZE, 3)
    cap2.set(cv.CAP_PROP_BUFFERSIZE, 3)

    num = int(input("Digite o número da foto:\n"))
    print("Câmera pronta para tirar fotos.")
    
    while (cap1.isOpened() and cap2.isOpened()):
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()

        img1 = cv.resize(img1, (1280, 720))
        img2 = cv.resize(img2, (1280, 720))
        img1 = draw_horizontal_line(img1)
        img2 = draw_horizontal_line(img2)

        imagem_combinada = np.hstack((img2, img1))

        if (not ret1 or not ret2):
            print("Erro ao conectar ao fluxo RTSP. Tentando reconectar...")
            cap1.release()
            cap2.release()
            cap1 = cv.VideoCapture(address1, cv.CAP_FFMPEG)
            cap2 = cv.VideoCapture(address2, cv.CAP_FFMPEG)
            cap1.grab()
            cap2.grab()
            time.sleep(1)
            continue

        k = cv.waitKey(10)
        
        if k == 27:  # Pressione 'esc' para sair
            break

        if cv.waitKey(1) & 0xFF == ord('r'):
                print("Limpando Buffer...")
                clear_buffer_two(cap1, cap2)
        
        elif k == ord('s'):  # Pressione 's' para salvar as imagens
            #time.sleep(2)
            filename = f'imagemCombinada{num}_Camera{choice}.png'
            cv.imwrite(filename, imagem_combinada)
            print(f"Imagem salva: {filename}")
            num += 1
        cv.imshow('RTSP Frame', imagem_combinada)
                    
    # Apos fechar o video, todas as janelas são destruidas e a variavel reiniciada
    cap1.release()
    cap2.release()
    cv.destroyAllWindows()

# getTwoImage(CAMERA01, CAMERA02, "12")

if check_wifi(WIFI_NAME) == True:
    print("Voce esta conectado no Wi-Fi correto.\n")
else:
    print("Voce não esta conectado no Wi-Fi.")
    print("Por favor, conecte-se ao Wi-Fi correto para iniciar as câmeras.\n")
    exit()

camera=""

while True:
    choice = str(input("Qual câmera esta sendo utilizada?: [1/2]\n")).strip()
    if choice == "1":
        camera = CAMERA01
        print("CAMERA01 selecionada.")
        break
    elif choice == "2":
        camera = CAMERA02
        print("CAMERA02 selecionada.")
        break
    elif choice.lower() == "n":
        print("O programa foi interrompido.")
        exit()
    else:
        print("Digito incorreto. Digite novamente.\n")
        print("Digite 'n' para sair do programa.\n")

getImage(camera, choice)
