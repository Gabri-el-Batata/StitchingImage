import cv2 as cv
import numpy as np

# Carregar a imagem original
image = cv.imread('C:/Users/gabri/Documents/Camera_Batata/panoramas/panorama_aruco.png')

height, width, _= image.shape

# Definir a área da linha de sobreposição
overlap_start = width // 2 - 25 + 125  # Ajuste conforme necessário
overlap_end = overlap_start + 30  # Ajuste conforme necessário

# Extrair a área de sobreposição
overlap_area = image[:, overlap_start:overlap_end]

# Aplicar desfoque na área de sobreposição
blurred_overlap = cv.GaussianBlur(overlap_area, (5, 5), 0)

# Substituir a área de sobreposição pela versão desfocada
image[:, overlap_start:overlap_end] = blurred_overlap

# Exibir o resultado
cv.imwrite('panorama_aruco_blur.png', image)
cv.imshow('Panorama Suavizado', image)
cv.waitKey(0)
cv.destroyAllWindows()
