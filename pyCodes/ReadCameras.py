import cv2 as cv
import time
from datetime import datetime

adress = "rtsp://admin:cepetro1234@"
CAMERA01 = "192.168.0.7"
CAMERA02 = "192.168.0.8"

def ReadCamera(ip1: str, ip2: str):
    # Leitura da Camera
    adress1 = adress + ip1
    adress2 = adress + ip2
    
    cap1 = cv.VideoCapture(adress1)
    cap2 = cv.VideoCapture(adress2)
    
    while True:
        ret1, img1 = cap1.read() # Lendo
        ret2, img2 = cap2.read()

        if ret1 == True and ret2 == True:
            cv.imshow('Camera1', img1) # Mostrando
            cv.imshow('Camera2', img2)

            k = cv.waitKey(5) # Expressao regular
            if k == 27: # Pressione esc para sair
                break
        #print(img.shape)
          
    # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap1.release()
    cap2.release()
    cv.destroyAllWindows()
    
    
def takeVideo(ip1:str, name:str):
    
    
    print("Gravação iniciada.")
    adress1 = adress + ip1
    cap1 = cv.VideoCapture(adress1)
    
    if not cap1.isOpened():
        print("Erro ao abrir uma das câmeras.")
        exit()

    frame_width = int(cap1.get(3))
    frame_height = int(cap1.get(4))
    fps = 20
    
    # current_time = datetime.now().strftime('%S')
    
    fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    name = 'output' + name + '.avi'
    try:
        out = cv.VideoWriter(name, fourcc, fps, (frame_width, frame_height))
    except Exception as ex:
        print(ex)
        
    start = time.time()
    while (time.time() - start) <= 10:
        ret1, frame1 =cap1.read()
        
        if not ret1:
            print("Erro.")
            exit()
        out.write(frame1) 
        #cv.imshow('Frame', frame1) 
            
    print("Gravação finalizada")
    
    cap1.release()
    out.release()
    cv.destroyAllWindows()
    
takeVideo(CAMERA02, '3')
