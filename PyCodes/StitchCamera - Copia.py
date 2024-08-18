import cv2 as cv
import numpy as np

from utils import stitch_images

# Desativar o uso do OpenCL
cv.ocl.setUseOpenCL(False)

# Caminhos para as imagens
image_path1 = "C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera1.png"
image_path2 = "C:/Users/gabri/Documents/Camera_Batata/equalized_caliResult_Camera2.png"

# Mesclar as imagens
stitch_images(image_path1, image_path2)
