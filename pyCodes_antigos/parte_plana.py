import cv2
import numpy as np

undistorted_img = cv2.imread(r'C:\Users\Adquiri\Documents\Camera_Batata\caliResult1.png'.replace('\\', '/'))

# Converter para escala de cinza
gray = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)

# Aplicar Sobel para detectar bordas e gradientes
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

# Calcular a magnitude do gradiente
magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

# Normalizar para visualização
magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Definir limiar para identificar áreas com baixo gradiente (áreas planas)
_, flat_areas = cv2.threshold(magnitude, 30, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('Áreas mais planas', flat_areas)
cv2.waitKey(0)
cv2.destroyAllWindows()
