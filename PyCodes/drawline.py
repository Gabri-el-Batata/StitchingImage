import cv2
import numpy as np
from matplotlib import pyplot as plt

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

# Exibe as imagens
plt.figure(figsize=(20, 10))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img1_with_line, cv2.COLOR_BGR2RGB))
plt.title('Imagem 1 com Linha Centralizada')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(img2_with_line, cv2.COLOR_BGR2RGB))
plt.title('Imagem 2 com Linha Centralizada')
plt.axis('off')

plt.show()
