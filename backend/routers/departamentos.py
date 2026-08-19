from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Departamento
import mysql.connector

router = APIRouter(prefix="/api/departamentos", tags=["Departamentos"])

@router.post("/", status_code=201)
def criar_departamento(dep: Departamento):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "INSERT INTO DEPARTAMENTO (nome, sigla) VALUES (%s, %s)"
        cursor.execute(sql, (dep.nome, dep.sigla))
        conn.commit()
        return {"mensagem": "Departamento criado com sucesso!", "id_inserido": cursor.lastrowid}

@router.get("/")
def listar_departamentos():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DEPARTAMENTO;")
        return cursor.fetchall()

@router.put("/{id_departamento}")
def atualizar_departamento(id_departamento: int, dep: Departamento):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = "UPDATE DEPARTAMENTO SET nome = %s, sigla = %s WHERE id_departamento = %s"
        cursor.execute(sql, (dep.nome, dep.sigla, id_departamento))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Departamento não encontrado")
        return {"mensagem": "Departamento atualizado com sucesso!"}

@router.delete("/{id_departamento}")
def deletar_departamento(id_departamento: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM DEPARTAMENTO WHERE id_departamento = %s"
            cursor.execute(sql, (id_departamento,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Departamento não encontrado")
            return {"mensagem": "Departamento deletado com sucesso!"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail="Existem registros vinculados a este departamento.")
