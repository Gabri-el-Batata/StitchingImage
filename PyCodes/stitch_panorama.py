import cv2
import numpy as np
from matplotlib import pyplot as plt

def warp_image(img, src_points, dst_points):
    h, w = img.shape[:2]
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped

def find_sift_matches(img1, img2):
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = matcher.match(descriptors1, descriptors2)

    matches = sorted(matches, key=lambda x: x.distance)
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    return points1, points2

def stitch_images_with_blending(img1, img2):
    points1, points2 = find_sift_matches(img1, img2)
    H, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

    height, width = img1.shape[:2]
    result = cv2.warpPerspective(img2, H, (width * 2, height))
    
    blend_width = 50  # Width of the blending area
    for i in range(blend_width):
        alpha = i / blend_width
        result[:, width - blend_width + i] = alpha * img1[:, width - blend_width + i] + (1 - alpha) * result[:, width - blend_width + i]

    result[0:height, 0:width] = img1

    return result

# Carrega as imagens
img1_path = 'equalized_caliResult_Camera1.png'
img2_path = 'equalized_caliResult_Camera2.png'

img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path)

# Visualizar pontos importantes para ajuste manual
def display_image_with_points(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Click to select points')
    points = plt.ginput(4, timeout=-1)  # Permitir ao usuário clicar para selecionar pontos
    plt.close()
    return np.float32(points)

print("Select 4 points on the first image")
src_points1 = display_image_with_points(img1)
print("Select the corresponding 4 points on the second image")
src_points2 = display_image_with_points(img2)

# Ajusta a perspectiva das imagens
dst_points1 = np.float32([[0, 0], [img1.shape[1] - 1, 0], [0, img1.shape[0] - 1], [img1.shape[1] - 1, img1.shape[0] - 1]])
warped_img1 = warp_image(img1, src_points1, dst_points1)
warped_img2 = warp_image(img2, src_points2, dst_points1)  # Usar os mesmos pontos de destino para alinhar ambas as imagens

# Mescla as imagens ajustadas
result = stitch_images_with_blending(warped_img1, warped_img2)

# Exibe o resultado
plt.figure(figsize=(20,10))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Stitched Image with Perspective Adjustment')
plt.axis('off')
plt.show()

# Salva o resultado
cv2.imwrite('stitched_image.png', result)
