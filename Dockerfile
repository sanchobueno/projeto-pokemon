# Imagem base oficial do Python
FROM python:3.11-slim

# Instala cron
RUN apt-get update && apt-get install -y cron && apt-get clean

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro
COPY app/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto
COPY app/ .

# Copia o arquivo do crontab para dentro do container
COPY cronjob /etc/cron.d/pokemon-cron

# Dá permissão para o cronjob
RUN chmod 0644 /etc/cron.d/pokemon-cron

# Registra o cronjob
RUN crontab /etc/cron.d/pokemon-cron

# Cria o arquivo de log do cron
RUN touch /var/log/cron.log

# Comando para iniciar cron + rodar a aplicação
CMD cron && tail -f /var/log/cron.log
