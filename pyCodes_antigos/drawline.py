import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import plotar_duas_imagens

def draw_horizontal_line(img):
    h, w = img.shape[:2]
    center_y = h // 2
    color = (0, 255, 0)  # Verde
    thickness = 2

    img_with_line = img.copy()
    cv2.line(img_with_line, (0, center_y), (w, center_y), color, thickness)

    return img_with_line

# Carrega as imagens
img1_path = 'caliResult_Camera2.png'
img2_path = 'caliResult_Camera1.png'

img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)

# Desenha a linha horizontal no centro de cada imagem
img1_with_line = draw_horizontal_line(img1)
img2_with_line = draw_horizontal_line(img2)


plotar_duas_imagens(img1, img2)
