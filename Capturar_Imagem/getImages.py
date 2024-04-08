import cv2 as cv
from time import time

defaultAdress = 'rtsp://admin:cepetro1234@'

def getImages(img1, img2, num):
    start1 = time()
    cv.imwrite(f'pictures/fotoL{num}.png', img2)
    end1 = time()
    start2 = time()
    cv.imwrite(f'pictures/fotoR{num}.png', img1)
    end2 = time()
    print(f'images saved\ntempo1: {end1 - start1}\ntempo2: {end2 - start2}')
    num += 1

def ReadCamera(ip1:str, ip2:str):
    # Leitura da Camera
    global defaultAdress
    adress1 = defaultAdress + ip1
    adress2 = defaultAdress + ip2
    
    cap1 = cv.VideoCapture(adress1)
    cap2 = cv.VideoCapture(adress2)
    
    num = 0
    
    while True:
        ret1, img1 = cap1.read() # Lendo
        ret2, img2 = cap2.read()
        

        if ret1 == True and ret2 == True:
            cv.imshow('Video - HikVision', img1) # Mostrando
            cv.imshow('Video', img2)

            k = cv.waitKey(5) # Expressao regular
            if k == 27: # Pressione esc para sair
                break
            elif k == ord('s'):
                getImages(img2, img1, num)
                
    # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap1.release()
    cap2.release()
    cv.destroyAllWindows()
    
ReadCamera("143.106.170.250", "143.106.170.251")
