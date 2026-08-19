from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import Usuario

router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])

@router.get("/")
def listar_usuarios():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, primeiro_nome, sobrenome, email, tipo_perfil FROM USUARIO LIMIT 20;")
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
