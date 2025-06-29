
import pymupdf
from openai import OpenAI

# Abrindo o arquivo pdf 
pdf = pymupdf.open(r'Caminho do PDF')

# função para extrair os textos do pdf
def leitor_pdf(pdf):
    texto = ''    
    # para cada pagina do arquivo do pdf
    for item in range(pdf.page_count):

        # carregar a pagina
        pagina = pdf.load_page(item)

        # pegar o texto da pagina e apendar na variavel texto
        texto += pagina.get_text()
    return texto

#print(leitor_pdf(pdf))

# função para enviar o prompt e os dados extraidos do pdf para IA análisar
def enviar_para_ia():
    client = OpenAI(
        api_key="colocar a kay aqui", 
        base_url="https://openrouter.ai/api/v1"
    )
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "Você é um profissional em RH e esta analisando curriculos e fazendo observaçôes resumidamento, coloca de maneira organizada e os topicos separados por emoticons,bem resumido para nao ficar um texto extenso "},
            {"role": "user", "content": leitor_pdf(pdf)}
        ]
    )
    return response.choices[0].message.content

# Usando com seu prompt do PDF
resposta = enviar_para_ia()

print(resposta)
