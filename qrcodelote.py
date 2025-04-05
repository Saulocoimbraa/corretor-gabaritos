import qrcode
import json
import os
from PIL import Image, ImageDraw, ImageFont

# === Lista de escolas e turmas ===
escolas_e_turmas = [
    ("Escola Alpha", "1A"),
    ("Escola Beta", "2B"),
    ("Escola Gama", "3C"),
]

# === Fonte para o texto ===
try:
    fonte = ImageFont.truetype("arial.ttf", 24)
except:
    fonte = ImageFont.load_default()

# === Criar a pasta de saída ===
os.makedirs("qrcodes_com_texto", exist_ok=True)

for escola, turma in escolas_e_turmas:
    dados = {
        "escola": escola,
        "turma": turma
    }

    conteudo = json.dumps(dados)
    nome_arquivo = f"{escola}_{turma}.png".replace(" ", "_")

    # Gera o QR Code e converte para RGB
    qr_img = qrcode.make(conteudo)
    qr_img = qr_img.convert("RGB")

    # Dimensões do QR
    largura, altura = qr_img.size

    # Criar imagem com espaço extra para o texto
    altura_total = altura + 60
    imagem_final = Image.new("RGB", (largura, altura_total), "white")
    imagem_final.paste(qr_img, (0, 0))  # Colar QR no topo

    # Escrever o texto abaixo
    draw = ImageDraw.Draw(imagem_final)
    texto = f"{escola} - Turma {turma}"

    # Usar textbbox para calcular posição do texto
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    text_largura = bbox[2] - bbox[0]
    pos_texto = ((largura - text_largura) // 2, altura + 10)
    draw.text(pos_texto, texto, font=fonte, fill="black")

    # Salvar imagem
    caminho = os.path.join("qrcodes_com_texto", nome_arquivo)
    imagem_final.save(caminho)
    print(f"✅ QR com texto salvo: {caminho}")
