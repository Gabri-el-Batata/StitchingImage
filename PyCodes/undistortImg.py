import cv2 as cv
import pickle
import os
from matplotlib import pyplot as plt

current_directory = os.getcwd().replace('\\', '/')

choice_camera = str(input("Qual câmera você vai acessar?: [1/2]\n")).strip()

cameraMatrix = f'/calibracao_camera1/cameraMatrix.pkl'
dist = f'/calibracao_camera1/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

print("Diretório para cameraMatrix: ", cameraMatrix_path)
print("Diretório para dist: ", dist_path)

choice = str(input("Esta correto?: [S/n]\n")).strip().upper()

if choice == "N":
    exit()

try:
    with open(cameraMatrix_path, 'rb') as f1:
        data1 = pickle.load(f1)
        print(f"Dados do arquivo {cameraMatrix} carregados com sucesso.")
except FileNotFoundError:
    print(f"Erro: O arquivo {cameraMatrix} não foi encontrado.")
except pickle.UnpicklingError:
    print(f"Erro: Não foi possível desserializar o conteúdo de {cameraMatrix}.")

try:
    with open(dist_path, 'rb') as f2:
        data2 = pickle.load(f2)
        print(f"Dados do arquivo {dist} carregados com sucesso.")
except FileNotFoundError:
    print(f"Erro: O arquivo {dist} não foi encontrado.")
except pickle.UnpicklingError:
    print(f"Erro: Não foi possível desserializar o conteúdo de {dist}.")

############## UNDISTORTION #####################################################

img = cv.imread(current_directory + f'/img0_Camera{choice_camera}.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(data1, data2, (w,h), 1, (w,h))

# Undistort
dst = cv.undistort(img, data1, data2, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title(f'Imagem com distorção. {img.shape[:2]}')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv.cvtColor(dst, cv.COLOR_BGR2RGB))
plt.title(f'Imagem sem distorção. {dst.shape[:2]}')
plt.axis('off')

plt.show()

salvar_imagem = str(input("Gostaria se salvar a imagem sem distorção?: [s/N]\n")).strip().upper()

if not(salvar_imagem == "N" or salvar_imagem == ""):
    cv.imwrite(f'caliResult_Camera{choice_camera}.png', dst)
else:
    exit()