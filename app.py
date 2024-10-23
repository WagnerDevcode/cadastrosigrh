from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

# Dicionário para armazenar os registros
codigo_registro = {}

# Cria a pasta 'date' se ela não existir
if not os.path.exists("date"):
    os.makedirs("date")

# Define o caminho do arquivo CSV único
csv_file = os.path.join("date", "codigo_registro.csv")


# Função para carregar os registros existentes do CSV no dicionário
def load_registro():
    global codigo_registro
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        codigo_registro = dict(zip(df["Description"], df["Code"]))


# Função para salvar os registros no arquivo CSV
def save_registro():
    df = pd.DataFrame(list(codigo_registro.items()), columns=["Description", "Code"])
    df.to_csv(csv_file, index=False)


# Carrega os registros ao iniciar o servidor
load_registro()


# Rota para exibir a página inicial
@app.route("/")
def index():
    return render_template("index.html")


# Rota para registrar códigos e atualizar o arquivo CSV na pasta 'date'
@app.route("/register", methods=["POST"])
def register_code():
    data = request.json
    code = data.get("code")
    description = data.get("description")

    if not code or not description:
        return jsonify({"message": "Both code and description are required."}), 400

    if description in codigo_registro:
        return jsonify(
            {
                "message": f" A descrição  '{description}' já existe para o codigo: {codigo_registro[description]}."
            }
        ), 400
    else:
        # Registra o código no dicionário
        codigo_registro[description] = code

        # Salva ou atualiza o arquivo CSV
        save_registro()

        return jsonify(
            {
                "message": f"Código registrado com sucesso! Código: {code} e com a descrição: {description}. atualizado na base de dados '{csv_file}'."
            }
        ), 200


# Rota para pesquisar código por descrição
@app.route("/search")
def search_code():
    description = request.args.get("description")
    results = [
        {"code": code, "description": desc}
        for desc, code in codigo_registro.items()
        if description.lower() in desc.lower()
    ]
    return jsonify(results)


# Rota para gerar e baixar o arquivo CSV
@app.route("/download-csv")
def download_csv():
    if not os.path.exists(csv_file):
        return jsonify({"message": "CSV file not found."}), 400

    # Enviar o arquivo para download
    return send_file(csv_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
