FROM python:3.11-slim

# Instalar dependências do sistema e wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libjpeg62-turbo \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
