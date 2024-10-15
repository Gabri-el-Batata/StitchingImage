from camera_classe import Camera, Wifi, WIFI_NAME
from imagem_classe import Imagem
from CAMERA_IPS import CAMERA01, CAMERA02
from utils import get_current_directory
import os
import cv2 as cv
from concatenador import main_concatenador

def mostra_arquivos(diretorio:str) -> list:
    arquivos = os.listdir(diretorio)
    
    print("\nEssas são as fotos que estão no diretorio especificado:")
    cont = 0
    lista_imagens = []
    for arq in arquivos:
        if arq.endswith('.png') and os.path.isfile(os.path.join(diretorio, arq)):
            cont += 1
            print(arq)
            lista_imagens.append(arq)
            
    if cont == 0: exit()
    return lista_imagens

def localizar_cam1_cam2(lista_imagens:list[str]) -> bool:
    c1, c2 = 0, 0
    for elemento in lista_imagens:
        if "Camera1" in elemento:
            c1 += 1
        elif "Camera2" in elemento:
            c2 += 1     
        if c1 == c2:
            break
    return c1 == c2
    
diretorio_atual = get_current_directory()

wifi = Wifi(WIFI_NAME)

wifi.verify_wifi()

Camera1 = Camera(1, CAMERA01, 3, 1)

#Camera1.getFrame()

lista_imagens = mostra_arquivos(diretorio_atual)

lista_imagens_objetos = [Imagem(endereco_imagem) for endereco_imagem in lista_imagens]

# Remover distorção de cada imagem e salvar essas imagens sem distorcao
for imagem in lista_imagens_objetos:
    cv.imwrite(f'caliResult_Camera{imagem.get_endereco[-5]}.png', imagem.remove_distorcao())

# Concatenar imagens da camera1 e camera2 (somente se tiver essas duas imagens respectivamente)
if localizar_cam1_cam2(lista_imagens):
    panorama = main_concatenador(lista_imagens_objetos[0], lista_imagens_objetos[1])

    cv.imshow("Panorama", panorama)
    cv.waitKey(0)

    cv.destroyAllWindows()
else:
    print("Não é possível fazer a concatenação.")