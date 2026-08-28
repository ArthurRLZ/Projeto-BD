# Projeto Banco de Dados — Transformação do Diagrama Conceitual (MERE) para o Esquema Lógico



## Integrantes do grupo
- Arthur Ricardo Matias Passos
- Augusto Jorge Brandão Mendonça
- Luís Arthur Siqueira Rodrigues
- Euclides Emanuel Laurindo

## Contexto do Projeto
Este projeto implementa o mapeamento do Diagrama Conceitual (MERE), elaborado na etapa anterior, para o Esquema Lógico Relacional, com a implementação física e povoamento do banco de dados em ambiente de contêiner Docker. O sistema tem como objetivo gerenciar as reservas de recursos (espaços e equipamentos) acadêmicos.

**SGBD utilizado:** MySQL 8.0

**Dados de acesso ao banco:**
| Parâmetro        | Valor              |
|------------------|--------------------|
| Host             | localhost          |
| Porta            | 3306               |
| Usuário          | root               |
| Senha            | root               |
| Banco de Dados   | ufape_reserva_db   |
**Portas de Acesso da Aplicação:**
| Serviço | Porta Exposta | Acesso Localhost |
|---------|---------------|------------------|
| Banco de Dados (MySQL) | 3306 | `localhost:3306` |
| Backend API (FastAPI) | 8000 | `http://localhost:8000/docs` |
| Frontend SPA (Nginx) | 3000 | `http://localhost:3000` |

## Como executar o projeto

```bash
# Limpar volumes antigos  
docker compose down -v

# Subir o projeto 
docker compose up -d
```

Após subir os contêineres, a aplicação fica disponível em:
- Frontend: `http://localhost:3000`
- Backend (Swagger/Docs): `http://localhost:8000/docs`
- Banco de Dados (MySQL): `localhost:3306`

Os scripts em `init-scripts/` são executados automaticamente pelo MySQL na primeira
inicialização do contêiner, na ordem:
1. `01-create-tables.sql` — criação das tabelas e índices (DDL)
2. `02-insert-data.sql` — povoamento das tabelas (DML)
3. `03-create-views.sql` — criação das Views utilizadas pelos relatórios e telas do sistema
4. `04-create-triggers.sql` — criação do(s) gatilho(s) (triggers) do banco de dados

## Estrutura do repositório

```text
PROJETO-BD/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── routers/
│       ├── departamentos.py
│       ├── disciplinas.py
│       ├── recursos.py
│       ├── reservas.py
│       ├── usuarios.py
│       ├── views.py
│       └── relatorios.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── docs/
│   ├── diagrama-conceitual.pdf
│   └── dicionario-de-dados.md
├── init-scripts/
│   ├── 01-create-tables.sql
│   ├── 02-insert-data.sql
│   ├── 03-create-views.sql
│   └── 04-create-triggers.sql
├── scripts/
│   └── gerador_dados.py
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Esquema Conceitual do Banco de Dados
O Diagrama Entidade-Relacionamento (MERE) atualizado do sistema encontra-se em [`docs/diagrama-conceitual.pdf`](docs/diagrama-conceitual.pdf).

## Dicionário de Dados
> As descrições detalhadas de cada tabela, incluindo tipos de dados, restrições (constraints) como chaves primárias e estrangeiras, além da semântica de cada atributo, encontram-se documentadas no arquivo `docs/dicionario-de-dados.md` (ou PDF equivalente em anexo).

## Normalização
O esquema lógico implementado atende plenamente à Terceira Forma Normal (3FN) e, consequentemente, à 2FN. 
- **1FN:** Os atributos multivalorados foram isolados em tabelas próprias (como a tabela `TELEFONE_USUARIO`).
- **2FN:** Todos os atributos não-chave dependem de forma total e não parcial da chave primária (por exemplo, os dados na tabela `USUARIO` dependem integralmente do `id_usuario`).
- **3FN:** Não há dependências transitivas entre atributos não-chave. Além disso, a herança entre `RECURSO`, `ESPACO` e `EQUIPAMENTO` foi mapeada separando as tabelas com chaves estrangeiras, eliminando a necessidade de atributos nulos (NULL) para campos que pertenceriam apenas a um subtipo.

## Metodologia de Povoamento
A estratégia utilizada para gerar o volume de dados exigido consistiu na criação de um script de automação em Python (`scripts/gerador_dados.py`). Utilizando a biblioteca de dados artificiais reais `Faker`, o script foi responsável por montar comandos DML dinâmicos, respeitando totalmente a integridade referencial do esquema.

O script garante o volume mínimo de dados exigido: gerou 50 tuplas exatas para as tabelas principais do sistema (como `USUARIO`, `RECURSO`, `RESERVA`) e pelo menos 15 tuplas consistentes para as tabelas de domínio secundárias (como `DEPARTAMENTO`, `PENALIDADE`, `MANUTENCAO`). Ao final da execução, o script compila todos os `INSERTs` no arquivo `02-insert-data.sql`, que é injetado diretamente no banco de dados durante a montagem do contêiner Docker.

## Gatilho (Trigger) Implementado
O arquivo [`init-scripts/04-create-triggers.sql`](init-scripts/04-create-triggers.sql) cria três gatilhos no MySQL que, juntos, automatizam todo o ciclo de vida de uso de um recurso reservado. Uma nova tabela de auditoria, `HISTORICO_STATUS_RESERVA`, foi criada em [`init-scripts/01-create-tables.sql`](init-scripts/01-create-tables.sql) para suportar o gatilho de auditoria.

| Gatilho | Evento | Regra de negócio automatizada |
|---|---|---|
| `trg_historico_status_reserva` | `AFTER UPDATE ON RESERVA` | Sempre que o `status_aprovacao` de uma reserva muda (ex: de `Pendente` para `Aprovada`), grava automaticamente uma linha em `HISTORICO_STATUS_RESERVA` com status anterior, status novo, quem analisou e o instante da mudança — garantindo **auditoria/rastreabilidade** das decisões tomadas sobre as reservas. |
| `trg_recurso_reservado_ao_aprovar` | `AFTER UPDATE ON RESERVA` | Quando uma reserva passa a `Aprovada`, todos os recursos vinculados a ela (via `RECURSO_RESERVA`) têm seu `status_atual` alterado automaticamente para `Reservado`, impedindo que continuem marcados como `Disponível`. |
| `trg_recurso_disponivel_ao_devolver` | `AFTER UPDATE ON RECURSO_RESERVA` | Quando a devolução de um recurso é registrada (`data_hora_devolucao` deixa de ser `NULL`), o recurso volta automaticamente para `status_atual = 'Disponível'`, liberando-o para novas reservas. |

### Como testar o gatilho
**Opção 1 — pela interface (recomendado):**
1. Acesse `http://localhost:3000`, vá em **Nova Reserva** e solicite uma reserva escolhendo um recurso `Disponível`.
2. No **Dashboard**, clique no ícone verde (✓) para **Aprovar** a reserva criada. O recurso escolhido passa automaticamente para `Reservado` — confira em **Recursos**.
3. Ainda no Dashboard, na mesma linha da reserva aprovada, clique no ícone de devolução (↩) para simular a devolução do recurso. O recurso volta automaticamente para `Disponível`.
4. Acesse a aba **Relatórios** → tabela **"Auditoria de Alterações de Reservas"**: nela aparecerá o registro criado automaticamente pelo `trg_historico_status_reserva` com o status anterior e o novo status da reserva.

**Opção 2 — via SQL direto:**
```sql
-- Conecte-se ao container do banco: docker exec -it ufape_mysql_db mysql -uroot -proot ufape_reserva_db

-- 1) Aprovar uma reserva pendente (dispara os gatilhos 1 e 2)
UPDATE RESERVA SET status_aprovacao = 'Aprovada', id_aprovador = 1 WHERE id_reserva = 1;
SELECT * FROM HISTORICO_STATUS_RESERVA WHERE id_reserva = 1;  -- linha inserida automaticamente
SELECT * FROM RECURSO r JOIN RECURSO_RESERVA rr ON r.id_recurso = rr.id_recurso WHERE rr.id_reserva = 1; -- status = 'Reservado'

-- 2) Registrar a devolução (dispara o gatilho 3)
UPDATE RECURSO_RESERVA SET data_hora_devolucao = NOW() WHERE id_reserva = 1;
SELECT status_atual FROM RECURSO WHERE id_recurso = <id_do_recurso>; -- volta para 'Disponível'
```

## Gerador de Relatórios
A aba **Relatórios** do frontend consome novas consultas SQL complexas (agregações com `JOIN`, `GROUP BY` e funções agregadas) e Views dedicadas, expostas pelo novo router `backend/routers/relatorios.py`:

| Relatório | Origem | Endpoint |
|---|---|---|
| Resumo de reservas por status | Consulta agregada (`GROUP BY status_aprovacao`) | `GET /api/relatorios/resumo-status` |
| Ranking de uso dos recursos | View `vw_uso_recursos` | `GET /api/relatorios/uso-recursos` |
| Ocupação de reservas por departamento | View `vw_ocupacao_departamentos` | `GET /api/relatorios/ocupacao-departamentos` |
| Auditoria de alterações de status (evidência do gatilho) | View `vw_historico_status_reservas` | `GET /api/relatorios/auditoria-status` |

Cada tabela é apresentada de forma organizada na interface e conta com um botão **"Exportar CSV"**, que gera o download do relatório correspondente diretamente no navegador.

## Correções em Relação à Entrega Anterior
- **Frontend sem estilo (CSS incompleto):** o arquivo `frontend/styles.css` da entrega anterior não definia diversas classes já utilizadas em `index.html`/`app.js` (`glass-panel`, `stats-grid`, `nav-item`, `data-table`, `skeleton`, `btn-primary`, `btn-outline`, `btn-icon`, entre outras), fazendo com que grande parte do layout fosse renderizada sem estilo algum. O arquivo foi reescrito para cobrir todas as classes usadas pela interface, restaurando o tema visual planejado (sidebar, cards de estatísticas, tabelas e modais).
- **View `vw_historico_reservas` incompleta:** a view não expunha o `id_recurso`, o que impedia identificar de forma programática qual recurso pertencia a qual linha da tabela de histórico. Esse campo foi adicionado, permitindo agora o registro de devolução de recursos diretamente pelo Dashboard.