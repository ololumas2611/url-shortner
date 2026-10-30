from fastapi import FastAPI
from app.api.routes.urls import urls_route


app = FastAPI(
    version='1.0.0'
)

# Rota para verificar se a API está a funcionar
@app.get('/health')
def health():
    return {'status': 'OK'}


app.include_router(urls_route)