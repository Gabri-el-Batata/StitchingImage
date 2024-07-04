import cv2 as cv
import numpy as np


# Carrega a imagem
image_path = 'caliResult1.png'
image = cv.imread(image_path)

# Rotaciona a imagem
rotated_image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)

#rotated_image = cv.resize(rotated_image, (400, 600))

# Salva a imagem rotacionada
cv.imwrite('imagem_rotacionada_teste.png', rotated_image)

# Exibe a imagem original e a rotacionada
cv.imshow('Imagem Original', image)
cv.imshow('Imagem Rotacionada', rotated_image)
cv.waitKey(0)
cv.destroyAllWindows()
