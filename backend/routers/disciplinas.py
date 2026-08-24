from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Disciplina
import mysql.connector

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

@router.put("/{id_disciplina}")
def atualizar_disciplina(id_disciplina: int, disc: Disciplina):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "UPDATE DISCIPLINA SET codigo_oficial = %s, nome = %s, id_departamento = %s WHERE id_disciplina = %s"
        cursor.execute(sql, (disc.codigo_oficial, disc.nome, disc.id_departamento, id_disciplina))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Disciplina não encontrada")
        return {"mensagem": "Disciplina atualizada com sucesso!"}

@router.delete("/{id_disciplina}")
def deletar_disciplina(id_disciplina: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM DISCIPLINA WHERE id_disciplina = %s"
            cursor.execute(sql, (id_disciplina,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Disciplina não encontrada")
            return {"mensagem": "Disciplina deletada com sucesso!"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail="Não foi possível excluir. Existem reservas vinculadas a esta disciplina.")
