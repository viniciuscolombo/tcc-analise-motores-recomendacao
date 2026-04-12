from fastapi import FastAPI

app = FastAPI(title="Motor de Recomendação")

@app.get("/")
def root():
    return {"status": "API rodando liso"}