import cv2 as cv
from glob import glob
import pickle

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



# Abrindo o caminho das imagens
imagePath = glob('*.png')
images = []
#
# Colocando todas as imagens em uma lista
for i, image in enumerate(imagePath):
    img = cv.imread(image)
    #img = undistortImage(img, 'C:/Users/Adquiri/Documents/Camera_Batata/calib2301/')

    # Importante dizer que esse processo de recorte e para ver o limite que se pode afastar as cameras
    #if i == 0:
    #    h, w = img.shape[:2]
    #    img1 = img[:, :int(0.6*w)]
    #    img2 = img[:, int(0.3*w):]
    #    images.append(img1)
    #    images.append(img2)
    #else:
    #    images.append(img)
    
    images.append(img)


imageStitcher = cv.Stitcher.create()

error, result = imageStitcher.stitch(images)

if error == cv.Stitcher_OK:
    cv.imwrite('StitchImage.png', result)
    cv.imshow('', result) # Mostrando imagem da camera esquerda
    cv.waitKey(0)
else:
    print(error)
    print("Error")
