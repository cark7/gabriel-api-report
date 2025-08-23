FROM ubuntu:22.04

# Evitar prompts durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python e dependências
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    wkhtmltopdf \
    libjpeg8 \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    fontconfig \
 && rm -rf /var/lib/apt/lists/*

# Criar link simbólico para python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
