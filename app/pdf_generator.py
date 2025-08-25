import os
import io
import pdfkit
import subprocess
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

        # Detectar wkhtmltopdf
        wkhtml_path = os.environ.get("WKHTMLTOPDF_PATH") or "/usr/bin/wkhtmltopdf"
        self.config = None
        if wkhtml_path and os.path.exists(wkhtml_path):
            self.config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)

        # Detectar wkhtmltoimage (opcional; se não achar, usa o binário do PATH)
        self.wkhtmltoimage = os.environ.get("WKHTMLTOIMAGE_PATH") or "wkhtmltoimage"

    def _render_html(self, data: dict) -> str:
        template = self.env.get_template("report.html")
        month_names = {
            "1": "Janeiro", "2": "Fevereiro", "3": "Março", "4": "Abril",
            "5": "Maio", "6": "Junho", "7": "Julho", "8": "Agosto",
            "9": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
        }

        template_data = {
            "year": data.get("year", "2025"),
            "month": month_names.get(str(data.get("month", "1")), str(data.get("month", "1"))),
            "igreja_nome": data.get("igreja_nome", "Igreja IPUB Salomé"),
            "events": data.get("events", []),
            "total_events": len(data.get("events", [])),
            "generated_date": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
        }
        return template.render(**template_data)

    def generate_report(self, data: dict) -> bytes:
        html_content = self._render_html(data)
        if self.config:
            return pdfkit.from_string(html_content, False, configuration=self.config)
        return pdfkit.from_string(html_content, False)

    def generate_image(self, data: dict, image_format: str = "png") -> bytes:
        """
        Gera imagem (png/jpg/bmp/svg*) a partir do mesmo HTML do PDF.
        Requer 'wkhtmltoimage' instalado no sistema.
        """
        html_content = self._render_html(data)

        # Arquivos temporários
        html_path = "/tmp/report.html"
        img_path = f"/tmp/report.{image_format}"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Chama wkhtmltoimage
        subprocess.run([self.wkhtmltoimage, html_path, img_path], check=True)

        with open(img_path, "rb") as f:
            return f.read()
