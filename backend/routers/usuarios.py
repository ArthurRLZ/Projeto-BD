from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Usuario
import mysql.connector

router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])

@router.get("/")
def listar_usuarios():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, primeiro_nome, sobrenome, email, tipo_perfil, id_departamento FROM USUARIO LIMIT 20;")
        return cursor.fetchall()

@router.post("/", status_code=201)
def criar_usuario(user: Usuario):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO USUARIO (primeiro_nome, sobrenome, email, tipo_perfil, id_departamento) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user.primeiro_nome, user.sobrenome, user.email, user.tipo_perfil, user.id_departamento))
        conn.commit()
        return {"mensagem": "Usuário cadastrado com sucesso!", "id_inserido": cursor.lastrowid}

@router.put("/{id_usuario}")
def atualizar_usuario(id_usuario: int, user: Usuario):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = """
            UPDATE USUARIO 
            SET primeiro_nome = %s, sobrenome = %s, email = %s, tipo_perfil = %s, id_departamento = %s
            WHERE id_usuario = %s
        """
        cursor.execute(sql, (user.primeiro_nome, user.sobrenome, user.email, user.tipo_perfil, user.id_departamento, id_usuario))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"mensagem": "Usuário atualizado com sucesso!"}

@router.delete("/{id_usuario}")
def deletar_usuario(id_usuario: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM USUARIO WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return {"mensagem": "Usuário deletado com sucesso!"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail="Não foi possível excluir. Existem reservas, telefones ou penalidades vinculadas a este usuário.")
