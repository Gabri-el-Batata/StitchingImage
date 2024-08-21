import cv2 as cv
from matplotlib import pyplot as plt
import subprocess

#### Constantes

ARUCO_DICT = {
  "DICT_4X4_50": cv.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv.aruco.DICT_ARUCO_ORIGINAL
}

def plotar_duas_imagens(img1, img2) -> None:
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 2, 1)
    plt.imshow(cv.cvtColor(img1, cv.COLOR_BGR2RGB))
    plt.title('Imagem 1')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv.cvtColor(img2, cv.COLOR_BGR2RGB))
    plt.title('Imagem 2')
    plt.axis('off')

    plt.show()

def equalizar_imagem_colorida(img):
    '''
    Metodo utilizado. Separar os canais de cores da imagem base, equalizar cada um e depois mesclar esses canais na imagem base.
    '''
    canal_b, canal_g, canal_r = cv.split(img)

    equalizado_b = cv.equalizeHist(canal_b)
    equalizado_g = cv.equalizeHist(canal_g)
    equalizado_r = cv.equalizeHist(canal_r)

    img_equalizada_colorida = cv.merge([equalizado_b, equalizado_g, equalizado_r])

    return img_equalizada_colorida

def equalizar_imagem(img):
    '''
    Essa funcao vai equalizar a imagem convertendo de BGR para YCrCb (canal de luz e cromancia)
    e equalizar o canal de luz
    '''
    imagem_ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)

    imagem_ycrcb[:, :, 0] = cv.equalizeHist(imagem_ycrcb[:, :, 0])

    imagem_equalizada_colorida = cv.cvtColor(imagem_ycrcb, cv.COLOR_YCrCb2BGR)

    return imagem_equalizada_colorida

def equalizar_imagens_normal(img):
    '''
    Metodo tradicional de equalizar a image, mas a deixa cinza.
    '''
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    equalized = cv.equalizeHist(gray)

    equalized_img = cv.cvtColor(equalized, cv.COLOR_GRAY2BGR)
    
    return equalized_img

def check_wifi(WIFI_NAME:str):

    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])

    if WIFI_NAME in str(wifi):
        return True
    else:
        return False
    
def remover_distorcao(img, cameraMatrix, dist):
    h, w = img.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    # Undistort
    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    if roi[2] > 0 and roi[3] > 0:
        dst = dst[y:y+h, x:x+w]
    else: print("ROI invalida, sera usada a imagem completa.")

    return dst

def ReadCamera(ip:str) -> None:
    adress = 'rtsp://admin:cepetro1234@' + ip
    cap = cv.VideoCapture(adress, cv.CAP_FFMPEG)

    # Defina um buffer de captura (se aplicável)
    cap.set(cv.CAP_PROP_BUFFERSIZE, 3)

    while (cap.isOpened()):
        ret, img = cap.read() # Lendo

        img = cv.GaussianBlur(img, (5, 5), 0)

        if not ret: break
        cv.imshow('RTSP Frame', img)
        if cv.waitKey(1) & 0xFF == ord('q'): # Pressione 'q' para parar o programa
            break
      
   # Apos fechar o video, todas as janelas sao destruidas e a variavel reiniciada
    cap.release()
    cv.destroyAllWindows()

def stitch_images(image_path1, image_path2):
    # Carregar as imagens
    img1 = cv.imread(image_path1)
    img2 = cv.imread(image_path2)

    if img1 is None or img2 is None:
        print("Erro ao carregar as imagens.")
        return

    # Criar o objeto stitcher
    stitcher = cv.Stitcher.create(mode=cv.STITCHER_PANORAMA)

    stitcher.setWaveCorrection(False)
    
    # Tentar mesclar as imagens
    status, stitched_image = stitcher.stitch([img2, img1])

    if status == cv.Stitcher_OK:
        print("Imagens mescladas com sucesso.")
        cv.imshow('imagem_mesclada.png', stitched_image)
        cv.waitKey(0)
        cv.imwrite('imagem_mesclada.png', stitched_image)
    else:
        print("Erro ao mesclar as imagens.")
        print(f"Código de retorno: {status}")

    cv.destroyAllWindows()


def detect_markers(image, desired_aruco_dictionary: str) -> None:
  
  this_aruco_dict = cv.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
  this_aruco_parameters = cv.aruco.DetectorParameters_create()

  (corners, ids, _) = cv.aruco.detectMarkers(image, this_aruco_dict, parameters=this_aruco_parameters)

  if len(corners) > 0:
    # Flatten the ArUco IDs list
    ids = ids.flatten()

    # Loop over the detected ArUco corners
    for (marker_corner, marker_id) in zip(corners, ids):
    
      # Extract the marker corners
      corners = marker_corner.reshape((4, 2))
      (top_left, top_right, bottom_right, bottom_left) = corners

      # Convert the (x,y) coordinate pairs to integers
      top_right = (int(top_right[0]), int(top_right[1]))
      bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
      bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
      top_left = (int(top_left[0]), int(top_left[1]))

      # Draw the bounding box of the ArUco detection
      cv.line(image, top_left, top_right, (0, 255, 0), 2)
      cv.line(image, top_right, bottom_right, (0, 255, 0), 2)
      cv.line(image, bottom_right, bottom_left, (0, 255, 0), 2)
      cv.line(image, bottom_left, top_left, (0, 255, 0), 2)

      # Calculate and draw the center of the ArUco marker
      center_x = int((top_left[0] + bottom_right[0]) / 2.0)
      center_y = int((top_left[1] + bottom_right[1]) / 2.0)
      cv.circle(image, (center_x, center_y), 4, (0, 0, 255), -1)

      # Draw the ArUco marker ID on the video image1
      # The ID is always located at the top_left of the ArUco marker
      cv.putText(image, str(marker_id), 
        (top_left[0], top_left[1] - 15),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)

      # Display the resulting image1
  cv.imshow('Imagem com ArUco detectado',image)
  cv.waitKey(0)