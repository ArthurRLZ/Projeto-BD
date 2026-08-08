# Projeto Banco de Dados — Transformação do Diagrama Conceitual (MERE) para o Esquema Lógico

## Integrantes do grupo
- [Nome completo 1]
- [Nome completo 2]
- [Nome completo 3]

## Contexto do Projeto
Este projeto implementa o mapeamento do Diagrama Conceitual (MERE), elaborado na etapa
anterior, para o Esquema Lógico Relacional, com a implementação física e povoamento do
banco de dados em ambiente de contêiner Docker.

**SGBD utilizado:** MySQL 8.0

**Dados de acesso ao banco:**
| Parâmetro       | Valor         |
|------------------|---------------|
| Host             | localhost     |
| Porta            | 3306          |
| Usuário          | admin         |
| Senha            | senha123      |
| Banco de Dados   | banco_aula    |

## Como executar o projeto

```bash
# Limpar volumes antigos (garante inicialização do zero)
docker compose down -v

# Subir o projeto (cria e popula o banco automaticamente)
docker compose up --build
```

Os scripts em `init-scripts/` são executados automaticamente pelo MySQL na primeira
inicialização do contêiner, na ordem:
1. `01-create-tables.sql` — criação das tabelas e índices (DDL)
2. `02-insert-data.sql` — povoamento das tabelas (DML)

## Estrutura do repositório

```
meu-projeto/
├── docker-compose.yml
├── README.md
├── init-scripts/
│   ├── 01-create-tables.sql
│   └── 02-insert-data.sql
└── docs/
    ├── diagrama-logico.png
    └── dicionario-de-dados.md
```

## Dicionário de Dados
> [Inserir aqui, tabela por tabela, a descrição, os tipos de dados, as restrições (constraints)
> e a semântica de cada atributo — ou referenciar o arquivo `docs/dicionario-de-dados.md` /
> um PDF anexado no repositório.]

## Normalização
> [Descrever brevemente como o esquema atende no mínimo à Segunda Forma Normal (2FN).]

## Metodologia de Povoamento
> [Explicar a estratégia utilizada para gerar e carregar o volume mínimo de dados exigido
> (mínimo 50 tuplas por tabela principal e 15 por tabela secundária): script DML manual,
> geração via ferramenta/script, consumo de API de terceiros, etc.]
