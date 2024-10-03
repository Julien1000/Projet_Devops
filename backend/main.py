from fastapi import FastAPI, Request , APIRouter ,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd

app = FastAPI()
router = APIRouter(prefix="/api/v1")
# Configuration des templates
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root():
    return {"message": "Hello, CACA Song Attributes!"}

@router.get("/data", response_class=HTMLResponse)
async def get_data(request: Request):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv('./data/spotify_data.csv')  # Ajuster le chemin si nécessaire

    # Convertir le DataFrame en HTML
    table_html = df.to_html(classes='table table-striped')
    # Rendre le template avec la table
    return templates.TemplateResponse("index.html", {"request": request, "table": table_html})

@router.post("/predict")
async def predict(query: Optional[str] = Form(None)):
    return {"query": query}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

