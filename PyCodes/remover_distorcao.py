import cv2 as cv
import os
from utils import get_data_pkl, remover_distorcao, plotar_duas_imagens

caminho_para_foto = r'C:\Users\Adquiri\Documents\Camera_Batata\img0_Camera1_aruco.png'
current_directory = os.getcwd().replace('\\', '/')

index_choice_camera = caminho_para_foto.index('img')+ len('img') + 2 + len('Camera')
choice_camera = caminho_para_foto[index_choice_camera]
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

img = cv.imread(caminho_para_foto)

dst = remover_distorcao(img, data1, data2)

plotar_duas_imagens(img, dst)

salvar_imagem = str(input("Gostaria se salvar a imagem sem distorção?: [s/N]\n")).strip().upper()

if not(salvar_imagem == "N" or salvar_imagem == ""):
    cv.imwrite(f'caliResult_Camera{choice_camera}.png', dst)
else:
    exit()