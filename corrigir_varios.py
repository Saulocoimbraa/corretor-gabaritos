import cv2
import numpy as np
import pandas as pd
import os

# === 1. Ler gabarito ===
with open("gabarito.txt", "r") as arquivo:
    gabarito = [linha.strip().upper() for linha in arquivo.readlines()]

# === 2. Função para corrigir uma imagem ===
def corrigir_imagem(caminho_imagem, nome_aluno):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print(f"❌ Erro ao abrir imagem: {caminho_imagem}")
        return None

    imagem = cv2.resize(imagem, (600, 800))
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(cinza, (5, 5), 0)
    _, binarizada = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contornos, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bolhas = []
    for c in contornos:
        area = cv2.contourArea(c)
        (x, y, w, h) = cv2.boundingRect(c)
        aspecto = w / float(h)
        if 0.5 <= aspecto <= 1.5 and 800 < area < 6000:
            bolhas.append((x, y, w, h))

    bolhas = ordenar_por_linhas(bolhas)

    respostas = []
    for i in range(0, len(bolhas), 5):
        grupo = bolhas[i:i+5]
        preenchimentos = []
        for (x, y, w, h) in grupo:
            roi = binarizada[y:y+h, x:x+w]
            preenchido = cv2.countNonZero(roi) / (w * h)
            preenchimentos.append(preenchido)

        indice_marcado = np.argmax(preenchimentos)
        alternativa = ["A", "B", "C", "D", "E"][indice_marcado]
        respostas.append(alternativa)

    acertos = sum([1 for r, g in zip(respostas, gabarito) if r == g])
    nota_percentual = round((acertos / len(gabarito)) * 100)

    dados = {
        "Aluno": nome_aluno,
        **{f"Q{i+1}": resp for i, resp in enumerate(respostas)},
        "Acertos": acertos,
        "Nota (%)": nota_percentual
    }
    return dados

# === 3. Ordenar bolhas por linha ===
def ordenar_por_linhas(bolhas, colunas_por_linha=5):
    linhas_agrupadas = []
    bolhas = sorted(bolhas, key=lambda b: b[1])
    for i in range(0, len(bolhas), colunas_por_linha):
        linha = sorted(bolhas[i:i+colunas_por_linha], key=lambda b: b[0])
        linhas_agrupadas.extend(linha)
    return linhas_agrupadas

# === 4. Processar todas as imagens ===
pasta_imagens = "imagens_recebidas"
resultados = []

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
        caminho = os.path.join(pasta_imagens, nome_arquivo)
        nome_aluno = os.path.splitext(nome_arquivo)[0]
        print(f"📄 Corrigindo: {nome_aluno}")
        dados = corrigir_imagem(caminho, nome_aluno)
        if dados:
            resultados.append(dados)

# === 5. Salvar resultados no Excel ===
if resultados:
    df = pd.DataFrame(resultados)
    df.to_excel("resultados_gerais.xlsx", index=False)
    print("✅ Todos os resultados foram salvos em 'resultados_gerais.xlsx'")
else:
    print("⚠️ Nenhum resultado foi gerado.")
