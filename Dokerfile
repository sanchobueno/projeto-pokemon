# Imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro
COPY app/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto
COPY app/ .

# Define o comando padrão para rodar o main.py
CMD ["python", "main.py"]
