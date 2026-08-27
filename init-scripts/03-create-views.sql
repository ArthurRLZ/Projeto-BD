-- Histórico Completo de Reservas
CREATE OR REPLACE VIEW vw_historico_reservas AS
SELECT 
    r.id_reserva,
    r.data_reserva,
    r.finalidade,
    r.status_aprovacao,
    CONCAT(u.primeiro_nome, ' ', u.sobrenome) AS nome_solicitante,
    rec.id_recurso,
    rec.nome AS nome_recurso,
    rr.data_hora_retirada,
    rr.data_hora_devolucao
FROM RESERVA r
JOIN USUARIO u ON r.id_solicitante = u.id_usuario
JOIN RECURSO_RESERVA rr ON r.id_reserva = rr.id_reserva
JOIN RECURSO rec ON rr.id_recurso = rec.id_recurso;

-- Relatório: Ranking de Uso dos Recursos (para o Gerador de Relatórios)
CREATE OR REPLACE VIEW vw_uso_recursos AS
SELECT
    rec.id_recurso,
    rec.nome AS nome_recurso,
    rec.status_atual,
    COUNT(rr.id_reserva) AS total_reservas,
    SUM(CASE WHEN r.status_aprovacao = 'Aprovada' THEN 1 ELSE 0 END) AS total_aprovadas,
    ROUND(SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fim, r.hora_inicio))) / 3600, 1) AS total_horas_reservadas
FROM RECURSO rec
LEFT JOIN RECURSO_RESERVA rr ON rec.id_recurso = rr.id_recurso
LEFT JOIN RESERVA r ON rr.id_reserva = r.id_reserva
GROUP BY rec.id_recurso, rec.nome, rec.status_atual;

-- Relatório: Ocupação de Reservas por Departamento (para o Gerador de Relatórios)
CREATE OR REPLACE VIEW vw_ocupacao_departamentos AS
SELECT
    d.id_departamento,
    d.nome AS nome_departamento,
    d.sigla,
    COUNT(r.id_reserva) AS total_reservas,
    SUM(CASE WHEN r.status_aprovacao = 'Aprovada' THEN 1 ELSE 0 END) AS total_aprovadas,
    SUM(CASE WHEN r.status_aprovacao = 'Pendente' THEN 1 ELSE 0 END) AS total_pendentes,
    SUM(CASE WHEN r.status_aprovacao = 'Rejeitada' THEN 1 ELSE 0 END) AS total_rejeitadas
FROM DEPARTAMENTO d
LEFT JOIN USUARIO u ON u.id_departamento = d.id_departamento
LEFT JOIN RESERVA r ON r.id_solicitante = u.id_usuario
GROUP BY d.id_departamento, d.nome, d.sigla;

-- Relatório/Evidência do Gatilho: Auditoria de Alterações de Status de Reserva
CREATE OR REPLACE VIEW vw_historico_status_reservas AS
SELECT
    h.id_historico,
    h.id_reserva,
    h.status_anterior,
    h.status_novo,
    h.data_alteracao,
    CONCAT(u.primeiro_nome, ' ', u.sobrenome) AS solicitante,
    CONCAT(a.primeiro_nome, ' ', a.sobrenome) AS alterado_por
FROM HISTORICO_STATUS_RESERVA h
JOIN RESERVA r ON h.id_reserva = r.id_reserva
JOIN USUARIO u ON r.id_solicitante = u.id_usuario
LEFT JOIN USUARIO a ON h.id_aprovador = a.id_usuario;

-- Visão de Painel de Infratores e Penalidades
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