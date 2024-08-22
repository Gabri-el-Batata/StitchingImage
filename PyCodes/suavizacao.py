import cv2
import numpy as np

# Carregar a imagem concatenada
imagem = cv2.imread('/home/ml1/Documents/Camera_Batata/StitchingImage/panoramas/panorama_aruco.png')

# Definir a região da marca de sobreposição (exemplo: [x_inicio, x_fim, y_inicio, y_fim])
# Ajuste esses valores com base na localização da marca
x_inicio, x_fim = 945, 985
y_inicio, y_fim = 0, imagem.shape[0]

# Recortar a região da marca de sobreposição
regiao_marca = imagem[y_inicio:y_fim, x_inicio:x_fim]

# Aplicar uma suavização para tentar remover a marca
# Neste caso, estamos usando um filtro Gaussiano, mas você pode experimentar outros filtros
imagem_suavizada = cv2.GaussianBlur(regiao_marca, (5, 5), 0)

# Substituir a região da marca na imagem original
imagem[y_inicio:y_fim, x_inicio:x_fim] = imagem_suavizada

# Salvar ou exibir a imagem resultante
cv2.imshow('Imagem Suavizada', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
