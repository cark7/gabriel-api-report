# Usar imagem baseada no Debian Bookworm (12), onde o wkhtmltopdf ainda existe
FROM python:3.11-slim-bookworm

# Instalar dependências do sistema e o wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libfontconfig1 \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar restante do código
COPY . .

# Variável padrão para produção (sobrescrevível no Coolify)
ENV WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf

# Expor porta
EXPOSE 8000

# Rodar app com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
