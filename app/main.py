from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from .pdf_generator import PDFGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Church Reports API",
    description="API para geração de relatórios de escala de cultos em PDF",
    version="1.0.0"
)

pdf_generator = PDFGenerator()

@app.get("/")
async def root():
    return {
        "message": "Church Reports API - Funcionando!",
        "endpoints": {
            "generate_report": "POST /generate-report",
            "health": "GET /health"
        }
    }

@app.post("/generate-report")
async def generate_report(request: dict):
    try:
        if not isinstance(request, dict):
            raise ValueError("Request deve ser um objeto JSON")
        
        if 'events' not in request or not isinstance(request['events'], list):
            raise ValueError("Campo 'events' é obrigatório e deve ser uma lista")
        
        year = request.get('year', '2025')
        month = request.get('month', '1')
        
        logger.info(f"Gerando relatório para {month}/{year}")
        
        pdf_content = pdf_generator.generate_report(request)
        
        filename = f"escala_cultos_{year}_{month.zfill(2)}.pdf"
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Church Reports API"}
