from camera_classe import Camera, Wifi, WIFI_NAME
from imagem_classe import Imagem
from CAMERA_IPS import CAMERA01, CAMERA02
from utils import get_current_directory
from glob import glob
import os
import cv2 as cv

def mostra_arquivos(diretorio:str):
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

diretorio_atual = get_current_directory()

wifi = Wifi(WIFI_NAME)

wifi.verify_wifi()

Camera1 = Camera(1, CAMERA01, 3)

# Camera1.getFrame()

lista_imagens = mostra_arquivos(diretorio_atual)

lista_imagens_objetos = [Imagem(endereco_imagem) for endereco_imagem in lista_imagens]

for imagem in lista_imagens_objetos:
    cv.imshow(imagem.get_endereco, imagem.getImage())
    cv.waitKey(0)

cv.destroyAllWindows()