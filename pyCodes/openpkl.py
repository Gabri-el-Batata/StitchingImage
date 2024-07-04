import cv2 as cv
import pickle
import os

current_directory = os.getcwd().replace('\\', '/')


cameraMatrix = '/cameraMatrix.pkl'
dist = '/dist.pkl'

cameraMatrix_path = current_directory + cameraMatrix
dist_path = current_directory + dist

try:
    with open(cameraMatrix_path, 'rb') as f1:
        data1 = pickle.load(f1)
        print(f"Dados do arquivo {cameraMatrix} carregados com sucesso.")
        print(data1)
except FileNotFoundError:
    print(f"Erro: O arquivo {cameraMatrix} não foi encontrado.")
except pickle.UnpicklingError:
    print(f"Erro: Não foi possível desserializar o conteúdo de {cameraMatrix}.")

try:
    with open(dist_path, 'rb') as f2:
        data2 = pickle.load(f2)
        print(f"Dados do arquivo {dist} carregados com sucesso.")
        print(data2)
except FileNotFoundError:
    print(f"Erro: O arquivo {dist} não foi encontrado.")
except pickle.UnpicklingError:
    print(f"Erro: Não foi possível desserializar o conteúdo de {dist}.")