import numpy as np
import cv2 as cv
from glob import glob
from pickle import dump
import os
from random import randint
from matplotlib import pyplot as plt
from utils import plotar_duas_imagens

def calcular_erro_projecao(objpoints, rvecs, tvecs, cameraMatrix, dist, imgpoints) -> None:
    mean_error = 0
    errors = []

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        errors.append(error)
        mean_error += error

    print( "Erro médio total: {}".format(mean_error/len(objpoints)))
    print(f"\nErros individuais: \n{errors}\n")

    plt.show()
    plt.plot(errors, marker='o', color='b', linestyle='-', markersize=8, markerfacecolor='red', markeredgewidth=2, markeredgecolor='red') 
    plt.title('Gráfico dos erros individuais')
    plt.xlabel('Imagens')
    plt.ylabel('Erro')

    if (mean_error/len(objpoints) < 0.5):
        print("Erro médio total baixo, a calibração ficou aceitável.")
    elif ( 0.5 < mean_error/len(objpoints) < 1.0):
        print("Erro médio total moderado, pode-se repetir a calibração.")
    else:
        print("Erro médio total alto, repita a calibração.")

def registra_calibracao(ret, cameraMatrix, dist, rvecs, tvecs) -> None:
    print("Registrando calibração no arquivo 'calibration_log.txt'.")

    with open('calibration_log.txt', 'w') as log_file:
        log_file.write(f"Camera calibrada: {ret}\n")
        log_file.write(f"\nMatriz da camera: \n{cameraMatrix}")
        log_file.write(f"\nParametros de distorcao: \n{dist}\n")
        log_file.write(f"\nVetores de rotacao: \n{rvecs}\n")
        log_file.write(f"\nVetores de translacao: \n{tvecs}\n")

def remover_distorcao(img, cameraMatrix, dist):
    h, w = img.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    # Undistort
    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    if roi[2] > 0 and roi[3] > 0:
        dst = dst[y:y+h, x:x+w]
    else: print("ROI invalida, sera usada a imagem completa.")

    return dst

def salvar_arquivos_calibracao(cameraMatrix, dist) -> None:
    dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
    dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
    dump(dist, open( "dist.pkl", "wb" ))

    print("Os arquivos foram salvos no diretório atual.")

def detectar_cantos(chessboardSize: tuple, tamanho_dos_quadrados_tabuleiro_mm: float, images, criteria):

    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
    
    objp = objp * tamanho_dos_quadrados_tabuleiro_mm

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

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
            #img = cv.resize(img, (1280, 720))
            cv.imshow('Imagem com tabuleiro desenhado', img)
            cv.waitKey(0)
    cv.destroyAllWindows()

    return objpoints, imgpoints, gray

chessboardSize = (6,9) # Quantidade de cantos

tamanho_dos_quadrados_tabuleiro_mm = 1

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

current_directory = os.getcwd().replace('\\', '/')
current_directory_imgs = current_directory + '/*.png'
print("Esse é o diretório que você esta tentando acessar, esta correto?: [\033[1mS\033[0m/n]", current_directory)
choice = str(input()).strip().upper()
if not (choice == "S" or choice == ""):
    exit()

images = glob(current_directory_imgs)

objpoints, imgpoints, gray = detectar_cantos(chessboardSize, tamanho_dos_quadrados_tabuleiro_mm, images, criteria)

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

registra_calibracao(ret, cameraMatrix, dist, rvecs, tvecs)

salvar_arquivos_calibracao(cameraMatrix, dist)

############## UNDISTORTION #####################################################

imagem_usada = images[randint(0, len(images))].replace('\\', '/')

print(f"A imagem que será usada para testar a calibração será: '{imagem_usada}'.")

img = cv.imread(imagem_usada)

dst = remover_distorcao(img, cameraMatrix, dist)

calcular_erro_projecao(objpoints, rvecs, tvecs, cameraMatrix, dist, imgpoints)

plotar_duas_imagens(img, dst)

salvar_imagem = str(input("Gostaria de salvar a imagem com distorção reduzida? [s/\033[1mN\033[0m]\n")).strip().upper()

if not (salvar_imagem == "N" or salvar_imagem == ""):
    cv.imwrite('caliResult1.png', dst)
    print("Imagem salva: 'caliResult1.png'")