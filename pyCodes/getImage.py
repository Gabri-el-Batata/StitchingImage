import cv2 as cv
import os

CAMERA01 = "192.168.0.7:554"

CAMERA03 = "192.168.0.9"

CAMERA02 = "192.168.0.8:554"

CAMERA02_CABO = "143.106.170.196"

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000" # 5 seconds

def ReadCamera(ip: str):
    address = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(address,cv.CAP_FFMPEG)

    # Verifique se a captura foi inicializada com sucesso
    if not cap.isOpened():
        print("Erro ao conectar ao fluxo RTSP")
        return
    
    # Defina um buffer de captura (se aplicável)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)

    num = 0
    print("Camera pronta para tirar fotos.")
    
    while cap.isOpened():
        ret, img = cap.read()

        if not ret:
            print("Erro ao ler o quadro")
            break
        
        k = cv.waitKey(10)
        
        if k == 27:  # Pressione 'esc' para sair
            break
        
        elif k == ord('s'):  # Pressione 's' para salvar as imagens
            filename = f'img{num}_Camera1.png'
            cv.imwrite(filename, img)
            print(f"Imagem salva: {filename}")
            num += 1
        
        cv.imshow('RTSP Frame', img)
    
    # Após fechar o vídeo, todas as janelas são destruídas e a variável reiniciada
    cap.release()
    cv.destroyAllWindows()

ReadCamera(CAMERA01)
