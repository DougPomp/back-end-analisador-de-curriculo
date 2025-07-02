from flask import Flask, jsonify, request
import fitz  # PyMuPDF
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


# Rota de informações (existente)
@app.route('/')
def info():
    return jsonify({
        "projeto": "Analisador de Currículo com IA",
        "hackathon": "Zeronauta 2025",
        "descricao": "Este projeto utiliza inteligência artificial para analisar currículos em PDF ou Word e fornecer resumos com insights para recrutadores.",
        "funcionalidades": [
            "Upload de currículo (PDF ou DOCX)",
            "Extração e leitura do texto",
            "Análise com modelo de IA",
            "Resumo das competências, experiências e habilidades"
        ],
        "tecnologias": {
            "front-end": "React.js",
            "back-end": "Flask",
            "IA": "OpenAI API",
            "deploy": "Vercel + Render/Fly.io"
        },
        "status": "Em desenvolvimento - Fase 1 Concluída",
    })


# Novo endpoint para análise de currículos
@app.route('/analisar-curriculo', methods=['POST'])
def analisar_curriculo():
    """
    Recebe um arquivo PDF (currículo), extrai o texto e o retorna em formato JSON.
    """
    logging.info("Recebida nova requisição para /analisar-curriculo")

    # 1. Valida se o arquivo foi enviado na requisição
    if 'curriculo' not in request.files:
        logging.warning("Requisição recebida sem o arquivo 'curriculo'")
        return jsonify({"erro": "Nenhum arquivo enviado. Use a chave 'curriculo'."}), 400

    file = request.files['curriculo']

    # 2. Valida se o nome do arquivo não está vazio
    if file.filename == '':
        logging.warning("Requisição com nome de arquivo vazio")
        return jsonify({"erro": "Nome de arquivo vazio."}), 400

    # 3. Processa o arquivo e extrai o texto
    if file and file.filename.lower().endswith('.pdf'):
        try:
            texto_completo = ""
            # Lê o conteúdo do arquivo em memória
            pdf_bytes = file.read()
            # Abre o PDF a partir dos bytes lidos
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                logging.info(f"Processando arquivo PDF: {file.filename}, {len(doc)} páginas.")
                # Itera sobre cada página para extrair o texto
                for page in doc:
                    texto_completo += page.get_text()

            logging.info(f"Extração de texto do arquivo '{file.filename}' concluída com sucesso.")
            return jsonify({"texto_extraido": texto_completo}), 200

        except Exception as e:
            logging.error(f"Falha ao processar o arquivo PDF '{file.filename}': {e}", exc_info=True)
            return jsonify({"erro": "Falha ao ler ou processar o arquivo PDF."}), 500
    else:
        logging.warning(f"Formato de arquivo inválido recebido: {file.filename}")
        return jsonify({"erro": "Formato de arquivo inválido. Por favor, envie um PDF."}), 400


if __name__ == '__main__':
    app.run(debug=True)
