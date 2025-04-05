import cv2
import os

# Caminho da imagem salva anteriormente
pasta_imagens = 'imagens_recebidas'
arquivos = os.listdir(pasta_imagens)

if not arquivos:
    print("Nenhuma imagem encontrada na pasta.")
else:
    imagem_path = os.path.join(pasta_imagens, arquivos[0])

    # Carrega a imagem com OpenCV
    imagem = cv2.imread(imagem_path)

    # Mostra a imagem em uma janela
    cv2.imshow("Imagem recebida", imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
