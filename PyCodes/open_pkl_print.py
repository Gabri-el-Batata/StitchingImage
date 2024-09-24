import pickle as pkl

caminho = "calibracao_camera1\dist.pkl".replace('\\', '/')

caminho = str(caminho)

with open(caminho, 'rb') as f:
    dados = pkl.load(f)
print(dados)