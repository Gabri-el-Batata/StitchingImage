import cv2 as cv
import numpy as np
from utils import detect_markers

desired_aruco_dictionary = "DICT_6X6_250"

# Carregar as imagens
image1 = cv.imread("C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera2.png")
image2 = cv.imread("C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera1.png")


# Configurar o dicionário e os parâmetros ArUco
aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters()

detector = cv.aruco.ArucoDetector(aruco_dict, parameters)

# Detectar os marcadores ArUco na primeira imagem
corners1, ids1, _ = detector.detectMarkers(image1)
# Detectar os marcadores ArUco na segunda imagem
corners2, ids2, _ = detector.detectMarkers(image2)

# Verificar se pelo menos um marcador foi detectado em cada imagem
if len(corners1) > 0 and len(corners2) > 0:
    # Pegar o centro do primeiro marcador encontrado em cada imagem
    center1 = np.mean(corners1[0][0], axis=0)
    center2 = np.mean(corners2[0][0], axis=0)

    print("centro1", center1)
    print("centro2", center2)
    
    # Calcular o deslocamento entre as duas imagens
    translation_x = int(center1[0] - center2[0])

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

    cv.imshow('', panorama)

    # Colocar a segunda imagem com base no deslocamento calculado
    panorama[:height2, int(center1[0]):] = image2

    # Salvar ou exibir o resultado
    cv.imwrite('panorama_aruco.png', panorama)
    cv.imshow('Panorama', panorama)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Não foram detectados marcadores ArUco em ambas as imagens.")
