import cv2 as cv
import numpy as np

# Desativar o uso do OpenCL
cv.ocl.setUseOpenCL(False)

def stitch_images(image_path1, image_path2):
    # Carregar as imagens
    img1 = cv.imread(image_path1)
    img2 = cv.imread(image_path2)

    if img1 is None or img2 is None:
        print("Erro ao carregar as imagens.")
        return

    # Criar o objeto stitcher
    stitcher = cv.Stitcher.create(mode=cv.STITCHER_PANORAMA)
    
    # Tentar mesclar as imagens
    status, stitched_image = stitcher.stitch([img1, img2])

    if status == cv.Stitcher_OK:
        print("Imagens mescladas com sucesso.")
        cv.imwrite('imagem_mesclada.png', stitched_image)
    else:
        print("Erro ao mesclar as imagens.")
        print(f"Código de retorno: {status}")

# Caminhos para as imagens
image_path2 = "C:/Users/Server/Documents/Camera_Batata/img0_Camera1.png"
image_path1 = "C:/Users/Server/Documents/Camera_Batata/img0_Camera2.png"

# Mesclar as imagens
stitch_images(image_path1, image_path2)
