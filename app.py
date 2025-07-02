from flask import Flask, jsonify, request
import logging
from extracao import extrair_texto_de_pdf
from analise import analisar_texto_com_ia
from flask_cors import CORS

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Libera CORS para um domínio específico:
CORS(app, resources={r"/*": {"origins": "https://curriculo-ai.zeronauta.com.br"}})

# Define um limite máximo para o tamanho do arquivo (5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


@app.route('/')
def info():
    return jsonify({
        "projeto": "Analisador de Currículo com IA",
        "versao": "1.0.0",
        "status": "Projeto Concluído",
        "descricao": "API que utiliza inteligência artificial para extrair informações estruturadas de currículos em formato PDF."
    })


@app.route('/analisar-curriculo', methods=['POST'])
def analisar_curriculo_route():
    """
    Rota principal que orquestra o processo de análise de currículo.
    """
    logging.info("Recebida nova requisição para /analisar-curriculo")

    try:
        if 'curriculo' not in request.files:
            logging.warning("Requisição recebida sem o arquivo 'curriculo'")
            return jsonify({"erro": "Nenhum arquivo enviado. Use a chave 'curriculo'."}), 400

        file = request.files['curriculo']

        if file.filename == '':
            logging.warning("Requisição com nome de arquivo vazio")
            return jsonify({"erro": "Nome de arquivo vazio."}), 400

        if not file.filename.lower().endswith('.pdf'):
            logging.warning(f"Formato de arquivo inválido recebido: {file.filename}")
            return jsonify({"erro": "Formato de arquivo inválido. Por favor, envie um PDF."}), 400

        pdf_bytes = file.read()

        # 1. Extração de Texto
        texto_curriculo = extrair_texto_de_pdf(pdf_bytes, file.filename)

        # 2. Análise com IA
        dados_analisados = analisar_texto_com_ia(texto_curriculo)

        return jsonify(dados_analisados), 200

    except ValueError as e:
        # Erro de negócio (ex: PDF inválido, JSON da IA malformado)
        return jsonify({"erro": str(e)}), 422  # Unprocessable Entity
    except ConnectionError as e:
        # Erro de comunicação com serviço externo (OpenAI)
        return jsonify({"erro": str(e)}), 502  # Bad Gateway
    except Exception as e:
        # Trata erros inesperados, incluindo o de arquivo muito grande (RequestEntityTooLarge)
        if 'Request Entity Too Large' in str(e):
            logging.warning("Tentativa de upload de arquivo maior que o limite permitido.")
            return jsonify({"erro": "Arquivo muito grande. O limite é de 5MB."}), 413

        logging.error(f"Ocorreu um erro inesperado: {e}", exc_info=True)
        return jsonify({"erro": "Ocorreu um erro interno no servidor."}), 500


if __name__ == '__main__':
    # Em um ambiente de produção, use um servidor WSGI como Gunicorn
    app.run(debug=False)
