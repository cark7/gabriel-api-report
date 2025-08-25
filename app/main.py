import io
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
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


@app.post("/generate-report-image")
async def generate_report_image(request: dict, fmt: str = Query("png")):
    """
    Recebe o MESMO JSON do /generate-report e retorna imagem (png/jpg).
    Exemplo de uso:
    POST /generate-report-image?fmt=jpg
    Body:
    {
      "year": "2025",
      "month": "6",
      "igreja_nome": "...",
      "events": [ ... ]
    }
    """
    try:
        if not isinstance(request, dict):
            raise ValueError("Request deve ser um objeto JSON")

        if 'events' not in request or not isinstance(request['events'], list):
            raise ValueError("Campo 'events' é obrigatório e deve ser uma lista")

        year = request.get('year', '2025')
        month = str(request.get('month', '1'))
        filename = f"escala_cultos_{year}_{month.zfill(2)}.{fmt}"

        img_bytes = pdf_generator.generate_image(request, image_format=fmt)

        return StreamingResponse(
            io.BytesIO(img_bytes),
            media_type=f"image/{'jpeg' if fmt in ('jpg', 'jpeg') else fmt}",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )

    except Exception as e:
        logger.error(f"Erro ao gerar imagem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar imagem: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Church Reports API"}
