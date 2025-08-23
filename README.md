# 📖 Church Reports API

API em **FastAPI** para geração de relatórios de escala de cultos em **PDF**.  
Baseada em templates **HTML + CSS (Jinja2)** e renderização com **pdfkit + wkhtmltopdf**.

---

## 🚀 Tecnologias usadas
- [FastAPI](https://fastapi.tiangolo.com/) → criação da API
- [pdfkit](https://pypi.org/project/pdfkit/) → wrapper Python para wkhtmltopdf
- [wkhtmltopdf](https://wkhtmltopdf.org/) → conversão de HTML em PDF
- [Jinja2](https://jinja.palletsprojects.com/) → templates dinâmicos HTML
- [Uvicorn](https://www.uvicorn.org/) → servidor ASGI

---

## 📂 Estrutura do projeto

church-reports-api/
├── app/
│ ├── init.py
│ ├── main.py # Rotas da API
│ ├── pdf_generator.py # Geração do PDF
│ └── templates/
│ └── report.html # Template do relatório
├── requirements.txt
├── .env # Caminho do wkhtmltopdf (Windows)
├── Dockerfile # Configuração para produção em container
└── README.md

---

## ⚙️ Instalação no Windows

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/church-reports-api.git
   cd church-reports-api
2. Crie ambiente virtual:

python -m venv .venv
.venv\Scripts\activate

3. Instale dependências:

pip install -r requirements.txt

4. Configure .env (raiz do projeto):

WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe

5. Rodando a API
uvicorn app.main:app --reload

API disponível em:
👉 http://127.0.0.1:8000

## Gerar relatório
POST /generate-report
{
  "year": "2025",
  "month": "8",
  "igreja_nome": "Igreja Exemplo",
  "events": [
    {
      "date": "02/08/2025",
      "tipo_culto": "Culto de Oração",
      "pregador": "Pr. João",
      "dirigente": "Maria",
      "louvor": "Equipe 1",
      "instrumentistas": "Carlos e Ana"
    },
    {
      "date": "09/08/2025",
      "tipo_culto": "Culto da Família",
      "pregador": "Pr. José",
      "dirigente": "Pedro",
      "louvor": "Equipe 2",
      "instrumentistas": "Lucas e Paulo"
    }
  ]
}
