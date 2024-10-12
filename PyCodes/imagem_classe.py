import cv2 as cv
from utils import check_wifi
import os
import time
from CAMERA_IPS import CAMERA01, CAMERA02

class Imagem:
    def __init__(self, endereco:str) -> None:
        try:
            self.endereco = endereco
            cv.imread(self.endereco)
        except Exception as e:
            print("Endereço vazio.")
        self.tamanho = cv.imread(self.endereco).shape
    
    def set_endereco(self, novo_endereco:str) -> None:
        self.endereco = novo_endereco
        try:
            cv.imread(novo_endereco)
        except Exception as e:
            print("Endereço invalido.")
    
    @property
    def get_endereco(self) -> str:
        return self.endereco
    
    def getImage(self) -> cv.typing.MatLike:
        return cv.imread(self.endereco)
    
    def remove_distorcao(self, cameraMatrix, dist) -> cv.typing.MatLike:
        h, w = self.tamanho[:2]
        
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))
        
        imagem_sem_distorcao = cv.undistort(self.getImage(), cameraMatrix, dist, None, newCameraMatrix)
        
        x, y, w, h = roi
        
        if roi[2] > 0 and roi[3] > 0:
            dst = dst[y:y+h, x:x+w]
        else: print("ROI invalida, sera usada a imagem completa.")
        
        return imagem_sem_distorcao
    
    def suavizar_imagem(self, alpha) -> cv.typing.MatLike:
        return cv.GaussianBlur(self.getImage(), (5, 5), alpha)
    
    def equalizar_imagem(self) -> cv.typing.MatLike:
        canal_b, canal_g, canal_r = cv.split(self.getImage())

        equalizado_b = cv.equalizeHist(canal_b)
        equalizado_g = cv.equalizeHist(canal_g)
        equalizado_r = cv.equalizeHist(canal_r)

        img_equalizada_colorida = cv.merge([equalizado_b, equalizado_g, equalizado_r])

        return img_equalizada_colorida