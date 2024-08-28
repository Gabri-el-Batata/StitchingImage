import cv2 as cv
import os
from CAMERA_IPS import (CAMERA01, CAMERA02)
import time
from utils import check_wifi

WIFI_NAME = "CompVisio"

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000" # 5 seconds

def draw_horizontal_line(img):
    h, w = img.shape[:2]
    center_y = h // 2
    color = (0, 0, 255)  # Verde
    thickness = 2

    img_with_line = img.copy()
    cv.line(img_with_line, (0, center_y), (w, center_y), color, thickness)
    cv.line(img_with_line, (0, center_y + 70), (w, center_y + 70), (0, 255, 0), thickness)
    cv.line(img_with_line, (0, center_y - 70), (w, center_y - 70), (255, 0, 0), thickness)

    return img_with_line

def getImage(ip: str, choice: str):
    address = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(address,cv.CAP_FFMPEG)

    if not cap.isOpened():
        print("Erro ao conectar ao fluxo RTSP. Verifique se as câmeras estão ligadas.")
        return
    
    # Buffer de Captura
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)

    num = int(input("Digite o número da foto:\n"))
    print("Camera pronta para tirar fotos.")
    
    while cap.isOpened():
        ret, img = cap.read()

        #img = draw_horizontal_line(img)

        if not ret:
            print("Erro ao conectar ao fluxo RTSP. Tentando reconectar...")
            cap.release()
            cap = cv.VideoCapture(address, cv.CAP_FFMPEG)
            time.sleep(1)
            continue

        k = cv.waitKey(10)
        
        if k == 27:  # Pressione 'esc' para sair
            break
        
        elif k == ord('s'):  # Pressione 's' para salvar as imagens
            #time.sleep(2)
            filename = f'img{num}_Camera{choice}.png'
            cv.imwrite(filename, img)
            print(f"Imagem salva: {filename}")
            num += 1
        cv.imshow('RTSP Frame', img)
                    
    # Apos fechar o video, todas as janelas são destruidas e a variavel reiniciada
    cap.release()
    cv.destroyAllWindows()

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
    else:
        print("Digito incorreto. Digite novamente.\n")

if check_wifi(WIFI_NAME) == True:
    print("Voce esta conectado no wifi correto.")
    getImage(camera, choice)
else:
    print("Voce não esta conectado no wifi.")
    exit()