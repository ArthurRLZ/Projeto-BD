import os
import random
from faker import Faker

# Configurando o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

# Define que o arquivo SQL será salvo diretamente na pasta init-scripts
caminho_arquivo = os.path.join('init-scripts', '02-insert-data.sql')

with open(caminho_arquivo, 'w', encoding='utf-8') as f:
    f.write("-- Arquivo de Povoamento Gerado Automaticamente (Faker)\n\n")

    # 1. Gerando 15 DEPARTAMENTOS (Tabela Secundária)
    f.write("-- 1. Povoando DEPARTAMENTO\n")
    f.write("INSERT INTO DEPARTAMENTO (nome, sigla) VALUES\n")
    
    departamentos = [
        "Ciência da Computação", "Engenharia de Software", "Medicina Veterinária",
        "Agronomia", "Engenharia de Alimentos", "Zootecnia",
        "Matemática Discreta e Aplicada", "Pedagogia", "História", "Geografia",
        "Física", "Química", "Ciências Biológicas", "Administração", "Direito"
    ]
    siglas = ["BCC", "BES", "BMV", "BAG", "BEA", "BZT", "BMA", "BPE", "BHI", "BGE", "BFI", "BQU", "BCB", "BAD", "BDI"]
    
    for i in range(15):
        terminador = ";" if i == 14 else ","
        f.write(f"('{departamentos[i]}', '{siglas[i]}'){terminador}\n")
    f.write("\n")

    # 2. Gerando 50 USUÁRIOS (Tabela Principal)
    f.write("-- 2. Povoando USUARIO\n")
    f.write("INSERT INTO USUARIO (matricula_siape, email, primeiro_nome, sobrenome, data_nascimento, tipo_perfil, id_departamento) VALUES\n")
    
    perfis = ['Aluno', 'Professor', 'Técnico', 'Admin']
    
    for i in range(50):
        matricula = fake.unique.random_number(digits=7, fix_len=True)
        email = fake.unique.company_email()
        nome = fake.first_name()
        sobrenome = fake.last_name()
        data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d')
        perfil = random.choice(perfis)
        id_dep = random.randint(1, 15) # Sorteia um departamento de 1 a 15
        
        terminador = ";" if i == 49 else ","
        f.write(f"('{matricula}', '{email}', '{nome}', '{sobrenome}', '{data_nasc}', '{perfil}', {id_dep}){terminador}\n")
    f.write("\n")

# 3. Gerando 50 TELEFONES (Tabela Secundária)
    f.write("-- 3. Povoando TELEFONE_USUARIO\n")
    f.write("INSERT INTO TELEFONE_USUARIO (numero, tipo, id_usuario) VALUES\n")
    
    tipos_tel = ['Celular', 'Fixo', 'WhatsApp', 'Comercial']
    
    for i in range(50):
        numero = fake.cellphone_number()
        tipo = random.choice(tipos_tel)
        id_user = i + 1 # Mapeia sequencialmente para os 50 usuários criados
        terminador = ";" if i == 49 else ","
        f.write(f"('{numero}', '{tipo}', {id_user}){terminador}\n")
    f.write("\n")

    # 4. Gerando 30 RECURSOS (Tabela Principal)
    f.write("-- 4. Povoando RECURSO\n")
    f.write("INSERT INTO RECURSO (nome, status_atual) VALUES\n")
    
    status_recurso = ['Disponível', 'Em Manutenção', 'Inativo', 'Reservado']
    recursos_nomes = []
    
    # 15 Nomes para Espaços
    for i in range(1, 16):
        recursos_nomes.append(f"Laboratório de Informática {i}")
    # 15 Nomes para Equipamentos
    for i in range(1, 16):
        recursos_nomes.append(f"Projetor Multimídia {i}")
        
    for i in range(30):
        status = random.choice(status_recurso)
        terminador = ";" if i == 29 else ","
        f.write(f"('{recursos_nomes[i]}', '{status}'){terminador}\n")
    f.write("\n")

    # 5. Gerando 15 ESPAÇOS (Especialização de Recurso)
    f.write("-- 5. Povoando ESPACO\n")
    f.write("INSERT INTO ESPACO (id_recurso, capacidade_pessoas, possui_arcondicionado, loc_predio, loc_andar, loc_sala) VALUES\n")
    
    predios = ['Prédio Principal UFAPE', 'Prédio de Laboratórios', 'Prédio do CTI']
    
    for i in range(15):
        id_rec = i + 1 # Os primeiros 15 IDs de Recursos correspondem aos Espaços
        capacidade = random.randint(15, 60)
        ar = random.choice(['TRUE', 'FALSE'])
        predio = random.choice(predios)
        andar = f"{random.randint(1, 4)}º Andar"
        sala = f"Sala {random.randint(101, 410)}"
        terminador = ";" if i == 14 else ","
        f.write(f"({id_rec}, {capacidade}, {ar}, '{predio}', '{andar}', '{sala}'){terminador}\n")
    f.write("\n")

    # 6. Gerando 15 EQUIPAMENTOS (Especialização de Recurso)
    f.write("-- 6. Povoando EQUIPAMENTO\n")
    f.write("INSERT INTO EQUIPAMENTO (id_recurso, marca, numero_patrimonio, voltagem, id_espaco_fixo) VALUES\n")
    
    marcas = ['Dell', 'Epson', 'Sony', 'HP', 'Lenovo']
    
    for i in range(15):
        id_rec = i + 16 # Do ID 16 ao 30 correspondem aos Equipamentos
        marca = random.choice(marcas)
        patrimonio = f"PAT-{fake.unique.random_number(digits=6, fix_len=True)}"
        voltagem = random.choice(['110V', '220V', 'Bivolt'])
        id_espaco = random.randint(1, 15) # Define que o equipamento fica guardado em um dos 15 espaços
        terminador = ";" if i == 14 else ","
        f.write(f"({id_rec}, '{marca}', '{patrimonio}', '{voltagem}', {id_espaco}){terminador}\n")
    f.write("\n")

# 7. Gerando 15 SEMESTRES (Tabela Secundária)
    f.write("-- 7. Povoando SEMESTRE_LETIVO\n")
    f.write("INSERT INTO SEMESTRE_LETIVO (ano, periodo, data_inicio_aulas, data_fim_aulas) VALUES\n")
    
    for i in range(15):
        ano = 2018 + (i // 2)
        periodo = (i % 2) + 1
        mes_inicio = "02" if periodo == 1 else "08"
        mes_fim = "06" if periodo == 1 else "12"
        terminador = ";" if i == 14 else ","
        f.write(f"({ano}, {periodo}, '{ano}-{mes_inicio}-01', '{ano}-{mes_fim}-15'){terminador}\n")
    f.write("\n")

    # 8. Gerando 15 DISCIPLINAS (Tabela Secundária)
    f.write("-- 8. Povoando DISCIPLINA\n")
    f.write("INSERT INTO DISCIPLINA (codigo_oficial, nome, id_departamento) VALUES\n")
    
    disciplinas = [
        "Banco de Dados I", "Engenharia de Software", "Programação Orientada a Objetos",
        "Redes de Computadores", "Sistemas Operacionais", "Matemática Discreta",
        "Cálculo I", "Física I", "Algoritmos e Estruturas de Dados",
        "Computação Gráfica", "Inteligência Artificial", "Arquitetura de Computadores",
        "Interação Humano-Computador", "Desenvolvimento Web", "Segurança da Informação"
    ]
    
    for i in range(15):
        codigo = f"BCC{fake.unique.random_number(digits=4, fix_len=True)}"
        nome_disc = disciplinas[i]
        id_dep = random.randint(1, 15)
        terminador = ";" if i == 14 else ","
        f.write(f"('{codigo}', '{nome_disc}', {id_dep}){terminador}\n")
    f.write("\n")

    # 9. Gerando 50 RESERVAS (Tabela Principal)
    f.write("-- 9. Povoando RESERVA\n")
    f.write("INSERT INTO RESERVA (data_reserva, hora_inicio, hora_fim, qtd_participantes_previstos, finalidade, status_aprovacao, data_hora_analise, justificativa_analise, id_solicitante, id_aprovador, id_semestre, id_disciplina) VALUES\n")
    
    status_opcoes = ['Aprovada', 'Pendente', 'Rejeitada']
    
    for i in range(50):
        data_res = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        hora_ini = f"{random.randint(8, 18):02d}:00:00"
        hora_fim = f"{random.randint(19, 22):02d}:00:00"
        qtd = random.randint(5, 50)
        finalidade = random.choice(['Aula prática', 'Palestra', 'Defesa de TCC', 'Reunião de colegiado', 'Grupo de estudos'])
        status = random.choice(status_opcoes)
        
        id_solic = random.randint(1, 50)
        id_aprov = random.randint(1, 50) if status != 'Pendente' else 'NULL'
        data_analise = f"'{data_res} 09:00:00'" if status != 'Pendente' else 'NULL'
        justificativa = "'Tudo certo.'" if status == 'Aprovada' else ("'Conflito de horário.'" if status == 'Rejeitada' else 'NULL')
        id_sem = random.randint(1, 15)
        id_disc = random.randint(1, 15)
        
        terminador = ";" if i == 49 else ","
        f.write(f"('{data_res}', '{hora_ini}', '{hora_fim}', {qtd}, '{finalidade}', '{status}', {data_analise}, {justificativa}, {id_solic}, {id_aprov}, {id_sem}, {id_disc}){terminador}\n")
    f.write("\n")

    # 10. Gerando 50 RECURSO_RESERVA (Associativa N:N - Tabela Principal)
    f.write("-- 10. Povoando RECURSO_RESERVA\n")
    f.write("INSERT INTO RECURSO_RESERVA (id_reserva, id_recurso, data_hora_retirada, data_hora_devolucao, observacao_avaria) VALUES\n")
    
    for i in range(50):
        id_reserva = i + 1
        id_recurso = random.randint(1, 30)
        data_base = fake.date_this_year().strftime('%Y-%m-%d')
        data_retirada = f"'{data_base} 08:00:00'"
        data_devol = f"'{data_base} 10:00:00'"
        obs = "'Nenhuma avaria'" if random.random() > 0.2 else "'Entregue com arranhões leves'"
        
        terminador = ";" if i == 49 else ","
        f.write(f"({id_reserva}, {id_recurso}, {data_retirada}, {data_devol}, {obs}){terminador}\n")
    f.write("\n")

    # 11. Gerando 15 MANUTENCOES (Tabela Secundária)
    f.write("-- 11. Povoando MANUTENCAO\n")
    f.write("INSERT INTO MANUTENCAO (id_recurso, data_hora_inicio, data_hora_fim, tipo_manutencao, descricao_servico, custo) VALUES\n")
    
    for i in range(15):
        id_rec = random.randint(16, 30) # Focado em equipamentos
        data_ini = fake.date_this_year().strftime('%Y-%m-%d')
        tipo = random.choice(['Preventiva', 'Corretiva'])
        desc = random.choice(['Troca de peça', 'Limpeza interna', 'Formatação', 'Reparo na fonte'])
        custo = round(random.uniform(50.0, 500.0), 2)
        
        terminador = ";" if i == 14 else ","
        f.write(f"({id_rec}, '{data_ini} 08:00:00', '{data_ini} 17:00:00', '{tipo}', '{desc}', {custo}){terminador}\n")
    f.write("\n")

    # 12. Gerando 15 PENALIDADES (Tabela Secundária)
    f.write("-- 12. Povoando PENALIDADE\n")
    f.write("INSERT INTO PENALIDADE (id_usuario, id_reserva, motivo, data_inicio, data_fim_suspensao) VALUES\n")
    
    for i in range(15):
        id_user = random.randint(1, 50)
        id_res = random.randint(1, 50)
        motivo = random.choice(['Atraso grave na devolução', 'Dano ao equipamento', 'Uso indevido do espaço', 'Não comparecimento'])
        data_ini = fake.date_this_year().strftime('%Y-%m-%d')
        
        terminador = ";" if i == 14 else ","
        f.write(f"({id_user}, {id_res}, '{motivo}', '{data_ini}', '{data_ini}'){terminador}\n")

print("✅ Sucesso Absoluto! Arquivo 02-insert-data.sql finalizado com todas as 12 tabelas preenchidas!")