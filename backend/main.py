from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

# Importando os roteadores
from routers import departamentos, usuarios, views, reservas, recursos, disciplinas

app = FastAPI(
    title="API Reserva UFAPE", 
    description="Backend refatorado com FastAPI para o sistema de reservas acadêmicas",
    version="3.0.0" # Nova versão Flawless
)

# Global Exception Handler para erros de Banco de Dados
@app.exception_handler(mysql.connector.Error)
async def mysql_exception_handler(request: Request, exc: mysql.connector.Error):
    # Log interno do erro real (não exibido para o usuário final por segurança)
    print(f"Database Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno de processamento de dados. Nossa equipe já foi notificada."},
    )

# Configuração de CORS para permitir que o Frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando as rotas modularizadas
app.include_router(departamentos.router)
app.include_router(usuarios.router)
app.include_router(recursos.router)
app.include_router(disciplinas.router)
app.include_router(reservas.router)
app.include_router(views.router)

@app.get("/", tags=["Healthcheck"])
def root():
    return {"status": "ok", "mensagem": "API UFAPE Reserva Rodando (Versão Flawless)."}