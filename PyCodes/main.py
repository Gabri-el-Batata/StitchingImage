import cv2 as cv
import os
from CAMERA_IPS import (CAMERA01, CAMERA02, WIFI_NAME)
import time
from glob import glob
from utils import check_wifi, confirma_escolha, getImage, get_data_pkl, remover_distorcao, plotar_duas_imagens, confirma_imagem, equalizar_imagem_colorida, confirma_leitura_imagens


current_directory = os.getcwd().replace('\\', '/')

# print("---------- Iniciando processo de capturar imagem ----------")

# #### Definir camera utilizada
# camera=""
# while True:
#     choice_camera = str(input("\n Qual câmera esta sendo utilizada?: [1/2]\n")).strip()
#     if choice_camera == "1":
#         camera = CAMERA01
#         print("CAMERA01 selecionada.")
#         break
#     elif choice_camera == "2":
#         camera = CAMERA02
#         print("CAMERA02 selecionada.")
#         break
#     else:
#         print("Digito incorreto. Digite novamente.\n")

# ### Verificar se o usuario esta conectado no Wi-Fi

# if check_wifi(WIFI_NAME) == True:
#     print("Voce esta conectado no wifi correto.")
#     getImage(camera, choice_camera)
# else:
#     print("Voce não esta conectado no wifi.")
#     exit()

choice_camera = str(input("De qual câmera você vai processar a imagem? [1/2]\n")).strip()

if choice_camera not in ['1', '2']:
    print("Você não digitou um número correto. Deve ser 1 ou 2.")

undistort_choice = str(input("\n ---------- Começar processo de remoção de distorção? [S/n] ---------- \n")).upper().strip()

confirma_escolha(undistort_choice)

cameraMatrix = f'/calibracao_camera1/cameraMatrix.pkl'
dist = f'/calibracao_camera1/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

print("Diretório para cameraMatrix: ", cameraMatrix_path)
print("Diretório para dist: ", dist_path)

choice = str(input("\n Esta correto?: [S/n]\n")).strip().upper()

confirma_escolha(choice)

data1 = get_data_pkl(cameraMatrix_path)
data2 = get_data_pkl(dist_path)

number = str(input("\nQual o número da imagem que você quer remover distorção?\n")).strip()

imagem_escolhida = f'img{number}_Camera{choice_camera}.png'

imagem_sem_distorcao = f'caliResult_Camera{choice_camera}.png'

#imagem_escolhida = current_directory + "/" + imagem_escolhida

confirma_imagem(imagem_escolhida)

def remover_distorcao_e_plotar(imagem_escolhida, data1, data2):

    img = cv.imread(current_directory + "/" + imagem_escolhida)

    dst = remover_distorcao(img, data1, data2)

    plotar_duas_imagens(img, dst)

    salvar_imagem = str(input("Gostaria de salvar a imagem sem distorção?: [S/n]\n")).strip().upper()

    if (salvar_imagem == "S" or salvar_imagem == ""):
        cv.imwrite(imagem_sem_distorcao, dst)
        print("A imagem foi salva como: ", imagem_sem_distorcao)
    else:
        print("A imagem não foi salva.")
        exit()

remover_distorcao_e_plotar(imagem_escolhida, data1, data2)

equalizar_choice = str(input("---------- Começar processo de equalização de imagem? [S/n] ---------- \n")).upper().strip()

confirma_imagem(imagem_sem_distorcao)

imagem_equalizada = equalizar_imagem_colorida(cv.imread(imagem_sem_distorcao))

nome_imagem_equalizada = 'equalized_' + imagem_sem_distorcao

plotar_duas_imagens(cv.imread(imagem_escolhida), imagem_equalizada)

choice = str(input("\nDeseja salvar a imagem equalizada? [S/n]\n")).strip().upper()

if (choice == "S" or choice ==""):
    print("Salvando imagem equalizada com o nome: ", nome_imagem_equalizada)
    cv.imwrite(nome_imagem_equalizada, imagem_equalizada)
else:
    print("As imagem não foi salva.")
    
#### Iniciar processo de concatenação

## Confirmar se o usuário possui as duas imagens requisitadas

# current_directory_imgs_path = current_directory + '/*.png'

# current_directory_imgs = glob(current_directory_imgs_path)

# if ('equalized_caliResult_Camera1.png' in current_directory_imgs) and ('equalized_caliResult_Camera2.png' in current_directory_imgs):
#     print("Você possui as duas imagens para realizar a concatenação.")
# else:
#     print("Você não possui as duas imagens para realizar a concatenação.")
#     exit()
    
# img1_path = current_directory + "/" + "equalized_caliResult_Camera2.png"
# img2_path = current_directory + "/" + "equalized_caliResult_Camera1.png"
