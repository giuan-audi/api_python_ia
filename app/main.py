from fastapi import FastAPI
from app.routers import generation, prompts

app = FastAPI()

app.include_router(generation.router, prefix="/generate", tags=["generation"])
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])


@app.get("/")
async def root():
    return {"message": "API Python para Gestão de Demandas com IA - Online!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
