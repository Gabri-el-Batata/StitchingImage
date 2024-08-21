import cv2 as cv
import numpy as np
from utils import detect_markers

desired_aruco_dictionary = "DICT_6X6_250"

# Carregar as imagens
image1 = cv.imread('C:/Users/Server/Documents/Camera_Batata/StitchingImage/equalized_caliResult_Camera2.png')
image2 = cv.imread('C:/Users/Server/Documents/Camera_Batata/StitchingImage/equalized_caliResult_Camera1.png')

# Configurar o dicionário e os parâmetros ArUco
aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()

# Detectar os marcadores ArUco na primeira imagem
corners1, ids1, _ = cv.aruco.detectMarkers(image1, aruco_dict, parameters=parameters)
# Detectar os marcadores ArUco na segunda imagem
corners2, ids2, _ = cv.aruco.detectMarkers(image2, aruco_dict, parameters=parameters)

# Verificar se pelo menos um marcador foi detectado em cada imagem
if len(corners1) > 0 and len(corners2) > 0:
    # Pegar o centro do primeiro marcador encontrado em cada imagem
    center1 = np.mean(corners1[0][0], axis=0)
    center2 = np.mean(corners2[0][0], axis=0)
    
    # Calcular o deslocamento entre as duas imagens
    translation_x = int(center1[0] - center2[0])

    # Dimensões das imagens
    height1, width1, _ = image1.shape
    height2, width2, _ = image2.shape

    # Calcular a largura da nova imagem
    new_width = width1 + abs(translation_x) + width2
    new_height = max(height1, height2)

    # Criar a nova imagem (panorama)
    panorama = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Colocar a primeira imagem
    panorama[:height1, :width1] = image1

    # Colocar a segunda imagem com base no deslocamento calculado
    panorama[:height2, width1 - translation_x:width1 - translation_x + width2] = image2

    # Salvar ou exibir o resultado
    cv.imwrite('panorama_aruco.png', panorama)
    cv.imshow('Panorama', panorama)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Não foram detectados marcadores ArUco em ambas as imagens.")
