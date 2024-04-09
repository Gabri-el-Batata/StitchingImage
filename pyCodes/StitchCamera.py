import cv2 as cv
import numpy as np
from glob import glob
import pickle
import imutils

def undistortImage(img, adress: str):
    h, w = img.shape[:2]
    
    cameraMatrix = pickle.load(open(str(adress) + "cameraMatrix.pkl", "rb"))
    dist = pickle.load(open(str(adress) + "dist.pkl", "rb"))
    
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    # Retirando distorsao
    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # Cortar a imagem (Apos retirar distorsao a imagem muda de tamanho)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def image_stitch(imagePath:str):
    imagePath = glob(imagePath)
    images = [cv.imread(img) for img in imagePath]

    imageStitcher = cv.Stitcher.create()

    error, panorama = imageStitcher.stitch(images)

    if error == cv.Stitcher_OK:
        cv.imshow('Panorama', panorama)
        cv.waitKey(0)
    else:
        print(error)
        print("Error")

def afterPanorama(panorama):
    panorama = cv.copyMakeBorder(panorama, 10, 10, 10, 10, cv.BORDER_CONSTANT, (0, 0, 0))
    gray = cv.cvtColor(panorama, cv.COLOR_BGR2GRAY)
    thresh_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]

    cv.imshow('', thresh_img)
    cv.waitKey(0)

    contours = cv.findContours(thresh_img.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv.contourArea)
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv.boundingRect(areaOI)
    cv.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
    minRectangle = mask.copy()
    sub = mask.copy()
    while cv.countNonZero(sub) > 0:
        minRectangle = cv.erode(minRectangle, None)
        sub = cv.subtract(minRectangle, thresh_img)
    contours = cv.findContours(minRectangle.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv.contourArea)

    cv.imshow('', minRectangle)
    cv.waitKey(0)

    x, y, w, h = cv.boundingRect(areaOI)
    print(cv.boundingRect(areaOI))
    
    panorama = panorama[y:y+h, x:x+w]
    cv.imshow('', panorama)
    cv.waitKey(0)
    

# Abrindo o caminho das imagens
imagePath = 'C:/Users/gabri/Documents/Projetos/fotos/*.png'

image_stitch(imagePath)
