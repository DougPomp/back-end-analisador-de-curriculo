# Dockerfile

# 1. Imagem Base: Começamos com uma imagem Python leve e oficial.
FROM python:3.9-slim

# 2. Variáveis de Ambiente: Evita que o Python gere arquivos .pyc e bufferize os logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Diretório de Trabalho: Define o diretório onde nossa aplicação ficará dentro do contêiner.
WORKDIR /app

# 4. Instalação de Dependências:
# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker.
# Se o requirements.txt não mudar, o Docker não reinstalará tudo a cada build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Criação de Usuário Não-Root: Cria um usuário e grupo dedicados para a aplicação.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# 6. Copia do Código da Aplicação: Copia o resto dos arquivos da aplicação para o contêiner.
# As permissões serão ajustadas após a cópia.
COPY . .

# 7. Ajuste de Permissões: Garante que o usuário da aplicação tenha acesso aos arquivos.
RUN chown -R appuser:appgroup /app
RUN chmod -R 755 /app # Permite leitura e execução para o usuário/grupo, e leitura/execução para outros.

# 8. Usuário de Execução: Muda para o usuário não-root.
USER appuser

# 9. Exposição da Porta: Informa ao Docker que o contêiner ouvirá na porta 5000.
# Usaremos gunicorn para rodar a aplicação.
EXPOSE 5000

# 10. Comando de Execução: O comando que será executado quando o contêiner iniciar.
# Gunicorn é um servidor WSGI de produção, muito mais robusto que o servidor de desenvolvimento do Flask.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
