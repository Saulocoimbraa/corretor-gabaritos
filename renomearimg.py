import os
import random
import string
import shutil

# === 1. Perguntar o nome da escola ===
nome_escola = input("Digite o nome da escola: ").strip().replace(" ", "_")

# === 2. Caminho das imagens originais e da pasta destino ===
pasta_origem = "imagens_recebidas"
pasta_destino = "imagens_renomeadas"
os.makedirs(pasta_destino, exist_ok=True)

# === 3. Função para gerar ID aleatório ===
def gerar_id(tamanho=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=tamanho))

# === 4. Renomear imagens ===
contador = 1
for arquivo in os.listdir(pasta_origem):
    if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
        id_aluno = gerar_id()
        novo_nome = f"{nome_escola}-{id_aluno}.png"
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, novo_nome)
        shutil.copy2(caminho_origem, caminho_destino)
        print(f"✅ {arquivo} → {novo_nome}")
        contador += 1

print(f"\n🎉 {contador-1} imagens renomeadas e salvas em '{pasta_destino}'")
