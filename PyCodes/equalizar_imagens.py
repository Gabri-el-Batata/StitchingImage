import cv2
from matplotlib import pyplot as plt
from utils import plotar_duas_imagens, equalizar_imagem_colorida

img1 = cv2.imread('caliResult_Camera1.png')
img2 = cv2.imread('caliResult_Camera2.png')

equalized_img1 = equalizar_imagem_colorida(img1)
equalized_img2 = equalizar_imagem_colorida(img2)

plotar_duas_imagens(img1, equalized_img1)

choice = str(input("Deseja salvar as imagens equalizadas? [S/n]\n")).strip().upper()
if (choice == "S" or choice ==""):
    print("Salvando as imagens equalizadas.")
    cv2.imwrite('equalized_caliResult_Camera1.png', equalized_img1)
    cv2.imwrite('equalized_caliResult_Camera2.png', equalized_img2)
else:
    print("As imagens não foram salvas.")
