import cv2 as cv
import pickle

def ReadCameraCalib(ip:str):
    # Leitura da Camera
    adress = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(adress)
    
    h, w  = [720, 1280]
    
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(pickle.load(open(".\calibrationUse\cameraMatrix.pkl", "rb")), # Matriz da camera
                            pickle.load(open("dist.pkl", "rb")), # Parametro de distorsao
                            (w,h), 1, (w,h))
    
    while True:
        ret, img = cap.read() # Lendo

        # Definindo uma nova matriz para a camera com base nos parametros da calibracao

        dst = cv.undistort(img, pickle.load(open(".\calibrationUse\cameraMatrix.pkl", "rb")), pickle.load(open(".\calibrationUse\dist.pkl", "rb")), None, newCameraMatrix)
        
        # Tem que fazer esse recorte na imagem se nao o .imshow() fica estranho
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        
        if ret == True:
            cv.imshow('Video - HikVision', dst) # Mostrando

            k = cv.waitKey(5) # Expressao regular
            if k == 27: # Pressione esc para sair
                break
        #print(img.shape)
          
    # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap.release()
    cv.destroyAllWindows()
    
ReadCameraCalib("169.254.46.55")

# Ip camera 2 = "169.254.68.41" 
# Ip camera 1 = "169.254.103.169" ou "169.254.46.55"