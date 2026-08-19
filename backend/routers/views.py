from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api", tags=["Views"])

@router.get("/historico-reservas")
def listar_historico():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_historico_reservas ORDER BY data_reserva DESC LIMIT 50;")
        return cursor.fetchall()

@router.get("/relatorio-penalidades")
def listar_penalidades():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_relatorio_penalidades ORDER BY data_inicio DESC LIMIT 50;")
        return cursor.fetchall()

@router.get("/detalhes-aulas")
def listar_aulas():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_detalhes_aulas ORDER BY data_reserva DESC LIMIT 50;")
        return cursor.fetchall()
