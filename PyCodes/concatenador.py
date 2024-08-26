import cv2 as cv
import numpy as np
from utils import get_current_directory, confirma_leitura_imagens, detectar_cantos_arucos, desenha_marcadores

current_directory = get_current_directory()
print("Esse é o diretório atual: ", current_directory)

img1_path = current_directory + "/" + "equalized_caliResult_Camera2.png"
img2_path = current_directory + "/" + "equalized_caliResult_Camera1.png"

image1, image2 = confirma_leitura_imagens(img1_path, img2_path)

# Configurar o dicionário e os parâmetros ArUco
aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters()

detector = cv.aruco.ArucoDetector(aruco_dict, parameters)

corners1, ids1, corners2, ids2 = detectar_cantos_arucos(image1, image2)

desenha_marcadores(image1, corners1, ids1)

# Pegar o centro do primeiro marcador encontrado em cada imagem
center1 = np.mean(corners1[0][0], axis=0)
center2 = np.mean(corners2[0][0], axis=0)

# Calcular o deslocamento entre as duas imagens
image2 = image2[:, int(center2[0]):]

# Dimensões das imagens
height1, width1, _ = image1.shape
height2, width2, _ = image2.shape

# Calcular a largura da nova imagem
new_width = int(center1[0]) + (width1-int(center2[0]))
new_height = max(height1, height2)

# Criar a nova imagem (panorama)
panorama = np.zeros((new_height, new_width, 3), dtype=np.uint8)

# Colocar a primeira imagem
panorama[:height1, :width1] = image1

# Colocar a segunda imagem com base no deslocamento calculado
panorama[:height2, int(center1[0]):] = image2

# Salvar ou exibir o resultado
cv.imshow('Panorama', panorama)
cv.waitKey(0)
cv.destroyAllWindows()

choice = str(input("Você deseja salvar a imagem final? [S/n]\n")).upper().split()

if not (choice == "S" or choice == ""):
    exit()

cv.imwrite('panorama_aruco.png', panorama)