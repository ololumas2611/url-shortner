from fastapi import FastAPI
from app.api.routes.urls import urls_route
from app.db.database import create_tables
from app.core.error_handlers import register_error_handlers


app = FastAPI(
    version='1.0.0'
)

# Rota para verificar se a API está a funcionar
@app.get('/health')
def health():
    return {'status': 'OK'}

create_tables()

register_error_handlers(app)

app.include_router(urls_route)
