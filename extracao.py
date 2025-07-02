import fitz  # PyMuPDF
import logging


def extrair_texto_de_pdf(pdf_bytes: bytes, nome_arquivo: str) -> str:
    """
    Extrai o texto completo de um arquivo PDF fornecido em bytes.

    Args:
        pdf_bytes: O conteúdo do arquivo PDF em bytes.
        nome_arquivo: O nome do arquivo para fins de logging.

    Returns:
        O texto extraído do PDF como uma string.

    Raises:
        Exception: Se ocorrer um erro durante o processamento do PDF.
    """
    texto_completo = ""
    try:
        # Abre o PDF a partir dos bytes em memória
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            logging.info(f"Processando arquivo PDF: {nome_arquivo}, {len(doc)} páginas.")
            # Itera sobre cada página para extrair o texto
            for page in doc:
                texto_completo += page.get_text()

        logging.info(f"Extração de texto do arquivo '{nome_arquivo}' concluída com sucesso.")
        return texto_completo
    except Exception as e:
        logging.error(f"Falha ao ler ou processar o arquivo PDF '{nome_arquivo}': {e}", exc_info=True)
        # Relança a exceção para ser tratada pela rota da API
        raise ValueError("Falha ao processar o arquivo PDF.")

