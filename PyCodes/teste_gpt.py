import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def show_image(title, img, figsize=(10, 7)):
    """Função para exibir imagens em etapas."""
    plt.figure(figsize=figsize)
    if len(img.shape) == 2:  # Grayscale image
        plt.imshow(img, cmap='gray')
    else:  # RGB image
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

# Carregar as imagens
img1 = cv.imread('equalized_caliResult_Camera1.png')
img2 = cv.imread('equalized_caliResult_Camera2.png')


# Detectar keypoints e descritores usando ORB
orb = cv.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Exibir keypoints
img1_kp = cv.drawKeypoints(img1, kp1, None, color=(0,255,0))
img2_kp = cv.drawKeypoints(img2, kp2, None, color=(0,255,0))

# show_image("Keypoints na Imagem 1", img1_kp)
# show_image("Keypoints na Imagem 2", img2_kp)

# Fazer correspondência dos keypoints usando BFMatcher
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

# Exibir correspondências
img_matches = cv.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# show_image("Correspondências entre as imagens", img_matches)

# Encontrar a matriz homográfica
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

# Fazer a transformação da perspectiva (warp) na primeira imagem
h, w, _ = img2.shape
img1_warped = cv.warpPerspective(img1, M, (w, h))

# Exibir a imagem transformada
show_image("Imagem 1 - Transformada pela homografia", img1_warped)
cv.imwrite("Camera1_transformada.png", img1_warped)


# stitcher = cv.Stitcher.create(mode=cv.Stitcher_PANORAMA)

# status, pano = stitcher.stitch([img1, img2])

# if status == cv.Stitcher_OK:
#     cv.imshow('Imagem mesclada', pano)
#     cv.waitKey(0)
# else:
#     print("Criação do panorama não deu certo.")

# Criar uma imagem final (panorama)
panorama = cv.addWeighted(img1_warped, 0.5, img2, 0.5, 0)

# Exibir o resultado final
show_image("Panorama Final", panorama)

# Salvar o panorama
cv.imwrite('panorama_final.png', panorama)
