import openai
import os
import json
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def analisar_texto_com_ia(texto_curriculo: str) -> dict:
    """
    Envia o texto extraído de um currículo para a API da OpenAI e retorna
    as informações estruturadas em formato de dicionário.
    """
    logging.info("Iniciando análise do texto com a IA da OpenAI.")

    prompt = f"""
    Analise o texto do currículo a seguir e extraia as seguintes informações em um formato JSON estrito:
    1.  "nome_completo": O nome completo do candidato. Se não encontrar, retorne null.
    2.  "email": O endereço de e-mail principal. Se não encontrar, retorne null.
    3.  "telefone": O número de telefone de contato. Se não encontrar, retorne null.
    4.  "habilidades_tecnicas": Uma lista (array) das principais habilidades e tecnologias. Se não encontrar, retorne uma lista vazia [].
    5.  "experiencia_profissional": Uma lista de objetos, onde cada objeto representa uma experiência e contém "cargo", "empresa" e "periodo". Se não encontrar, retorne uma lista vazia [].

    Texto do Currículo:
    ---
    {texto_curriculo}
    ---

    Retorne APENAS o objeto JSON, sem nenhum texto, comentários ou formatação adicional.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Você é um assistente de RH especializado em extrair informações de currículos e retornar dados em formato JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        resultado_json_str = response.choices[0].message.content
        logging.info("Análise da IA concluída com sucesso.")

        return json.loads(resultado_json_str)

    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar o JSON retornado pela IA. Resposta recebida: {resultado_json_str}")
        raise ValueError("A resposta da IA não estava em um formato JSON válido.")
    except Exception as e:
        logging.error(f"Erro ao chamar a API da OpenAI: {e}", exc_info=True)
        raise ConnectionError("Falha na comunicação com a API da OpenAI.")

