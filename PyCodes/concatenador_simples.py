import cv2 as cv
import numpy as np

img1 = "C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera1.png"
img2 = "C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera2.png"

img1 = cv.imread(img1)
img2 = cv.imread(img2)

img1 = img1[:, 484:]

cv.imshow('imagem concatenada', img1)
cv.waitKey(0)