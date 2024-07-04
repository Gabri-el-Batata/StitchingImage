import cv2 as cv
from glob import glob

# Abrindo o caminho das imagens
imagePath = glob('C:/Users/Server/Documents/Camera_Batata/pictures/*.png')
images = []

# Colocando todas as imagens em uma lista
for image in imagePath:
    img = cv.imread(image)
    h, w = img.shape[:2]
    img1 = img[:, :int(0.6*int(w))]
    img2 = img[:, int(0.3*int(w)):int(0.9*int(w))]
    img3 = img[:, int(0.6*int(w)):]
    images.append(img1)
    images.append(img2)
    images.append(img3)

print(len(images))
for img in images:
    cv.imshow('', img)
    cv.waitKey(0)
    
imageStitcher = cv.Stitcher.create()

error, result = imageStitcher.stitch(images[:])

if not error:
    cv.imwrite('StitchImage.png', result)
    cv.imshow('', result) # Mostrando imagem da camera esquerda
    cv.waitKey(0)
else:
    print(error)
    print("Error")