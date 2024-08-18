import cv2 as cv
from matplotlib import pyplot as plt
import subprocess

def plotar_duas_imagens(img1:cv.typing.MatLike, img2:cv.typing.MatLike) -> None:
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
