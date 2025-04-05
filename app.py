from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'static/imagens_recebidas'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return 'Nenhum arquivo enviado.'

    imagem = request.files['imagem']
    escola = request.form.get('escola')

    if imagem.filename == '':
        return 'Nenhum arquivo selecionado.'

    if imagem:
        from uuid import uuid4
        id_aluno = str(uuid4())[:8]
        nome_arquivo = f"{escola}_{id_aluno}.png"
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(nome_arquivo))
        imagem.save(caminho)

        # Chamar script de correção (opcional aqui)
        subprocess.run(['python', 'corrigir_gabaritos.py'])

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
