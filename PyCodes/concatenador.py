import cv2 as cv
import numpy as np
from utils import get_current_directory, confirma_leitura_imagens, detectar_cantos_arucos, desenha_marcadores

current_directory = get_current_directory()

print("Esse é o diretório atual: ", current_directory)

# number = str(input("Qual número da imagem que você vai concatenar: \n")).strip()

img1_path = r"C:\Users\Adquiri\Documents\Camera_Batata\StitchingImage\caliResult_Camera2.png".replace('\\', '/')
img2_path = r"C:\Users\Adquiri\Documents\Camera_Batata\StitchingImage\caliResult_Camera1.png".replace('\\', '/')

image1, image2 = confirma_leitura_imagens(img1_path, img2_path)

corners1, ids1, corners2, ids2 = detectar_cantos_arucos(image1, image2)

def get_center(corners1, corners2):
    center1 = np.mean(corners1[0][0], axis=0)
    center2 = np.mean(corners2[0][0], axis=0)
    
    return (center1, center2)

def calcula_translacao(center1, center2) -> int:
    translation_x = int(center1[0] - center2[0])
    return translation_x

def concatena_imagens(image1, image2, center1, center2):
    
    image2 = image2[:, int(center2[0]):]

    # Dimensões das imagens
    height1, width1, _ = image1.shape
    height2, width2, _ = image2.shape

    # Calcular a largura da nova imagem
    new_width = int(center1[0]) + (1244-int(center2[0]))
    new_height = max(height1, height2)

    # Criar a nova imagem (panorama)
    panorama = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Colocar a primeira imagem
    panorama[:height1, :width1] = image1

    # Colocar a segunda imagem com base no deslocamento calculado
    panorama[:height2, int(center1[0]):] = image2
    
    return panorama

def main_concatenador(image1, image2):
    
    corners1, ids1, corners2, ids2 = detectar_cantos_arucos(image1, image2)

    center1, center2 = get_center(corners1, corners2)

    return concatena_imagens(image1, image2, center1, center2)
    
panorama = main_concatenador(image1, image2)

# Salvar ou exibir o resultado
cv.imshow('Panorama', panorama)
cv.waitKey(0)
cv.destroyAllWindows()
choice = str(input("Você deseja salvar a imagem final? [S/n]\n")).upper().strip()

if not (choice == "S" or choice == ""):
    exit()

cv.imwrite(f'panoramas/panorama_aruco_normal.png', panorama)
print("Salvando Panorama.")