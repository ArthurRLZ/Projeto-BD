document.addEventListener('DOMContentLoaded', () => {
    // pega os elementos
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.view-section');
    const pageTitle = document.getElementById('page-title');

    const viewTitles = {
        'dashboard': 'Visão Geral',
        'reservas': 'Nova Reserva',
        'recursos': 'Gestão de Recursos',
        'usuarios': 'Gestão de Usuários',
        'penalidades': 'Painel de Penalidades',
        'aulas': 'Cronograma de Aulas'
    };

    const getBaseUrl = () => window.location.hostname === 'localhost' ? 'http://localhost:8000/api' : '/api';

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(sec => sec.classList.remove('active'));
            
            item.classList.add('active');
            
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
            
            pageTitle.textContent = viewTitles[targetId];
            
            // chama a funcao baseada na aba
            if(targetId === 'dashboard') carregarReservas();
            else if(targetId === 'recursos') carregarRecursos();
            else if(targetId === 'usuarios') carregarUsuarios();
            else if(targetId === 'penalidades') carregarPenalidades();
            else if(targetId === 'aulas') carregarAulas();
            else if(targetId === 'reservas') carregarOpcoesNovaReserva();
        });
    });

    // formata a data pro brasil
    window.formatarDataBr = (dataString) => {
        if(!dataString) return '-';
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR');
    };

    // carrega dados das reservas na tabela do inicio
    async function carregarReservas() {
        const tabela = document.getElementById('tabela-reservas');
        try {
            const resposta = await fetch(`${getBaseUrl()}/historico-reservas`);
            if(!resposta.ok) throw new Error('Erro na API');
            const reservas = await resposta.json();
            tabela.innerHTML = '';
            
            if (reservas.length === 0) {
                tabela.innerHTML = `<tr><td colspan="6" style="text-align:center;">Nenhuma reserva encontrada.</td></tr>`;
                return;
            }

            reservas.forEach(reserva => {
                let badgeClass = 'badge-warning';
                if (reserva.status_aprovacao === 'Aprovada') badgeClass = 'badge-success';
                else if (reserva.status_aprovacao === 'Rejeitada') badgeClass = 'badge-danger';

                let acoes = '';
                if(reserva.status_aprovacao === 'Pendente') {
                    acoes = `
                        <button class="btn btn-icon" title="Aprovar" style="color:var(--success)" onclick="atualizarStatusReserva(${reserva.id_reserva}, 'Aprovada')"><i class="ph ph-check-circle"></i></button>
                        <button class="btn btn-icon" title="Rejeitar" style="color:var(--danger)" onclick="atualizarStatusReserva(${reserva.id_reserva}, 'Rejeitada')"><i class="ph ph-x-circle"></i></button>
                    `;
                }
                acoes += `<button class="btn btn-icon" title="Excluir" style="color:var(--danger)" onclick="deletarReserva(${reserva.id_reserva})"><i class="ph ph-trash"></i></button>`;

                tabela.innerHTML += `
                    <tr>
                        <td>
                            <div style="font-weight:500">${window.formatarDataBr(reserva.data_reserva)}</div>
                            <div style="font-size:0.75rem; color:var(--text-muted)">ID: #${reserva.id_reserva}</div>
                        </td>
                        <td>${reserva.nome_solicitante}</td>
                        <td>${reserva.nome_recurso}</td>
                        <td>${reserva.finalidade}</td>
                        <td><span class="badge ${badgeClass}">${reserva.status_aprovacao}</span></td>
                        <td><div style="display:flex; gap:4px;">${acoes}</div></td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="6" style="color:var(--danger); text-align:center;">Erro ao conectar com a API.</td></tr>`;
        }
    }

    // carrega os recursos disponiveis
    async function carregarRecursos() {
        const tabela = document.getElementById('tabela-gestao-recursos');
        try {
            const resposta = await fetch(`${getBaseUrl()}/recursos`);
            const recursos = await resposta.json();
            tabela.innerHTML = '';
            recursos.forEach(rec => {
                let badgeClass = rec.status_atual === 'Disponível' ? 'badge-success' : 'badge-danger';
                tabela.innerHTML += `
                    <tr>
                        <td>#${rec.id_recurso}</td>
                        <td>${rec.nome}</td>
                        <td><span class="badge ${badgeClass}">${rec.status_atual}</span></td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="3">Erro ao carregar recursos.</td></tr>`;
        }
    }

    // busca a lista de usuarios
    async function carregarUsuarios() {
        const tabela = document.getElementById('tabela-gestao-usuarios');
        try {
            const resposta = await fetch(`${getBaseUrl()}/usuarios`);
            const usuarios = await resposta.json();
            tabela.innerHTML = '';
            usuarios.forEach(usr => {
                tabela.innerHTML += `
                    <tr>
                        <td>${usr.primeiro_nome} ${usr.sobrenome}</td>
                        <td>${usr.email}</td>
                        <td>${usr.tipo_perfil}</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="3">Erro ao carregar usuários.</td></tr>`;
        }
    }

    // puxa relatorio penalidades
    async function carregarPenalidades() {
        const tabela = document.getElementById('tabela-gestao-penalidades');
        try {
            const resposta = await fetch(`${getBaseUrl()}/relatorio-penalidades`);
            const penalidades = await resposta.json();
            tabela.innerHTML = '';
            if(penalidades.length === 0) {
                tabela.innerHTML = `<tr><td colspan="5" style="text-align:center;">Nenhuma penalidade encontrada.</td></tr>`;
                return;
            }
            penalidades.forEach(pen => {
                tabela.innerHTML += `
                    <tr>
                        <td>${pen.nome_usuario}</td>
                        <td>${pen.departamento_nome}</td>
                        <td>${pen.motivo_penalidade}</td>
                        <td>Reserva #${pen.id_reserva}</td>
                        <td>${window.formatarDataBr(pen.data_fim)}</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="5">Erro ao carregar penalidades.</td></tr>`;
        }
    }

    // view de aulas
    async function carregarAulas() {
        const tabela = document.getElementById('tabela-aulas');
        try {
            const resposta = await fetch(`${getBaseUrl()}/detalhes-aulas`);
            const aulas = await resposta.json();
            tabela.innerHTML = '';
            if(aulas.length === 0) {
                tabela.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhuma aula agendada.</td></tr>`;
                return;
            }
            aulas.forEach(aula => {
                tabela.innerHTML += `
                    <tr>
                        <td>
                            <div style="font-weight:500">${window.formatarDataBr(aula.data_reserva)}</div>
                            <div style="font-size:0.8rem; color:var(--text-muted)">${aula.hora_inicio} - ${aula.hora_fim}</div>
                        </td>
                        <td>
                            <div style="font-weight:500">${aula.nome_disciplina}</div>
                            <div style="font-size:0.8rem; color:var(--text-muted)">${aula.codigo_oficial}</div>
                        </td>
                        <td>${aula.professor_responsavel}</td>
                        <td>${aula.ano}.${aula.periodo}</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="4">Erro ao carregar cronograma de aulas.</td></tr>`;
        }
    }

    // tela do forms de reserva
    async function carregarOpcoesNovaReserva() {
        try {
            // Carrega usuários
            const resUsuarios = await fetch(`${getBaseUrl()}/usuarios`);
            const usuarios = await resUsuarios.json();
            const selectSol = document.getElementById('id_solicitante');
            selectSol.innerHTML = '<option value="">Selecione quem está solicitando</option>';
            usuarios.forEach(usr => {
                selectSol.innerHTML += `<option value="${usr.id_usuario}">${usr.primeiro_nome} ${usr.sobrenome} (${usr.tipo_perfil})</option>`;
            });

            // Carrega recursos
            const resRecursos = await fetch(`${getBaseUrl()}/recursos`);
            const recursos = await resRecursos.json();
            const listaRecursos = document.getElementById('lista-recursos-checkbox');
            listaRecursos.innerHTML = '';
            recursos.forEach(rec => {
                const disabled = (rec.status_atual === 'Em Manutenção' || rec.status_atual === 'Inativo') ? 'disabled' : '';
                const cor = disabled ? 'color: var(--text-muted);' : 'color: var(--text-primary);';
                listaRecursos.innerHTML += `
                    <label style="display:flex; align-items:center; gap:8px; cursor:pointer; ${cor}">
                        <input type="checkbox" name="recurso" value="${rec.id_recurso}" ${disabled}>
                        ${rec.nome} - <span style="font-size:0.8rem; opacity:0.8;">${rec.status_atual}</span>
                    </label>
                `;
            });

        } catch (erro) {
            console.error(erro);
        }
    }

    window.enviarReserva = async function(event) {
        event.preventDefault();
        
        const alerta = document.getElementById('mensagem-alerta');
        alerta.style.display = 'none';

        // Coleta os checkboxes marcados
        const checkboxes = document.querySelectorAll('input[name="recurso"]:checked');
        const recursosSelecionados = Array.from(checkboxes).map(cb => parseInt(cb.value));

        if(recursosSelecionados.length === 0) {
            alerta.style.display = 'block';
            alerta.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
            alerta.style.color = '#ef4444';
            alerta.innerHTML = 'Você precisa selecionar pelo menos um recurso.';
            return;
        }

        const payload = {
            data_reserva: document.getElementById('data_reserva').value,
            hora_inicio: document.getElementById('hora_inicio').value + ":00",
            hora_fim: document.getElementById('hora_fim').value + ":00",
            finalidade: document.getElementById('finalidade').value,
            qtd_participantes_previstos: parseInt(document.getElementById('qtd_participantes').value) || 0,
            id_solicitante: parseInt(document.getElementById('id_solicitante').value),
            id_disciplina: null, // Para simplificar
            id_semestre: null,
            recursos: recursosSelecionados
        };

        try {
            const resposta = await fetch(`${getBaseUrl()}/reservas/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const dados = await resposta.json();

            if(!resposta.ok) {
                throw new Error(dados.detail || 'Erro desconhecido ao solicitar reserva.');
            }

            // Sucesso
            alerta.style.display = 'block';
            alerta.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
            alerta.style.color = '#10b981';
            alerta.innerHTML = `✅ ${dados.mensagem} (ID: #${dados.id_reserva})`;
            document.getElementById('form-reserva').reset();
            
        } catch(erro) {
            // Erro (Ex: Conflito de horário)
            alerta.style.display = 'block';
            alerta.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
            alerta.style.color = '#ef4444';
            alerta.innerHTML = `⚠️ ${erro.message}`;
        }
    }

    // funcoes crud
    window.atualizarStatusReserva = async function(id_reserva, status) {
        if(!confirm(`Deseja realmente marcar a reserva #${id_reserva} como ${status}?`)) return;
        
        try {
            const resposta = await fetch(`${getBaseUrl()}/reservas/${id_reserva}/aprovar`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    status_aprovacao: status,
                    justificativa_analise: "Análise via Painel",
                    id_aprovador: 1 // Admin fake
                })
            });
            if(!resposta.ok) throw new Error('Erro ao atualizar status');
            alert(`Reserva ${status} com sucesso!`);
            carregarReservas();
        } catch(erro) {
            alert(erro.message);
        }
    };

    window.deletarReserva = async function(id_reserva) {
        if(!confirm(`⚠️ Tem certeza que deseja excluir a reserva #${id_reserva} do banco de dados?\nEsta ação não pode ser desfeita.`)) return;
        
        try {
            const resposta = await fetch(`${getBaseUrl()}/reservas/${id_reserva}`, {
                method: 'DELETE'
            });
            if(!resposta.ok) throw new Error('Falha ao excluir reserva. Ela pode estar vinculada a uma penalidade.');
            alert(`Reserva #${id_reserva} apagada com sucesso!`);
            carregarReservas();
        } catch(erro) {
            alert(erro.message);
        }
    };

    // Inicia carregando o dashboard
    carregarReservas();
});
