from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# ... (código existente) ...
app = FastAPI(title="API Reserva UFAPE", description="Backend para o sistema de reservas")

# ADICIONE ESTE BLOCO AQUI:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que o frontend acesse a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Função de conexão com correção de acentuação (utf8mb4)
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="db", 
            user="root",
            password="root",
            database="ufape_reserva_db",
            port=3306,
            charset="utf8mb4" 
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        return None

# ==========================================
# ROTAS DE LEITURA (VIEWS)
# ==========================================

@app.get("/api/historico-reservas", tags=["Views"])
def listar_historico():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco")
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vw_historico_reservas LIMIT 15;")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ==========================================
# MODELOS DE DADOS (PYDANTIC)
# ==========================================
class Departamento(BaseModel):
    nome: str
    sigla: str

# ==========================================
# ROTAS CRUD - TABELA: DEPARTAMENTO
# ==========================================

# 1. CREATE (Criar)
@app.post("/api/departamentos", tags=["Departamentos"], status_code=201)
def criar_departamento(dep: Departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO DEPARTAMENTO (nome, sigla) VALUES (%s, %s)"
        cursor.execute(sql, (dep.nome, dep.sigla))
        conn.commit()
        return {"mensagem": "Departamento criado com sucesso!", "id_inserido": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# 2. READ (Ler)
@app.get("/api/departamentos", tags=["Departamentos"])
def listar_departamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM DEPARTAMENTO;")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 3. UPDATE (Atualizar)
@app.put("/api/departamentos/{id_departamento}", tags=["Departamentos"])
def atualizar_departamento(id_departamento: int, dep: Departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "UPDATE DEPARTAMENTO SET nome = %s, sigla = %s WHERE id_departamento = %s"
        cursor.execute(sql, (dep.nome, dep.sigla, id_departamento))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Departamento não encontrado")
        return {"mensagem": "Departamento atualizado com sucesso!"}
    finally:
        cursor.close()
        conn.close()

# 4. DELETE (Deletar)
@app.delete("/api/departamentos/{id_departamento}", tags=["Departamentos"])
def deletar_departamento(id_departamento: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM DEPARTAMENTO WHERE id_departamento = %s"
        cursor.execute(sql, (id_departamento,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Departamento não encontrado")
        return {"mensagem": "Departamento deletado com sucesso!"}
    except mysql.connector.Error as err:
        # Previne deletar se houver chaves estrangeiras dependentes
        raise HTTPException(status_code=400, detail="Não é possível deletar: existem registros vinculados a este departamento.")
    finally:
        cursor.close()
        conn.close()

# ==========================================
# EXPANSÃO DE VIEWS (RELATÓRIOS)
# ==========================================

@app.get("/api/relatorio-penalidades", tags=["Views"])
def listar_penalidades():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco")
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vw_relatorio_penalidades LIMIT 15;")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

@app.get("/api/detalhes-aulas", tags=["Views"])
def listar_aulas():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco")
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vw_detalhes_aulas LIMIT 15;")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ==========================================
# MODELO E CRUD - TABELA: USUARIO
# ==========================================
class Usuario(BaseModel):
    primeiro_nome: str
    sobrenome: str
    email: str
    tipo_perfil: str
    id_departamento: int

@app.get("/api/usuarios", tags=["Usuários"])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_usuario, primeiro_nome, sobrenome, email, tipo_perfil FROM USUARIO LIMIT 20;")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

@app.post("/api/usuarios", tags=["Usuários"], status_code=201)
def criar_usuario(user: Usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO USUARIO (primeiro_nome, sobrenome, email, tipo_perfil, id_departamento) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user.primeiro_nome, user.sobrenome, user.email, user.tipo_perfil, user.id_departamento))
        conn.commit()
        return {"mensagem": "Usuário cadastrado com sucesso!", "id_inserido": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()