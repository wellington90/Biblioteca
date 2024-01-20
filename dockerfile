FROM python:3.10-slim

# Restante do seu Dockerfile
WORKDIR /app

COPY requirements.txt .

# Instala as dependências necessárias para o mysqlclient
RUN apt-get update && \
    apt-get install -y libmariadb-dev-compat build-essential libssl-dev libffi-dev pkg-config

# Instala as dependências, incluindo o mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "manage.py", "runserver"]
