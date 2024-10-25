import cv2 as cv
from concatenador import main_concatenador
from utils import equalizar_imagem_colorida
import numpy as np

img1 = cv.imread(r"StitchingImage\fotos2410\caliResult_Camera1.png".replace('\\', '/'))
img2 = cv.imread(r"StitchingImage\fotos2410\caliResult_Camera2.png".replace('\\', '/'))


# Converter para escala de cinza
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

# Detectar pontos de interesse e descrever características usando o SIFT
sift = cv.SIFT_create()
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# Realizar a correspondência dos pontos usando o FLANN Matcher
index_params = dict(algorithm=1, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# Filtrar as melhores correspondências usando a razão de Lowe
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Obter os pontos das correspondências filtradas
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# Calcular a matriz de homografia
H, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

# Aplicar a transformação usando warpPerspective
height, width, channels = img2.shape
result = cv.warpPerspective(img1, H, (width, height))

cv.imshow('', result)
cv.waitKey(0)

cv.imshow('', main_concatenador(img2, result))
cv.imwrite('panorama_homografico.png', main_concatenador(img2, result))
cv.waitKey(0)