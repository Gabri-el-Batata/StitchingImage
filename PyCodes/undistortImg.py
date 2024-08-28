import cv2 as cv
import pickle
import os
from matplotlib import pyplot as plt
from utils import plotar_duas_imagens, remover_distorcao, get_data_pkl

current_directory = os.getcwd().replace('\\', '/')

choice_camera = str(input("Qual câmera você capturou a imagem?: [1/2]\n")).strip()
#number = str(input("Qual o número da foto?\n")).strip()

cameraMatrix = f'/calibracao_camera1/cameraMatrix.pkl'
dist = f'/calibracao_camera1/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

print("Diretório para cameraMatrix: ", cameraMatrix_path)
print("Diretório para dist: ", dist_path)

choice = str(input("Esta correto?: [S/n]\n")).strip().upper()

if choice == "N":
    exit()

data1 = get_data_pkl(cameraMatrix_path)
data2 = get_data_pkl(dist_path)

############## UNDISTORTION #####################################################

img = cv.imread(current_directory + f'/img0_Camera{choice_camera}.png')

dst = remover_distorcao(img, data1, data2)

plotar_duas_imagens(img, dst)

salvar_imagem = str(input("Gostaria se salvar a imagem sem distorção?: [s/N]\n")).strip().upper()

if not(salvar_imagem == "N" or salvar_imagem == ""):
    cv.imwrite(f'caliResult_Camera{choice_camera}.png', dst)
else:
    exit()