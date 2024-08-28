import cv2 as cv
import os
from CAMERA_IPS import (CAMERA01, CAMERA02, WIFI_NAME)
import time
from utils import check_wifi, confirma_escolha, getImage, get_data_pkl, remover_distorcao, plotar_duas_imagens


current_directory = os.getcwd().replace('\\', '/')

camera=""
while True:
    choice_camera = str(input("Qual câmera esta sendo utilizada?: [1/2]\n")).strip()
    if choice_camera == "1":
        camera = CAMERA01
        print("CAMERA01 selecionada.")
        break
    elif choice_camera == "2":
        camera = CAMERA02
        print("CAMERA02 selecionada.")
        break
    else:
        print("Digito incorreto. Digite novamente.\n")

if check_wifi(WIFI_NAME) == True:
    print("Voce esta conectado no wifi correto.")
    getImage(camera, choice_camera)
else:
    print("Voce não esta conectado no wifi.")
    exit()

undistort_choice = str(input("---------- Começar processo de remoção de distorção? [S/n] ---------- \n")).upper().strip()

if confirma_escolha(undistort_choice) == False:
    exit()

cameraMatrix = f'/calibracao_camera1/cameraMatrix.pkl'
dist = f'/calibracao_camera1/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

print("Diretório para cameraMatrix: ", cameraMatrix_path)
print("Diretório para dist: ", dist_path)

choice = str(input("Esta correto?: [S/n]\n")).strip().upper()

if confirma_escolha == False:
    exit()

data1 = get_data_pkl(cameraMatrix_path)
data2 = get_data_pkl(dist_path)

number = str(input("Qual o número da imagem que você quer remover distorção? ")).strip()

imagem_escolhida = f'img{number}_Camera{choice_camera}.png'

def remover_distorcao_e_plotar(imagem_escolhida, data1, data2):

    img = cv.imread(current_directory + '/' + imagem_escolhida)

    dst = remover_distorcao(img, data1, data2)

    plotar_duas_imagens(img, dst)

    salvar_imagem = str(input("Gostaria se salvar a imagem sem distorção?: [s/N]\n")).strip().upper()

    if not(salvar_imagem == "N" or salvar_imagem == ""):
        cv.imwrite(f'caliResult_Camera{choice_camera}.png', dst)
    else:
        exit()

remover_distorcao_e_plotar(imagem_escolhida, data1, data2)

# choice_equalizar = 