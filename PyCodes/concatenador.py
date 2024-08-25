import cv2 as cv
import numpy as np
from utils import detect_markers

desired_aruco_dictionary = "DICT_6X6_250"

# Carregar as imagens
image1 = cv.imread("C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera2.png")
image2 = cv.imread("C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera1.png")

# A = image1.copy()
# B = image2.copy()

# print(A.shape, B.shape)

# gpA = [A]
# for i in range(6):
#     A = cv.pyrDown(A)
#     gpA.append(A)

# gpB = [B]
# for i in range(6):
#     B = cv.pyrDown(B)
#     gpB.append(B)

# lpA = [gpA[5]]
# for i in range(5, 0, -1):
#     GE = cv.pyrUp(gpA[i])
#     GE = cv.resize(GE, (gpA[i-1].shape[1], gpA[i-1].shape[0]))  # Redimensiona para garantir o mesmo tamanho
#     LA = cv.subtract(gpA[i-1], GE)
#     lpA.append(LA)

# lpB = [gpB[5]]
# for i in range(5, 0, -1):
#     GE = cv.pyrUp(gpB[i])
#     GE = cv.resize(GE, (gpB[i-1].shape[1], gpB[i-1].shape[0]))  # Redimensiona para garantir o mesmo tamanho
#     LB = cv.subtract(gpB[i-1], GE)
#     lpB.append(LB)


# LS = []

# for la, lb in zip(lpA, lpB):
#     cols, rows, _ = la.shape
#     ls = np.hstack((la[:, :cols//2], lb[:, cols//2:]))
#     LS.append(ls)

# lsc = LS[0]
# for i in range(1, 6):
#     lsc = cv.pyrUp(lsc)
#     lsc = cv.resize(lsc, (LS[i].shape[1], LS[i].shape[0]))
#     lsc = cv.add(lsc, LS[i])

# cv.imshow('piramid', lsc)
# cv.waitKey(0)

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
    new_width = int(center1[0]) + (width1-int(center2[0]))
    new_height = max(height1, height2)

    # Criar a nova imagem (panorama)
    panorama = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Colocar a primeira imagem
    panorama[:height1, :width1] = image1

    # Colocar a segunda imagem com base no deslocamento calculado
    panorama[:height2, int(center1[0]):] = image2

    # Salvar ou exibir o resultado
    #cv.imwrite('panorama_aruco.png', panorama)
    cv.imshow('Panorama', panorama)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("Não foram detectados marcadores ArUco em ambas as imagens.")
