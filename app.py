from flask import Flask, jsonify, request
import fitz  # PyMuPDF
import openai
import os
import json
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração da API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def analisar_texto_com_ia(texto_curriculo: str) -> dict:
    """
    Envia o texto extraído de um currículo para a API da OpenAI e retorna
    as informações estruturadas em formato de dicionário.
    """
    logging.info("Iniciando análise do texto com a IA da OpenAI.")

    prompt = f"""
    Analise o texto do currículo a seguir e extraia as seguintes informações em um formato JSON estrito:
    1.  "nome_completo": O nome completo do candidato.
    2.  "email": O endereço de e-mail principal.
    3.  "telefone": O número de telefone de contato.
    4.  "habilidades_tecnicas": Uma lista (array) das principais habilidades e tecnologias.
    5.  "experiencia_profissional": Uma lista de objetos, onde cada objeto representa uma experiência e contém "cargo", "empresa" e "periodo".

    Texto do Currículo:
    ---
    {texto_curriculo}
    ---

    Retorne APENAS o objeto JSON, sem nenhum texto ou formatação adicional.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Você é um assistente de RH especializado em extrair informações de currículos e retornar dados em formato JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Baixa temperatura para respostas mais consistentes
        )

        # Extrai o conteúdo da resposta, que deve ser uma string JSON
        resultado_json_str = response.choices[0].message.content
        logging.info("Análise da IA concluída com sucesso.")

        # Converte a string JSON em um dicionário Python
        return json.loads(resultado_json_str)

    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar o JSON retornado pela IA: {e}")
        logging.error(f"String recebida da IA: {resultado_json_str}")
        return {"erro": "A resposta da IA não estava em um formato JSON válido."}
    except Exception as e:
        logging.error(f"Erro ao chamar a API da OpenAI: {e}", exc_info=True)
        return {"erro": "Falha na comunicação com a API da OpenAI."}


@app.route('/')
def info():
    return jsonify({
        "projeto": "Analisador de Currículo com IA",
        "hackathon": "Zeronauta 2025",
        "status": "Em desenvolvimento - Fase 2 Concluída",
    })


@app.route('/analisar-curriculo', methods=['POST'])
def analisar_curriculo():
    """
    Recebe um arquivo PDF, extrai o texto e usa a IA para analisar o conteúdo.
    """
    logging.info("Recebida nova requisição para /analisar-curriculo")

    if 'curriculo' not in request.files:
        logging.warning("Requisição recebida sem o arquivo 'curriculo'")
        return jsonify({"erro": "Nenhum arquivo enviado. Use a chave 'curriculo'."}), 400

    file = request.files['curriculo']

    if file.filename == '':
        logging.warning("Requisição com nome de arquivo vazio")
        return jsonify({"erro": "Nome de arquivo vazio."}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            texto_completo = ""
            pdf_bytes = file.read()
            with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
                logging.info(f"Processando arquivo PDF: {file.filename}, {len(doc)} páginas.")
                for page in doc:
                    texto_completo += page.get_text()

            logging.info(f"Extração de texto do arquivo '{file.filename}' concluída.")

            # --- INTEGRAÇÃO COM IA ---
            dados_analisados = analisar_texto_com_ia(texto_completo)

            if "erro" in dados_analisados:
                # Se a análise da IA falhou, retorna o erro específico
                return jsonify(dados_analisados), 502  # 502 Bad Gateway (problema com o serviço externo)

            return jsonify(dados_analisados), 200

        except Exception as e:
            logging.error(f"Falha ao processar o arquivo PDF '{file.filename}': {e}", exc_info=True)
            return jsonify({"erro": "Falha ao ler ou processar o arquivo PDF."}), 500
    else:
        logging.warning(f"Formato de arquivo inválido recebido: {file.filename}")
        return jsonify({"erro": "Formato de arquivo inválido. Por favor, envie um PDF."}), 400


if __name__ == '__main__':
    app.run(debug=True)
