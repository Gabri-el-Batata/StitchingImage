import cv2 as cv
import pickle
import os

current_directory = os.getcwd().replace('\\', '/')


cameraMatrix = '/calibracao_camera2/cameraMatrix.pkl'
dist = '/calibracao_camera2/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

print("Diretório para cameraMatrix: ", cameraMatrix_path)
print("Diretório para dist: ", dist_path)

choice = str(input("Esta correto?: [S/N]\n")).strip().upper()

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

img = cv.imread(current_directory + '/img0_Camera2.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(data1, data2, (w,h), 1, (w,h))


# Undistort
dst = cv.undistort(img, data1, data2, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('caliResult_Camera2.png', dst)