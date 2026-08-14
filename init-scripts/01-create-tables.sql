
CREATE TABLE DEPARTAMENTO (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(10) NOT NULL
);

CREATE TABLE USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    matricula_siape VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    primeiro_nome VARCHAR(50) NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    data_nascimento DATE NOT NULL,
    tipo_perfil VARCHAR(20) NOT NULL,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO(id_departamento)
);

-- 3. Criação da tabela TELEFONE_USUARIO (Atributo multivalorado)
CREATE TABLE TELEFONE_USUARIO (
    id_telefone INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- 4. Criação da tabela RECURSO (Tabela "Pai" na herança)
CREATE TABLE RECURSO (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    status_atual VARCHAR(30) NOT NULL
);

-- 5. Criação da tabela ESPACO (Especialização de RECURSO)
CREATE TABLE ESPACO (
    id_recurso INT PRIMARY KEY,
    capacidade_pessoas INT NOT NULL,
    possui_arcondicionado BOOLEAN NOT NULL,
    loc_predio VARCHAR(50) NOT NULL,
    loc_andar VARCHAR(20) NOT NULL,
    loc_sala VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_recurso) REFERENCES RECURSO(id_recurso)
);

-- 6. Criação da tabela EQUIPAMENTO (Especialização de RECURSO)
CREATE TABLE EQUIPAMENTO (
    id_recurso INT PRIMARY KEY,
    marca VARCHAR(50),
    numero_patrimonio VARCHAR(50) UNIQUE NOT NULL,
    voltagem VARCHAR(20),
    id_espaco_fixo INT,
    FOREIGN KEY (id_recurso) REFERENCES RECURSO(id_recurso),
    FOREIGN KEY (id_espaco_fixo) REFERENCES ESPACO(id_recurso)
);

-- 7. Criação da tabela SEMESTRE_LETIVO
CREATE TABLE SEMESTRE_LETIVO (
    id_semestre INT AUTO_INCREMENT PRIMARY KEY,
    ano INT NOT NULL,
    periodo INT NOT NULL,
    data_inicio_aulas DATE NOT NULL,
    data_fim_aulas DATE NOT NULL
);

-- 8. Criação da tabela DISCIPLINA
CREATE TABLE DISCIPLINA (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    codigo_oficial VARCHAR(20) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    id_departamento INT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES DEPARTAMENTO(id_departamento)
);

-- 9. Criação da tabela RESERVA
CREATE TABLE RESERVA (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    qtd_participantes_previstos INT,
    finalidade VARCHAR(100) NOT NULL,
    status_aprovacao VARCHAR(30) NOT NULL,
    data_hora_analise DATETIME,
    justificativa_analise TEXT,
    id_solicitante INT NOT NULL,
    id_aprovador INT,
    id_semestre INT,
    id_disciplina INT,
    FOREIGN KEY (id_solicitante) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_aprovador) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_semestre) REFERENCES SEMESTRE_LETIVO(id_semestre),
    FOREIGN KEY (id_disciplina) REFERENCES DISCIPLINA(id_disciplina)
);

-- 10. Criação da tabela RECURSO_RESERVA (Associativa N:N)
CREATE TABLE RECURSO_RESERVA (
    id_reserva INT,
    id_recurso INT,
    data_hora_retirada DATETIME,
    data_hora_devolucao DATETIME,
    observacao_avaria VARCHAR(255),
    PRIMARY KEY (id_reserva, id_recurso),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva),
    FOREIGN KEY (id_recurso) REFERENCES RECURSO(id_recurso)
);

-- 11. Criação da tabela MANUTENCAO (Entidade Fraca)
CREATE TABLE MANUTENCAO (
    id_recurso INT,
    data_hora_inicio DATETIME,
    data_hora_fim DATETIME,
    tipo_manutencao VARCHAR(50) NOT NULL,
    descricao_servico TEXT NOT NULL,
    custo DECIMAL(10,2),
    PRIMARY KEY (id_recurso, data_hora_inicio),
    FOREIGN KEY (id_recurso) REFERENCES RECURSO(id_recurso)
);

-- 12. Criação da tabela PENALIDADE
CREATE TABLE PENALIDADE (
    id_penalidade INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_reserva INT NOT NULL,
    motivo VARCHAR(150) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim_suspensao DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
    FOREIGN KEY (id_reserva) REFERENCES RESERVA(id_reserva)
);