import cv2 as cv
from time import time
import os
from CAMERA_IPS import CAMERA01, CAMERA02

# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h265_cuvid"


def ReadCamera(ip:str):
    adress = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(adress, cv.CAP_FFMPEG)
    # Defina um buffer de captura (se aplicável)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)
    while (cap.isOpened()):
        ret, img = cap.read() # Lendo
        cap.set(cv.CAP_PROP_BUFFERSIZE, 3)
        img = cv.GaussianBlur(img, (5, 5), 0)
        if not ret: break
        cv.imshow('RTSP Frame', img)
        if cv.waitKey(1) & 0xFF == ord('q'): # Pressione 'q' para parar o programa
            break
      
   # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    ReadCamera(CAMERA02)