# Objetivo da programação
O objetivo da programação é, em geral, capturar duas imagens  (a principio), atenuar as distorções apresentadas e aplicar o algoritmo de mesclagem.

# Links uteis
Image stitching using SIFT keypoint descriptor and homography matrix (https://codereview.stackexchange.com/questions/285153/image-stitching-using-sift-keypoint-descriptor-and-homography-matrix)

Stitching tutorial with OpenCV (https://github.com/whdlgp/Stitching-tutorial-with-OpenCV/blob/master/README.md)

Blog Open Pano (https://ppwwyyxx.com/blog/2016/How-to-Write-a-Panorama-Stitcher/)

# Imagens
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/main/esquerdaCorrigida.jpeg" alt="Foto esquerda">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/main/direitaCorrigida.jpeg" alt="Foto direita">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/main/result.jpg" alt="Panorama">


Outras refêrencias que podem ser utéis na avaliação da incluência na redução da região de sobreposição entre imagens.

https://docs.opencv.org/4.x/d8/d19/tutorial_stitcher.html

https://docs.opencv.org/4.x/d2/d8d/classcv_1_1Stitcher.html#a114713924ec05a0309f4df7e918c0324

# Segundo semestre de 2024

O objetivo é explorar a redução da região de sobreposição e avlaiar a influência desse ato na criação do panorama

- Fotos com distorção
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/img0_Camera1.png" alt = "Foto da câmera de cima">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/img0_Camera2.png" alt = "Foto da câmera de baixo">

- Fotos sem distorção
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/caliResult_Camera1.png" alt = "Foto da câmera de cima sem distorção">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/caliResult_Camera2.png" alt = "Foto da câmera de cima sem distorção">

Por meio de algumas observações, percebeu-se que era necessário realizar uma equalização nas imagens, pois havia certa variação de iluminação entre as duas imagens, tornando o processo de detecção de correspondencia entre as imagens dificil.

- Imagens equalizadas
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/equalized_caliResult_Camera1.png" alt = "Foto da câmera de cima sem distorção equalizada">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/equalized_caliResult_Camera2.png" alt = "Foto da câmera de cima sem distorção equalizada">

# Panoramas criados
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/panoramas/imagem_mesclada.png" alt = "Panorama 1">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/panoramas/result.png" alt = "Panorama 2">
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/panoramas/result_plano.png" alt = "Panorama 3">

Panorama 1 -> Esse panorama foi criado usando a função Stitch do opencv, o código do python com a modificação de que a classe foi criada como STITCHER_SCANS.
Panorama 2 -> Esse panorama foi criado usando a função Stitch do opencv, o código do python padrão.
Panorama 3 -> Esse panorama foi criado usando a função Stitch do opencv, com a condição de que esse panorama foi distorcido ao redor de uma região plana.

# Panorama criado manualmente
<img src="https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/panoramas/panorama_aruco.png" alt = "Panorama feito manualmente com rastreamento do aruco">

# Panorama final com o blur na região de sobreposição
<img src="=https://github.com/Gabri-el-Batata/StitchingImage/blob/batata_dev/panorama_aruco_blur.png" alt = "Panorama feito manualmente com rastreamento do aruco e com blur">



