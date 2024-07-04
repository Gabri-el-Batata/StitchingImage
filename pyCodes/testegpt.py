import cv2
import numpy as np
from matplotlib import pyplot as plt

# Carregar as imagens
img2 = cv2.imread('C:/Users/Server/Documents/Camera_Batata/caliResult1_Camera2.png')
img1 = cv2.imread('C:/Users/Server/Documents/Camera_Batata/caliResult1_Camera1.png')

# Converter as imagens para escala de cinza
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Criar o detector de características SIFT
sift = cv2.SIFT_create()

# Detectar os pontos chave e calcular os descritores
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# Configurar o FLANN matcher
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

# Encontrar correspondências usando o KNN
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# Aplicar a razão de Lowe para selecionar boas correspondências
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Verificar se há correspondências suficientes
if len(good_matches) > 10:
    # Obter pontos correspondentes
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

    # Calcular a homografia
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Usar a homografia para transformar a imagem
    height, width, channels = img2.shape
    img1_warp = cv2.warpPerspective(img1, H, (width, height))

    # Inicializar o resultado com a imagem 2
    result = img2.copy()

    # Mesclar as imagens com blending
    for i in range(width):
        alpha = i / width
        result[:, i] = cv2.addWeighted(img1_warp[:, i], alpha, result[:, i], 1 - alpha, 0)

    # Mostrar o resultado
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
else:
    print("Não há correspondências suficientes entre as imagens.")
