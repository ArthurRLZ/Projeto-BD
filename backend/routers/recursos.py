from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Recurso

router = APIRouter(prefix="/api/recursos", tags=["Recursos"])

@router.get("/")
def listar_recursos():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM RECURSO;")
        return cursor.fetchall()

@router.post("/", status_code=201)
def criar_recurso(rec: Recurso):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO RECURSO (nome, status_atual) VALUES (%s, %s)"
        cursor.execute(sql, (rec.nome, rec.status_atual))
        conn.commit()
        return {"mensagem": "Recurso criado com sucesso!", "id_inserido": cursor.lastrowid}

@router.put("/{id_recurso}")
def atualizar_recurso(id_recurso: int, rec: Recurso):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "UPDATE RECURSO SET nome = %s, status_atual = %s WHERE id_recurso = %s"
        cursor.execute(sql, (rec.nome, rec.status_atual, id_recurso))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recurso não encontrado")
        return {"mensagem": "Recurso atualizado com sucesso!"}
