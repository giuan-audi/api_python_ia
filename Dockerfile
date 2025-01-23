# Use uma imagem oficial do Python como base
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração do Poetry para o container
COPY pyproject.toml poetry.lock ./

# Instala o Poetry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

# Configura o Poetry para não criar um ambiente virtual dentro do container
RUN poetry config virtualenvs.create false

# Instala as dependências do projeto SEM o código do projeto
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o código-fonte da API para o container
COPY ./app /app

# Inicializa o banco de dados
RUN python /app/database/init_db.py

# Expõe a porta que a API vai usar
EXPOSE 8000

# Comando para iniciar a API com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]