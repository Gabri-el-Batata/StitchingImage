import subprocess as sp
import os

diretorioAtual = os.path.dirname(os.path.abspath(__file__))
# diretorioAtual = diretorioAtual.replace("//", "//", -1)
print("Diretorio atual: ", diretorioAtual)

codigoCpp = "C:/Users/Server/Documents/CameraC/build/Debug/CameraC.exe" 

IMG1 = "C:/Users/Server/Documents/Camera_Batata/img0_Camera1.png"
IMG2 = "C:/Users/Server/Documents/Camera_Batata/img0_Camera2.png"
# IMAGEM1 = "C:/Users/Server/Documents/Camera_Batata/esquerdaCorrigida.jpeg"
# IMAGEM2 = "C:/Users/Server/Documents/Camera_Batata/direitaCorrigida.jpeg"

argumentos = [IMG1, IMG2, diretorioAtual]

processo = sp.Popen([codigoCpp]+argumentos, stdout=sp.PIPE, stderr=sp.PIPE)

saida, erro = processo.communicate()

print("SAIDA: ", saida.decode("utf-8"))

if erro:
    print("ERRO: ", erro.decode("utf-8"))

codigoRetorno = processo.returncode

print("CODIGO RETORNO: ", codigoRetorno)