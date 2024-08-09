import cv2 as cv
import os
from CAMERA_IPS import (CAMERA01, CAMERA02)
import time

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000" # 5 seconds

def ReadCamera(ip: str, choice: str):
    address = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(address,cv.CAP_FFMPEG)

    if not cap.isOpened():
        print("Erro ao conectar ao fluxo RTSP.")
        return
    
    # Buffer de Captura
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)

    num = 0
    print("Camera pronta para tirar fotos.")
    
    
    while cap.isOpened():
        ret, img = cap.read()

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
choice = str(input("Qual câmera esta sendo utilizada?: [1/2]\n")).strip()
if choice == "1":
    camera = CAMERA01
elif choice == "2":
    camera = CAMERA02

ReadCamera(camera, choice)