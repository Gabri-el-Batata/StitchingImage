import numpy as np
import cv2 as cv
import glob
import pickle
import os
import random
import matplotlib as plt

chessboardSize = (6,9) # Quantidade de cantos

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

tamanho_dos_quadrados_tabuleiro_mm = 23.6
objp = objp * tamanho_dos_quadrados_tabuleiro_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

current_directory = os.getcwd().replace('\\', '/')
current_directory_imgs = current_directory + '/*.png'

print("Esse é o diretório que voce esta tentando acessar, esta correto?: [\033[1mS\033[0m/N] ", current_directory)
choice = str(input()).strip().upper()
if not (choice == "S" or choice == ""):
    exit()

images = glob.glob(current_directory_imgs)

for image in images:

    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)


cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera calibrada: ", ret)
print("\nMatriz da camera: \n", cameraMatrix)
print("\nParametros de distorcao: \n", dist)
print("\nVetores de rotacao: \n", rvecs)
print("\nVetores de translacao: \n", tvecs)


# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
pickle.dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
pickle.dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
pickle.dump(dist, open( "dist.pkl", "wb" ))

print("Os arquivos foram salvos no diretório atual.")
############## UNDISTORTION #####################################################

imagem_usada = images[random.randint(0, 14)]

print(f"A imagem que será usada para testar a calibração será '{imagem_usada}'.")

img = cv.imread(current_directory + f'/{imagem_usada}')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))


# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
if roi[2] > 0 and roi[3] > 0:
    dst = dst[y:y+h, x:x+w]
else: print("ROI invalida, sera usada a imagem completa.")

cv.imwrite('caliResult1.png', dst)

print("Imagem salva: 'caliResult1.png'")

# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )


if (mean_error/len(objpoints) < 0.5):
    print("Erro baixo, a calibração ficou aceitável.")
elif ( 0.5 < mean_error/len(objpoints) < 1.0):
    print("Erro moderado, pode-se repetir a calibração.")
else:
    print("Erro alto, repita a calibração.")

plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.imshow(imagem_usada)
plt.title('Imagem 1 - Imagem com distorção.')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(dst)
plt.title('Imagem 2 - Imagem sem distorção.')
plt.axis('off')

plt.show()