import cv2 as cv
import imutils
import numpy as np

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
    while cv.countNonZero(sub) > 450:
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
    cv.imwrite('panoramaCorrigido.png', panorama)
    cv.imshow('', panorama)
    cv.waitKey(0)
    
img = cv.imread('imagemCombinada.jpeg')

afterPanorama(img)