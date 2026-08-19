from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Disciplina

router = APIRouter(prefix="/api/disciplinas", tags=["Disciplinas"])

@router.get("/")
def listar_disciplinas():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DISCIPLINA;")
        return cursor.fetchall()

@router.post("/", status_code=201)
def criar_disciplina(disc: Disciplina):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO DISCIPLINA (codigo_oficial, nome, id_departamento) VALUES (%s, %s, %s)"
        cursor.execute(sql, (disc.codigo_oficial, disc.nome, disc.id_departamento))
        conn.commit()
        return {"mensagem": "Disciplina criada com sucesso!", "id_inserido": cursor.lastrowid}
