# Dicionário de Dados

## Tabela: DEPARTAMENTO
**Descrição:** Armazena os dados dos departamentos acadêmicos da instituição.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_departamento | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único do departamento. |
| nome | VARCHAR(100) | NOT NULL | Nome completo do departamento. |
| sigla | VARCHAR(10) | NOT NULL | Abreviação ou sigla oficial do departamento (ex: BCC). |

## Tabela: USUARIO
**Descrição:** Registra todos os usuários do sistema, englobando alunos, professores, técnicos e administradores.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_usuario | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único do usuário. |
| matricula_siape | VARCHAR(20) | UNIQUE, NOT NULL | Matrícula acadêmica ou SIAPE do servidor. |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Endereço de e-mail institucional. |
| primeiro_nome | VARCHAR(50) | NOT NULL | Nome do usuário. |
| sobrenome | VARCHAR(100) | NOT NULL | Sobrenome do usuário. |
| data_nascimento | DATE | NOT NULL | Data de nascimento do usuário. |
| tipo_perfil | VARCHAR(20) | NOT NULL | Define o nível de acesso: Aluno, Professor, Técnico, Admin. |
| id_departamento | INT | FOREIGN KEY | Referencia o departamento ao qual o usuário está vinculado. |

## Tabela: TELEFONE_USUARIO
**Descrição:** Tabela para armazenar os telefones dos usuários, resolvendo a questão de atributos multivalorados (1FN).

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_telefone | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único do registro de telefone. |
| numero | VARCHAR(20) | NOT NULL | Número de telefone com DDD. |
| tipo | VARCHAR(20) | NOT NULL | Classificação do telefone (ex: Celular, Comercial, WhatsApp). |
| id_usuario | INT | FOREIGN KEY, NOT NULL | Referencia a qual usuário este telefone pertence. |

## Tabela: RECURSO
**Descrição:** Tabela supertipo que generaliza qualquer item que possa ser reservado no sistema (Espaços ou Equipamentos).

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_recurso | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único do recurso. |
| nome | VARCHAR(100) | NOT NULL | Nome descritivo do recurso. |
| status_atual | VARCHAR(30) | NOT NULL | Situação atual: Disponível, Reservado, Em Manutenção, Inativo. |

## Tabela: ESPACO
**Descrição:** Subtipo de RECURSO, representando locais físicos como salas e laboratórios.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_recurso | INT | PRIMARY KEY, FOREIGN KEY | Chave primária que também é estrangeira referenciando RECURSO. |
| capacidade_pessoas | INT | NOT NULL | Quantidade máxima de pessoas comportada pelo local. |
| possui_arcondicionado | BOOLEAN | NOT NULL | Indica presença de refrigeração: 1 (Sim), 0 (Não). |
| loc_predio | VARCHAR(50) | NOT NULL | Nome do prédio onde o espaço está localizado. |
| loc_andar | VARCHAR(20) | NOT NULL | Andar específico no prédio. |
| loc_sala | VARCHAR(20) | NOT NULL | Número ou identificação da sala. |

## Tabela: EQUIPAMENTO
**Descrição:** Subtipo de RECURSO, representando itens móveis como projetores e computadores.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_recurso | INT | PRIMARY KEY, FOREIGN KEY | Chave primária que também é estrangeira referenciando RECURSO. |
| marca | VARCHAR(50) | Nenhuma | Fabricante do equipamento. |
| numero_patrimonio | VARCHAR(50) | UNIQUE, NOT NULL | Registro oficial de tombamento patrimonial. |
| voltagem | VARCHAR(20) | Nenhuma | Especificação elétrica (ex: 110V, 220V, Bivolt). |
| id_espaco_fixo | INT | FOREIGN KEY | Referencia o ESPACO onde o equipamento fica guardado por padrão. |

## Tabela: SEMESTRE_LETIVO
**Descrição:** Controla o calendário acadêmico para associar reservas a períodos específicos.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_semestre | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único do semestre. |
| ano | INT | NOT NULL | Ano letivo (ex: 2026). |
| periodo | INT | NOT NULL | Período do ano (ex: 1 ou 2). |
| data_inicio_aulas | DATE | NOT NULL | Data em que as aulas iniciam. |
| data_fim_aulas | DATE | NOT NULL | Data de encerramento do semestre letivo. |

## Tabela: DISCIPLINA
**Descrição:** Cadastro das matérias ou disciplinas ofertadas pelos departamentos.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_disciplina | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único da disciplina. |
| codigo_oficial | VARCHAR(20) | NOT NULL | Código institucional da matéria (ex: BCC7171). |
| nome | VARCHAR(100) | NOT NULL | Nome descritivo da disciplina. |
| id_departamento | INT | FOREIGN KEY, NOT NULL | Referencia o departamento responsável pela oferta. |

## Tabela: RESERVA
**Descrição:** Entidade principal de movimentação, registrando as solicitações de uso de recursos.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_reserva | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único da solicitação. |
| data_reserva | DATE | NOT NULL | Data para a qual o uso está sendo solicitado. |
| hora_inicio | TIME | NOT NULL | Horário de início do uso pretendido. |
| hora_fim | TIME | NOT NULL | Horário de término do uso pretendido. |
| qtd_participantes_previstos | INT | Nenhuma | Estimativa de pessoas envolvidas. |
| finalidade | VARCHAR(100) | NOT NULL | Objetivo da reserva (ex: Aula prática, Defesa de TCC). |
| status_aprovacao | VARCHAR(30) | NOT NULL | Situação da solicitação: Pendente, Aprovada, Rejeitada. |
| data_hora_analise | DATETIME | Nenhuma | Timestamp de quando a reserva foi avaliada. |
| justificativa_analise | TEXT | Nenhuma | Observação deixada pelo aprovador caso rejeitada ou aprovada com ressalvas. |
| id_solicitante | INT | FOREIGN KEY, NOT NULL | Referencia o USUARIO que solicitou a reserva. |
| id_aprovador | INT | FOREIGN KEY | Referencia o USUARIO (Admin) que analisou o pedido. |
| id_semestre | INT | FOREIGN KEY | Referencia o semestre letivo vigente. |
| id_disciplina | INT | FOREIGN KEY | Opcional; referencia a qual disciplina a reserva atende. |

## Tabela: RECURSO_RESERVA
**Descrição:** Entidade associativa (N:N) que relaciona quais recursos foram alocados em cada reserva, registrando detalhes da posse física.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_reserva | INT | PRIMARY KEY, FOREIGN KEY | Comporá a chave composta. Referencia a RESERVA. |
| id_recurso | INT | PRIMARY KEY, FOREIGN KEY | Comporá a chave composta. Referencia o RECURSO. |
| data_hora_retirada | DATETIME | Nenhuma | Momento exato em que a chave/equipamento foi pego. |
| data_hora_devolucao | DATETIME | Nenhuma | Momento exato em que foi entregue. |
| observacao_avaria | VARCHAR(255) | Nenhuma | Anotações sobre danos percebidos no momento da devolução. |

## Tabela: MANUTENCAO
**Descrição:** Entidade fraca associada a RECURSO, registrando o histórico de reparos e bloqueios.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_recurso | INT | PRIMARY KEY, FOREIGN KEY | Parte da chave composta. Referencia o RECURSO. |
| data_hora_inicio | DATETIME | PRIMARY KEY | Parte da chave composta. Momento de início da manutenção. |
| data_hora_fim | DATETIME | Nenhuma | Previsão ou data efetiva de finalização do serviço. |
| tipo_manutencao | VARCHAR(50) | NOT NULL | Classificação do serviço (ex: Preventiva, Corretiva). |
| descricao_servico | TEXT | NOT NULL | Detalhamento técnico da ação realizada. |
| custo | DECIMAL(10,2) | Nenhuma | Valor gasto no conserto. |

## Tabela: PENALIDADE
**Descrição:** Registra sanções aplicadas aos usuários por mau uso ou atrasos na entrega dos recursos.

| Atributo | Tipo | Restrições | Semântica |
| :--- | :--- | :--- | :--- |
| id_penalidade | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único da sanção. |
| id_usuario | INT | FOREIGN KEY, NOT NULL | Referencia o infrator. |
| id_reserva | INT | FOREIGN KEY, NOT NULL | Referencia a reserva onde a infração ocorreu. |
| motivo | VARCHAR(150) | NOT NULL | Causa da punição (ex: Dano ao equipamento, Atraso grave). |
| data_inicio | DATE | NOT NULL | Dia em que a sanção entra em vigor. |
| data_fim_suspensao | DATE | NOT NULL | Dia em que os direitos do usuário retornam à normalidade. |
