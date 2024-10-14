import cv2 as cv
from utils import check_wifi
import os
import time
from CAMERA_IPS import CAMERA01, CAMERA02

WIFI_NAME = "CompVisio"

def save_image(num, img) -> None:
    filename = f'img{num}_Camera.png'
    cv.imwrite(filename, img)
    print("Imagem Salva: ", filename)

def clear_buffer_one(capture, frames_to_clear=5) -> None:
    for _ in range(frames_to_clear):
        capture.grab()

def init_capture(capture, buffer_size:int, fps:int) -> None:
    capture.set(cv.CAP_PROP_BUFFERSIZE, buffer_size)
    capture.set(cv.CAP_PROP_FPS, fps)
    capture.set(cv.CAP_PROP_OPEN_TIMEOUT_MSEC, 50000)  # Timeout para abertura do stream
    capture.set(cv.CAP_PROP_READ_TIMEOUT_MSEC, 50000) 

class Wifi:
    def __init__(self, wifi_name: str) -> None:
        self.name = wifi_name
    
    def verify_wifi(self) -> None:
        '''
        Verificar se o usuario esta conectado no wifi correto.
        '''
        if check_wifi(self.name) == False:
            print("Você não esta conectado no Wi-Fi correto. Por favor, conecte no Wi-Fi: ", WIFI_NAME)
            exit()
        print("Voce esta conectado no Wi-Fi correto.")

class Camera:
    def __init__(self, fps: int, ip:str, buffer_size:int, limite_frames:int=30) -> None:
        self.fps = fps
        self.ip = ip
        self.buffer_size = buffer_size
        self.address = f'rtsp://admin:cepetro1234@{self.ip}?tcp&fps={self.fps}'
        self.limite_frames = limite_frames
        
    
    def ping_camera(self) -> None:
        response = os.system(f"ping -c 1 {self.ip}")
        if response == 0:
            print(f"{self.ip} is reachable.")
            return True
        else:
            print(f"{self.ip} is not reachable.")
            return False
    
    def set_fps(self, new_fps:int) -> None:
        self.fps = new_fps
        
    @property
    def get_fps(self) -> int:
        return self.fps
    
    def set_buffer_size(self, new_buffer_size:int) -> None:
        self.buffer_size = new_buffer_size
    
    @property
    def get_buffer_size(self) -> int:
        return self.buffer_size  
    
    def getFrame(self) -> None:
        cap = cv.VideoCapture(self.address, cv.CAP_FFMPEG)
        
        init_capture(cap, 3, 1)
        
        if not cap.isOpened():
            print("Erro ao conectar ao fluxo RTSP. Verifique se as câmeras estão ligadas.")
            exit()
        
        num = int(input("Digite o número da foto:\n"))    
        
        for i in range(2, -1, -1):
            print(f"Começando a filmagem em {i+1} segundos...")
            time.sleep(1)
        
        print("\nCâmera pronta para tirar fotos.\n")
        
        frames = 0
        
        while cap.isOpened():
            ret, img = cap.read()
        
            if not ret:
                #print("Frame corrompido, continuando o processamento.")
                # print("Erro ao conectar ao fluxo RTSP. Tentando reconectar...")
                # cap.release()
                # cap = self.init_capture()
                # cap.grab()
                # time.sleep(1)
                print("A camera nao esta respondendo.")
                break
            
            if frames % 10 == 0:
                cv.imshow("Frame", img)
            
            k = cv.waitKey(10)
            
            if k == 27:
                break
            
            elif k == ord('s'):
                save_image(num, img)
                num += 1
            
            elif frames >= self.limite_frames:
                clear_buffer_one(cap)
                frames = 0
            
            frames += 1
            
        cap.release()
        cv.destroyAllWindows()
        
# wifi = Wifi(WIFI_NAME)

# wifi.verify_wifi()

# Camera1 = Camera(1, CAMERA01, 3)

# Camera1.getFrame()