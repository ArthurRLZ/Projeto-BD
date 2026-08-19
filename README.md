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

Os scripts em `init-scripts/` são executados automaticamente pelo MySQL na primeira
inicialização do contêiner, na ordem:
1. `01-create-tables.sql` — criação das tabelas e índices (DDL)
2. `02-insert-data.sql` — povoamento das tabelas (DML)

## Estrutura do repositório


```text
PROJETO-BD/
├── docs/
│   ├── diagrama.pdf
│   └── dicionario-de-dados.md
├── init-scripts/
│   ├── 01-create-tables.sql
│   └── 02-insert-data.sql
├── scripts/
│   └── gerador_dados.py
├── .gitignore
├── docker-compose.yml
└── README.md
```

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