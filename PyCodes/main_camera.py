from camera_classe import Camera, Wifi, WIFI_NAME
from imagem_classe import Imagem
from CAMERA_IPS import CAMERA01, CAMERA02
from utils import get_current_directory
import os
import cv2 as cv
from concatenador import main_concatenador
import time
import pathlib

def mostra_arquivos(diretorio:str) -> list:
    arquivos = os.listdir(diretorio)

    if [arq.endswith('.png') for arq in arquivos].count(True) == 0:
        print("Não há imagens no diretório.")
        exit()
    
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
Camera2 = Camera(1, CAMERA02, 3, 2)

#Camera1.getFrame()
#Camera2.getFrame()

lista_imagens = mostra_arquivos(diretorio_atual)

lista_imagens_objetos = [Imagem(endereco_imagem, endereco_imagem[3]) for endereco_imagem in lista_imagens]

# Remover distorção de cada imagem e salvar essas imagens sem distorcao

# Erro gravissimo de remover distorção de todas as imagens que estao no diretorio !!!!
# Consertar essa linha de codigo urgentemente

print("-"*7, " INICIANDO CALIBRAÇÃO ", 7*"-", "\n")
print("Iniciando a remoção da distorção das imagens em:\n")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# Verificar se a pasta onde vou salvar as imagens sem distorcao ja existe e se nao existir, criar uma
pasta_imagens_sem_distorcao_nome = 'imagens_sem_dist'

pasta_imagens_sem_distorcao = pathlib.Path(pasta_imagens_sem_distorcao_nome)
if not pasta_imagens_sem_distorcao.exists():
    pasta_imagens_sem_distorcao.mkdir(parents=True, exist_ok=True)
    print(f"A pasta {pasta_imagens_sem_distorcao} foi criada com sucesso!\n")

lista_imagens_sem_dist_obj = []
for imagem in lista_imagens_objetos:
    nome_imagens_sem_dist = f'{pasta_imagens_sem_distorcao_nome}/caliResult{imagem.get_tag}_Camera{imagem.get_endereco[-5]}.png'
    cv.imwrite(nome_imagens_sem_dist, imagem.remove_distorcao())
    lista_imagens_sem_dist_obj.append(Imagem(nome_imagens_sem_dist, imagem.get_tag))

# Concatenar imagens da camera1 e camera2 (somente se tiver essas duas imagens respectivamente)

try:
    imagem1_sem_dist = Imagem(f'{pasta_imagens_sem_distorcao_nome}/caliResult0_Camera1.png')
    imagem2_sem_dist = Imagem(f'{pasta_imagens_sem_distorcao_nome}/caliResult0_Camera2.png')
except Exception as e:
    print("Não foi possível carregar as imagens. Verifique se as imagens estão no diretório.")
    exit()

if localizar_cam1_cam2(lista_imagens):
    try:
        panorama = main_concatenador(imagem2_sem_dist.getImage(), imagem1_sem_dist.getImage()) 
    except Exception as e:
        print("Não foi possível realizar a concatenação.")
        exit()
    
    cv.imshow("Panorama", panorama)
    cv.waitKey(0)

    cv.destroyAllWindows()
else:
    print("Não é possível fazer a concatenação.")