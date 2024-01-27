import numpy as np
import cv2 as cv
from glob import glob
import pickle

def reconhecerPadroes(chessboardSize: list[int], imagesPath:str):
    '''
    Reconhecer os padroes do tabuleiro cujo tamanho deve ser passado como parametro
    Devolvera a lista com os pontos de objeto e pontos de imagem
    '''
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    # Listas para armazenar os pontos do objeto e os pontos das imagens
    objpoints = []
    imgpoints = []

    # Abrindo o caminho das imagens
    images = glob(imagesPath) 

    for image in images:

        img = cv.imread(image)

        # Mudando a tonaliade para cinza para encontrar os cantos mais facilmente
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Achar os cantos do tabuleiro
        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        # Se encontrar adicionar nas listas apos refina-los
        if ret == True:

            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # Desenhar e mostrar os cantos
            cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(1000)
    cv.destroyAllWindows()
    return (objpoints, imgpoints)

############## Calibracao #######################################################
    
def calibraCamera(chessboardSize:tuple(int), frameSize:tuple(int), imagePath:str):
    '''
    Essa funcao calibra determina uma nova matriz para camera e os coeficientes de distorsao
    com base nos pontos de imagem e objeto
    '''

    objpoints, imgpoints = reconhecerPadroes(chessboardSize)

    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

    print("Camera calibrada: ", ret)
    print("\nMatriz da camera: \n", cameraMatrix)
    print("\nParametros de distorcao: \n", dist)
    print("\nVetores de rotacao: \n", rvecs)
    print("\nVetores de translacao: \n", tvecs)


    # Salvar os resultados para usar depois
    pickle.dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
    pickle.dump(dist, open( "dist.pkl", "wb" ))

    return (cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints)


############## Retirar Distorcao da Imagem #####################################################


def retiraDistorsao(imagePath:str, cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints):
    '''
    Essa funcao tem objetivo de retirar a distorcao da imagem com base nos parametros medidos
    '''

    img = cv.imread(imagePath)
    h, w = img.shape[:2]

    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # Cortar a imagem (Apos retirar distorsao a imagem muda de tamanho)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite('caliResult1.png', dst)

    # Erro de Projeção
    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error

    print( "total error: {}".format(mean_error/len(objpoints)) )

if __name__ == '__main__':
    chessboardSize = (9,6) 
    frameSize = (720,1280)
    imagesPath = 'C:/Users/PC_APB/Documents/Camera_Batata/imagesSecondCamera/*.png'
    imagePath = 'C:/Users/PC_APB/Documents/Camera_Batata/imagesSecondCamera/img5.png'

    cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints = calibraCamera(chessboardSize, frameSize, imagesPath)

    retiraDistorsao(imagesPath, cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints)
