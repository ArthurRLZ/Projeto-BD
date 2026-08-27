from fastapi import APIRouter
from database import get_db_connection

router = APIRouter(prefix="/api/relatorios", tags=["Relatórios"])

@router.get("/resumo-status")
def resumo_status():
    """Contagem de reservas agrupadas por status (consulta agregada complexa)."""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status_aprovacao, COUNT(*) AS total
            FROM RESERVA
            GROUP BY status_aprovacao;
        """)
        return cursor.fetchall()

@router.get("/uso-recursos")
def uso_recursos():
    """Ranking de utilização dos recursos (baseado na view vw_uso_recursos)."""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_uso_recursos ORDER BY total_reservas DESC;")
        return cursor.fetchall()

@router.get("/ocupacao-departamentos")
def ocupacao_departamentos():
    """Ocupação/demanda de reservas por departamento (baseado na view vw_ocupacao_departamentos)."""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_ocupacao_departamentos ORDER BY total_reservas DESC;")
        return cursor.fetchall()

@router.get("/auditoria-status")
def auditoria_status():
    """Histórico de alterações de status de reservas, populado automaticamente pelo gatilho trg_historico_status_reserva."""
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vw_historico_status_reservas ORDER BY data_alteracao DESC LIMIT 100;")
        return cursor.fetchall()
