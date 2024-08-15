import cv2
from matplotlib import pyplot as plt

# Carregar as imagens
img1 = cv2.imread('caliResult_Camera1.png')
img2 = cv2.imread('caliResult_Camera2.png')

# Converter para escala de cinza
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Equalizar o histograma
equalized1 = cv2.equalizeHist(gray1)
equalized2 = cv2.equalizeHist(gray2)

# Converter de volta para BGR para manter a consistência de cores
equalized_img1 = cv2.cvtColor(equalized1, cv2.COLOR_GRAY2BGR)
equalized_img2 = cv2.cvtColor(equalized2, cv2.COLOR_GRAY2BGR)

plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.imshow(equalized_img2)
plt.title('Imagem 2 equalizada.')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(equalized_img1)
plt.title('Imagem 1 equalizada')
plt.axis('off')

plt.show()

cv2.imwrite('equalized_caliResult_Camera1.png', equalized_img1)
cv2.imwrite('equalized_caliResult_Camera2.png', equalized_img2)

# cv2.waitKey(0)

# cv2.destroyAllWindows()