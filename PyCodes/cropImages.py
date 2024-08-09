import cv2 as cv

img = cv.imread('caliResult_Camera2.png')
img = img[80:400, :]


cv.imshow("", img)
cv.waitKey()

cv.imwrite('caliResult_cropCamera2.png', img)