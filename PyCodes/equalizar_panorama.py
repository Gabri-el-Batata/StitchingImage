import cv2 as cv
import numpy as np
from utils import equalizar_imagem_colorida

imagem = cv.imread('/home/ml1/Documents/Camera_Batata/StitchingImage/panoramas/panorama_aruco.png')

imagem = equalizar_imagem_colorida(imagem)

cv.imshow('', imagem)
cv.waitKey(0)

