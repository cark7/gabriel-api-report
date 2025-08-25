import os
import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis do .env (se existir)
load_dotenv()


class PDFGenerator:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"])
        )

        # Detectar wkhtmltopdf no Windows via .env
        wkhtml_path = os.environ.get("WKHTMLTOPDF_PATH")

        if not wkhtml_path:  
            # tenta default Linux
            wkhtml_path = "/usr/bin/wkhtmltopdf"

        self.config = None
        if wkhtml_path and os.path.exists(wkhtml_path):
            self.config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)

    def generate_report(self, data: dict) -> bytes:
        template = self.env.get_template("report.html")

        month_names = {
            "1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril",
            "5": "Maio", "6": "Junho", "7": "Julho", "8": "Agosto",
            "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
        }

        template_data = {
            "year": data.get("year", "2025"),
            "month": month_names.get(data.get("month", "1"), data.get("month", "1")),
            "igreja_nome": data.get("igreja_nome", "Igreja IPUB Salomé"),
            "events": data.get("events", []),
            "total_events": len(data.get("events", [])),
            "generated_date": datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        }

        html_content = template.render(**template_data)

        if self.config:
            pdf_bytes = pdfkit.from_string(html_content, False, configuration=self.config)
        else:
            pdf_bytes = pdfkit.from_string(html_content, False)

        return pdf_bytes
