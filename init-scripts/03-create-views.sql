-- Histórico Completo de Reservas
CREATE OR REPLACE VIEW vw_historico_reservas AS
SELECT 
    r.id_reserva,
    r.data_reserva,
    r.finalidade,
    r.status_aprovacao,
    CONCAT(u.primeiro_nome, ' ', u.sobrenome) AS nome_solicitante,
    rec.nome AS nome_recurso,
    rr.data_hora_retirada,
    rr.data_hora_devolucao
FROM RESERVA r
JOIN USUARIO u ON r.id_solicitante = u.id_usuario
JOIN RECURSO_RESERVA rr ON r.id_reserva = rr.id_reserva
JOIN RECURSO rec ON rr.id_recurso = rec.id_recurso;

--Visão de Painel de Infratores e Penalidades
CREATE OR REPLACE VIEW vw_relatorio_penalidades AS
SELECT 
    p.id_penalidade,
    CONCAT(u.primeiro_nome, ' ', u.sobrenome) AS usuario_punido,
    u.tipo_perfil,
    d.sigla AS departamento,
    p.motivo,
    p.data_inicio,
    p.data_fim_suspensao,
    r.finalidade AS reserva_origem
FROM PENALIDADE p
JOIN USUARIO u ON p.id_usuario = u.id_usuario
JOIN DEPARTAMENTO d ON u.id_departamento = d.id_departamento
JOIN RESERVA r ON p.id_reserva = r.id_reserva;

-- detalhamento de Reservas Acadêmicas/Aulas
CREATE OR REPLACE VIEW vw_detalhes_aulas AS
SELECT 
    r.id_reserva,
    r.data_reserva,
    r.hora_inicio,
    r.hora_fim,
    disc.nome AS nome_disciplina,
    disc.codigo_oficial,
    sem.ano,
    sem.periodo,
    CONCAT(u.primeiro_nome, ' ', u.sobrenome) AS professor_responsavel
FROM RESERVA r
JOIN DISCIPLINA disc ON r.id_disciplina = disc.id_disciplina
JOIN SEMESTRE_LETIVO sem ON r.id_semestre = sem.id_semestre
JOIN USUARIO u ON r.id_solicitante = u.id_usuario
WHERE r.id_disciplina IS NOT NULL;