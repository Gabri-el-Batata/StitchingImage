import cv2 as cv
from time import time
from CAMERA_IPS import (CAMERA01, CAMERA02)

def ReadCamera(ip1:str, ip2:str):
    defaultAdress = 'rtsp://admin:cepetro1234@'
    adress1 = defaultAdress + ip1
    adress2 = defaultAdress + ip2
    cap1, cap2 = cv.VideoCapture(adress1), cv.VideoCapture(adress2)
    cap1.set(cv.CAP_PROP_BUFFERSIZE, 3), cap2.set(cv.CAP_PROP_BUFFERSIZE, 3)
    while True:
        ret1, img1 = cap1.read() # Lendo
        ret2, img2 = cap2.read()

        if ret1 == True and ret2 == True:
            cv.imshow('Video - HikVision', img1) # Mostrando
            cv.imshow('Video', img2)

            k = cv.waitKey(5) # Expressao regular
            if k == 27: break # Pressione esc para sair
          
    # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap1.release()
    cap2.release()
    cv.destroyAllWindows()
    
ReadCamera(CAMERA01, CAMERA02)
