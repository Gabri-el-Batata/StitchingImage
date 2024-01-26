import numpy as np
import cv2 as cv
import glob
import pickle

################ ACHAR CANTOS DO TABULEIRO DE XADREZ - PONTOS DO OBJETO E PONTOS DA IMAGEM #############################

# Quantidade de cantos do tabuleiro impresso
chessboardSize = (9,6) 

# Resolucao da imagem
frameSize = (720,1280) 

# critério de rescisão
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# Preparando pontos do objeto

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
# Listas para armazenar os pontos do objeto e os pontos das imagens

objpoints = []
imgpoints = []


# Abrindo o caminho das imagens
images = glob.glob('C:/Users/PC_APB/Documents/Camera_Batata/imagesSecondCamera/*.png') 


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

############## Calibracao #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

print("Camera calibrada: ", ret)
print("\nMatriz da camera: \n", cameraMatrix)
print("\nParametros de distorcao: \n", dist)
print("\nVetores de rotacao: \n", rvecs)
print("\nVetores de translacao: \n", tvecs)


# Salvar os resultados para usar depois
pickle.dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
pickle.dump(dist, open( "dist.pkl", "wb" ))


############## Retirar Distorcao da Imagem #####################################################

img = cv.imread('C:/Users/PC_APB/Documents/Camera_Batata/imagesSecondCamera/img8.png')
print(img)
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))


# Retirando distorsao
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# Cortar a imagem (Apos retirar distorsao a imagem muda de tamanho)
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('caliResult1.png', dst)

# Reprojetando o erro
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )