import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('C:/Users/gabri/Documents/Camera_Batata/fotos2908/img0_Camera2.png', cv2.IMREAD_GRAYSCALE)

# Aplicar a Transformada de Fourier
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# Criar um filtro de rejeição de alta frequência
rows, cols = image.shape
crow, ccol = rows // 2, cols // 2
mask = np.ones((rows, cols, 2), np.uint8)
r = 30  # Raio do filtro de rejeição
center = (crow, ccol)
cv2.circle(mask, center, r, (0, 0), thickness=-1)

# Aplicar o filtro
fshift = dft_shift * mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

# Normalizar e salvar a imagem
cv2.normalize(img_back, img_back, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('imagem_sem_reflexo.png', img_back)
