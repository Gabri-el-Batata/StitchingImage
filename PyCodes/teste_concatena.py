import cv2 as cv
from concatenador import main_concatenador
from utils import equalizar_imagem_colorida

img1 = cv.imread(r"C:\Users\Adquiri\Documents\Camera_Batata\caliResult_Camera1.png".replace('\\', '/'))
img2 = cv.imread(r"C:\Users\Adquiri\Documents\Camera_Batata\caliResult_Camera2.png".replace('\\', '/'))

cv.imshow('', equalizar_imagem_colorida(main_concatenador(img2, img1)))
cv.imwrite('panorama.png', main_concatenador(img2, img1))
cv.waitKey(0)