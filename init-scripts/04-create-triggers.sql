-- ============================================================================
-- Gatilhos (Triggers) do sistema de reservas UFAPE
--
-- 1) trg_historico_status_reserva
--    Regra de auditoria: sempre que o status de aprovação de uma RESERVA muda,
--    grava uma linha em HISTORICO_STATUS_RESERVA com o status anterior, o novo
--    status, quem realizou a análise e o instante da alteração.
--
-- 2) trg_recurso_reservado_ao_aprovar
--    Regra de negócio: quando uma reserva passa a ser 'Aprovada', os recursos
--    vinculados a ela (RECURSO_RESERVA) têm seu status automaticamente
--    alterado para 'Reservado', evitando que fiquem "Disponível" indevidamente.
--
-- 3) trg_recurso_disponivel_ao_devolver
--    Regra de negócio: quando a devolução de um recurso é registrada
--    (RECURSO_RESERVA.data_hora_devolucao deixa de ser NULL), o recurso volta
--    automaticamente ao status 'Disponível', liberando-o para novas reservas.
-- ============================================================================

SET NAMES utf8mb4;

DELIMITER $$

CREATE TRIGGER trg_historico_status_reserva
AFTER UPDATE ON RESERVA
FOR EACH ROW
BEGIN
    IF NOT (OLD.status_aprovacao <=> NEW.status_aprovacao) THEN
        INSERT INTO HISTORICO_STATUS_RESERVA (id_reserva, status_anterior, status_novo, id_aprovador)
        VALUES (NEW.id_reserva, OLD.status_aprovacao, NEW.status_aprovacao, NEW.id_aprovador);
    END IF;
END$$

CREATE TRIGGER trg_recurso_reservado_ao_aprovar
AFTER UPDATE ON RESERVA
FOR EACH ROW
BEGIN
    IF NEW.status_aprovacao = 'Aprovada' AND OLD.status_aprovacao <> 'Aprovada' THEN
        UPDATE RECURSO
        SET status_atual = 'Reservado'
        WHERE status_atual = 'Disponível'
          AND id_recurso IN (
              SELECT id_recurso FROM RECURSO_RESERVA WHERE id_reserva = NEW.id_reserva
          );
    END IF;
END$$

CREATE TRIGGER trg_recurso_disponivel_ao_devolver
AFTER UPDATE ON RECURSO_RESERVA
FOR EACH ROW
BEGIN
    IF NEW.data_hora_devolucao IS NOT NULL AND OLD.data_hora_devolucao IS NULL THEN
        UPDATE RECURSO
        SET status_atual = 'Disponível'
        WHERE id_recurso = NEW.id_recurso;
    END IF;
END$$

DELIMITER ;
