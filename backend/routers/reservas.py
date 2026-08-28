from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import ReservaCreate, ReservaAprovar, DevolucaoRecurso
import mysql.connector

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

@router.post("/", status_code=201)
def criar_reserva(reserva: ReservaCreate):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # inicia transacao
            conn.start_transaction()
            
            if not reserva.recursos:
                raise HTTPException(status_code=400, detail="Pelo menos um recurso deve ser selecionado.")
            
            # ve se ta disponivel
            formato_recursos = ','.join(['%s'] * len(reserva.recursos))
            sql_status = f"SELECT id_recurso, nome, status_atual FROM RECURSO WHERE id_recurso IN ({formato_recursos})"
            cursor.execute(sql_status, tuple(reserva.recursos))
            recursos_bd = cursor.fetchall()
            
            if len(recursos_bd) != len(reserva.recursos):
                raise HTTPException(status_code=404, detail="Um ou mais recursos solicitados não existem.")
                
            for rec in recursos_bd:
                if rec['status_atual'] in ['Em Manutenção', 'Inativo']:
                    raise HTTPException(status_code=400, detail=f"O recurso {rec['nome']} não pode ser reservado pois está {rec['status_atual']}.")
            
            # checa conflito de horario
            sql_conflito = f"""
                SELECT r.id_reserva, rr.id_recurso 
                FROM RESERVA r
                JOIN RECURSO_RESERVA rr ON r.id_reserva = rr.id_reserva
                WHERE r.data_reserva = %s 
                AND r.status_aprovacao != 'Rejeitada'
                AND rr.id_recurso IN ({formato_recursos})
                AND (
                    (r.hora_inicio <= %s AND r.hora_fim > %s) OR
                    (r.hora_inicio < %s AND r.hora_fim >= %s) OR
                    (%s <= r.hora_inicio AND %s >= r.hora_fim)
                )
            """
            params_conflito = [reserva.data_reserva] + list(reserva.recursos) + [
                reserva.hora_inicio, reserva.hora_inicio,
                reserva.hora_fim, reserva.hora_fim,
                reserva.hora_inicio, reserva.hora_fim
            ]
            
            cursor.execute(sql_conflito, tuple(params_conflito))
            conflitos = cursor.fetchall()
            
            if conflitos:
                raise HTTPException(status_code=409, detail="Conflito de horário detectado para um ou mais recursos solicitados.")
            
            # salva no banco
            sql_reserva = """
                INSERT INTO RESERVA 
                (data_reserva, hora_inicio, hora_fim, qtd_participantes_previstos, finalidade, status_aprovacao, id_solicitante, id_disciplina, id_semestre)
                VALUES (%s, %s, %s, %s, %s, 'Pendente', %s, %s, %s)
            """
            valores_reserva = (
                reserva.data_reserva, reserva.hora_inicio, reserva.hora_fim, 
                reserva.qtd_participantes_previstos, reserva.finalidade, 
                reserva.id_solicitante, reserva.id_disciplina, reserva.id_semestre
            )
            cursor.execute(sql_reserva, valores_reserva)
            id_reserva = cursor.lastrowid
            
            # liga a reserva com os recursos
            sql_recurso = "INSERT INTO RECURSO_RESERVA (id_reserva, id_recurso) VALUES (%s, %s)"
            valores_recursos = [(id_reserva, id_rec) for id_rec in reserva.recursos]
            cursor.executemany(sql_recurso, valores_recursos)
            
            # deu certo
            conn.commit()
            return {"mensagem": "Reserva solicitada com sucesso!", "id_reserva": id_reserva}
            
        except HTTPException as http_exc:
            conn.rollback()
            raise http_exc
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail="Erro interno ao processar a reserva.")

@router.put("/{id_reserva}/aprovar")
def analisar_reserva(id_reserva: int, analise: ReservaAprovar):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = """
            UPDATE RESERVA 
            SET status_aprovacao = %s, justificativa_analise = %s, id_aprovador = %s, data_hora_analise = NOW()
            WHERE id_reserva = %s
        """
        cursor.execute(sql, (analise.status_aprovacao, analise.justificativa_analise, analise.id_aprovador, id_reserva))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
            
        return {"mensagem": f"Reserva {analise.status_aprovacao.lower()} com sucesso!"}

@router.delete("/{id_reserva}")
def deletar_reserva(id_reserva: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            # apaga recursos primeiro
            cursor.execute("DELETE FROM RECURSO_RESERVA WHERE id_reserva = %s", (id_reserva,))
            # apaga reserva
            cursor.execute("DELETE FROM RESERVA WHERE id_reserva = %s", (id_reserva,))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Reserva não encontrada ou já deletada.")
                
            conn.commit()
            return {"mensagem": "Reserva cancelada/excluída com sucesso."}
        except mysql.connector.Error as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao excluir. Pode existir dependências (ex: Penalidades). {err}")

@router.put("/{id_reserva}/recursos/{id_recurso}/devolucao")
def registrar_devolucao(id_reserva: int, id_recurso: int, dados: DevolucaoRecurso):
    """Registra a devolução de um recurso vinculado a uma reserva.
    O gatilho trg_recurso_disponivel_ao_devolver libera automaticamente o
    recurso (status_atual = 'Disponível') no banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql = """
            UPDATE RECURSO_RESERVA
            SET data_hora_retirada = COALESCE(data_hora_retirada, NOW()),
                data_hora_devolucao = NOW(),
                observacao_avaria = %s
            WHERE id_reserva = %s AND id_recurso = %s
        """
        cursor.execute(sql, (dados.observacao_avaria, id_reserva, id_recurso))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vínculo entre reserva e recurso não encontrado.")

        return {"mensagem": "Devolução registrada com sucesso! O recurso foi liberado automaticamente pelo gatilho do banco de dados."}
