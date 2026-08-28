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
        'disciplinas': 'Gestão de Disciplinas',
        'penalidades': 'Painel de Penalidades',
        'aulas': 'Cronograma de Aulas',
        'relatorios': 'Gerador de Relatórios'
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
            else if(targetId === 'disciplinas') carregarDisciplinas();
            else if(targetId === 'penalidades') carregarPenalidades();
            else if(targetId === 'aulas') carregarAulas();
            else if(targetId === 'reservas') carregarOpcoesNovaReserva();
            else if(targetId === 'relatorios') carregarRelatorios();
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
                } else if(reserva.status_aprovacao === 'Aprovada' && !reserva.data_hora_devolucao) {
                    acoes = `
                        <button class="btn btn-icon" title="Registrar Devolução" style="color:var(--info)" onclick="registrarDevolucao(${reserva.id_reserva}, ${reserva.id_recurso})"><i class="ph ph-arrow-u-down-left"></i></button>
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
    window.carregarRecursos = async function () {
        const tabela = document.getElementById('tabela-gestao-recursos');
        try {
            const resposta = await fetch(`${getBaseUrl()}/recursos`);
            const recursos = await resposta.json();
            tabela.innerHTML = '';
            if (recursos.length === 0) {
                tabela.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhum recurso cadastrado.</td></tr>`;
                return;
            }
            recursos.forEach(rec => {
                let badgeClass = rec.status_atual === 'Disponível' ? 'badge-success' : 'badge-danger';
                tabela.innerHTML += `
                    <tr>
                        <td>#${rec.id_recurso}</td>
                        <td>${rec.nome}</td>
                        <td><span class="badge ${badgeClass}">${rec.status_atual}</span></td>
                        <td>
                            <button class="btn btn-icon" title="Editar" onclick='abrirModal("recurso", ${JSON.stringify(rec)})'><i class="ph ph-pencil-simple"></i></button>
                            <button class="btn btn-icon btn-danger" title="Excluir" onclick="excluirItem('recurso', ${rec.id_recurso})"><i class="ph ph-trash"></i></button>
                        </td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="4">Erro ao carregar recursos.</td></tr>`;
        }
    }

    // busca a lista de usuarios
    window.carregarUsuarios = async function () {
        const tabela = document.getElementById('tabela-gestao-usuarios');
        try {
            const resposta = await fetch(`${getBaseUrl()}/usuarios`);
            const usuarios = await resposta.json();
            tabela.innerHTML = '';
            if (usuarios.length === 0) {
                tabela.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhum usuário cadastrado.</td></tr>`;
                return;
            }
            usuarios.forEach(usr => {
                tabela.innerHTML += `
                    <tr>
                        <td>${usr.primeiro_nome} ${usr.sobrenome}</td>
                        <td>${usr.email}</td>
                        <td>${usr.tipo_perfil}</td>
                        <td>
                            <button class="btn btn-icon" title="Editar" onclick='abrirModal("usuario", ${JSON.stringify(usr)})'><i class="ph ph-pencil-simple"></i></button>
                            <button class="btn btn-icon btn-danger" title="Excluir" onclick="excluirItem('usuario', ${usr.id_usuario})"><i class="ph ph-trash"></i></button>
                        </td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="4">Erro ao carregar usuários.</td></tr>`;
        }
    }

    // busca a lista de disciplinas
    window.carregarDisciplinas = async function () {
        const tabela = document.getElementById('tabela-gestao-disciplinas');
        try {
            const resposta = await fetch(`${getBaseUrl()}/disciplinas`);
            const disciplinas = await resposta.json();
            tabela.innerHTML = '';
            if (disciplinas.length === 0) {
                tabela.innerHTML = `<tr><td colspan="4" style="text-align:center;">Nenhuma disciplina cadastrada.</td></tr>`;
                return;
            }
            disciplinas.forEach(disc => {
                tabela.innerHTML += `
                    <tr>
                        <td>${disc.codigo_oficial}</td>
                        <td>${disc.nome}</td>
                        <td>${disc.id_departamento}</td>
                        <td>
                            <button class="btn btn-icon" title="Editar" onclick='abrirModal("disciplina", ${JSON.stringify(disc)})'><i class="ph ph-pencil-simple"></i></button>
                            <button class="btn btn-icon btn-danger" title="Excluir" onclick="excluirItem('disciplina', ${disc.id_disciplina})"><i class="ph ph-trash"></i></button>
                        </td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="4">Erro ao carregar disciplinas.</td></tr>`;
        }
    }

    // ================== MODAL GENÉRICO DE CRIAR/EDITAR ==================

    // define os campos de formulario para cada tipo de entidade
    const configEntidades = {
        recurso: {
            titulo: 'Recurso',
            endpoint: 'recursos',
            idField: 'id_recurso',
            campos: [
                { name: 'nome', label: 'Nome', type: 'text' },
                { name: 'status_atual', label: 'Status Atual', type: 'select', options: ['Disponível', 'Reservado', 'Em Manutenção', 'Inativo'] }
            ]
        },
        usuario: {
            titulo: 'Usuário',
            endpoint: 'usuarios',
            idField: 'id_usuario',
            campos: [
                { name: 'primeiro_nome', label: 'Primeiro Nome', type: 'text' },
                { name: 'sobrenome', label: 'Sobrenome', type: 'text' },
                { name: 'email', label: 'Email', type: 'text' },
                { name: 'tipo_perfil', label: 'Perfil', type: 'select', options: ['Aluno', 'Professor', 'Técnico', 'Admin'] },
                { name: 'id_departamento', label: 'ID do Departamento', type: 'number' }
            ]
        },
        disciplina: {
            titulo: 'Disciplina',
            endpoint: 'disciplinas',
            idField: 'id_disciplina',
            campos: [
                { name: 'codigo_oficial', label: 'Código Oficial', type: 'text' },
                { name: 'nome', label: 'Nome', type: 'text' },
                { name: 'id_departamento', label: 'ID do Departamento', type: 'number' }
            ]
        }
    };

    let modalTipoAtual = null;
    let modalIdAtual = null;

    // abre o modal, em modo criacao (sem 'item') ou edicao (com 'item')
    window.abrirModal = function (tipo, item) {
        const config = configEntidades[tipo];
        modalTipoAtual = tipo;
        modalIdAtual = item ? item[config.idField] : null;

        document.getElementById('modal-titulo').textContent = (item ? 'Editar ' : 'Novo(a) ') + config.titulo;

        const camposHtml = config.campos.map(campo => {
            const valorAtual = item ? (item[campo.name] ?? '') : '';
            if (campo.type === 'select') {
                const opcoes = campo.options.map(op =>
                    `<option value="${op}" ${op === valorAtual ? 'selected' : ''}>${op}</option>`
                ).join('');
                return `
                    <div class="form-group">
                        <label>${campo.label}</label>
                        <select id="modal-campo-${campo.name}">${opcoes}</select>
                    </div>`;
            }
            return `
                <div class="form-group">
                    <label>${campo.label}</label>
                    <input type="${campo.type}" id="modal-campo-${campo.name}" value="${valorAtual}">
                </div>`;
        }).join('');

        document.getElementById('modal-campos').innerHTML = camposHtml;
        document.getElementById('modal-overlay').classList.add('active');
    };

    window.fecharModal = function () {
        document.getElementById('modal-overlay').classList.remove('active');
        modalTipoAtual = null;
        modalIdAtual = null;
    };

    // le os campos do form, monta o payload e salva (create ou update)
    window.salvarModal = async function () {
        const config = configEntidades[modalTipoAtual];
        const payload = {};
        config.campos.forEach(campo => {
            let valor = document.getElementById(`modal-campo-${campo.name}`).value;
            if (campo.type === 'number') valor = parseInt(valor) || null;
            payload[campo.name] = valor;
        });

        const editando = !!modalIdAtual;
        const url = editando
            ? `${getBaseUrl()}/${config.endpoint}/${modalIdAtual}`
            : `${getBaseUrl()}/${config.endpoint}/`;

        try {
            const resposta = await fetch(url, {
                method: editando ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const dados = await resposta.json();
            if (!resposta.ok) throw new Error(dados.detail || 'Erro ao salvar.');

            fecharModal();
            if (modalTipoAtual === 'recurso') carregarRecursos();
            else if (modalTipoAtual === 'usuario') carregarUsuarios();
            else if (modalTipoAtual === 'disciplina') carregarDisciplinas();
        } catch (erro) {
            alert(erro.message);
        }
    };

    // exclui um registro de qualquer uma das 3 entidades
    window.excluirItem = async function (tipo, id) {
        const config = configEntidades[tipo];
        if (!confirm(`Tem certeza que deseja excluir este(a) ${config.titulo.toLowerCase()}?`)) return;

        try {
            const resposta = await fetch(`${getBaseUrl()}/${config.endpoint}/${id}`, { method: 'DELETE' });
            const dados = await resposta.json();
            if (!resposta.ok) throw new Error(dados.detail || 'Erro ao excluir.');

            if (tipo === 'recurso') carregarRecursos();
            else if (tipo === 'usuario') carregarUsuarios();
            else if (tipo === 'disciplina') carregarDisciplinas();
        } catch (erro) {
            alert(erro.message);
        }
    };

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
                        <td>${pen.usuario_punido}</td>
                        <td>${pen.departamento}</td>
                        <td>${pen.motivo}</td>
                        <td>${pen.reserva_origem}</td>
                        <td>${window.formatarDataBr(pen.data_fim_suspensao)}</td>
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

    // registra a devolução de um recurso (aciona o gatilho trg_recurso_disponivel_ao_devolver)
    window.registrarDevolucao = async function(id_reserva, id_recurso) {
        if(!confirm(`Confirmar a devolução do recurso da reserva #${id_reserva}?\nO recurso será liberado automaticamente pelo gatilho do banco de dados.`)) return;

        try {
            const resposta = await fetch(`${getBaseUrl()}/reservas/${id_reserva}/recursos/${id_recurso}/devolucao`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ observacao_avaria: null })
            });
            const dados = await resposta.json();
            if(!resposta.ok) throw new Error(dados.detail || 'Erro ao registrar devolução.');
            alert(dados.mensagem);
            carregarReservas();
        } catch(erro) {
            alert(erro.message);
        }
    };

    // ================== GERADOR DE RELATÓRIOS ==================

    // guarda em cache o último resultado de cada relatório para permitir exportação em CSV
    const cacheRelatorios = {};

    async function carregarRelatorios() {
        await Promise.all([
            carregarResumoStatus(),
            carregarUsoRecursos(),
            carregarOcupacaoDepartamentos(),
            carregarAuditoriaStatus()
        ]);
    }

    async function carregarResumoStatus() {
        try {
            const resposta = await fetch(`${getBaseUrl()}/relatorios/resumo-status`);
            const dados = await resposta.json();
            const totais = { 'Aprovada': 0, 'Pendente': 0, 'Rejeitada': 0 };
            dados.forEach(item => { totais[item.status_aprovacao] = item.total; });
            document.getElementById('stat-aprovadas').textContent = totais['Aprovada'];
            document.getElementById('stat-pendentes').textContent = totais['Pendente'];
            document.getElementById('stat-rejeitadas').textContent = totais['Rejeitada'];
        } catch (erro) {
            console.error('Erro ao carregar resumo de status:', erro);
        }
    }

    async function carregarUsoRecursos() {
        const tabela = document.getElementById('tabela-uso-recursos');
        try {
            const resposta = await fetch(`${getBaseUrl()}/relatorios/uso-recursos`);
            const dados = await resposta.json();
            cacheRelatorios['uso-recursos'] = dados;
            tabela.innerHTML = '';
            if (dados.length === 0) {
                tabela.innerHTML = `<tr><td colspan="5" style="text-align:center;">Nenhum dado disponível.</td></tr>`;
                return;
            }
            dados.forEach(item => {
                const badgeClass = item.status_atual === 'Disponível' ? 'badge-success' : 'badge-danger';
                tabela.innerHTML += `
                    <tr>
                        <td>${item.nome_recurso}</td>
                        <td><span class="badge ${badgeClass}">${item.status_atual}</span></td>
                        <td>${item.total_reservas}</td>
                        <td>${item.total_aprovadas}</td>
                        <td>${item.total_horas_reservadas ?? 0}h</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="5" style="color:var(--danger); text-align:center;">Erro ao carregar relatório.</td></tr>`;
        }
    }

    async function carregarOcupacaoDepartamentos() {
        const tabela = document.getElementById('tabela-ocupacao-departamentos');
        try {
            const resposta = await fetch(`${getBaseUrl()}/relatorios/ocupacao-departamentos`);
            const dados = await resposta.json();
            cacheRelatorios['ocupacao-departamentos'] = dados;
            tabela.innerHTML = '';
            if (dados.length === 0) {
                tabela.innerHTML = `<tr><td colspan="5" style="text-align:center;">Nenhum dado disponível.</td></tr>`;
                return;
            }
            dados.forEach(item => {
                tabela.innerHTML += `
                    <tr>
                        <td>${item.nome_departamento} (${item.sigla})</td>
                        <td>${item.total_reservas}</td>
                        <td>${item.total_aprovadas}</td>
                        <td>${item.total_pendentes}</td>
                        <td>${item.total_rejeitadas}</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="5" style="color:var(--danger); text-align:center;">Erro ao carregar relatório.</td></tr>`;
        }
    }

    async function carregarAuditoriaStatus() {
        const tabela = document.getElementById('tabela-auditoria-status');
        try {
            const resposta = await fetch(`${getBaseUrl()}/relatorios/auditoria-status`);
            const dados = await resposta.json();
            cacheRelatorios['auditoria-status'] = dados;
            tabela.innerHTML = '';
            if (dados.length === 0) {
                tabela.innerHTML = `<tr><td colspan="6" style="text-align:center;">Nenhuma alteração registrada ainda. Aprove ou rejeite uma reserva para gerar um registro de auditoria.</td></tr>`;
                return;
            }
            dados.forEach(item => {
                tabela.innerHTML += `
                    <tr>
                        <td>#${item.id_reserva}</td>
                        <td>${item.solicitante}</td>
                        <td>${item.status_anterior ?? '-'}</td>
                        <td>${item.status_novo}</td>
                        <td>${item.alterado_por ?? '-'}</td>
                        <td>${new Date(item.data_alteracao).toLocaleString('pt-BR')}</td>
                    </tr>`;
            });
        } catch (erro) {
            tabela.innerHTML = `<tr><td colspan="6" style="color:var(--danger); text-align:center;">Erro ao carregar relatório.</td></tr>`;
        }
    }

    // converte o resultado em cache do relatório para CSV e dispara o download
    window.exportarRelatorioCSV = function (chave) {
        const dados = cacheRelatorios[chave];
        if (!dados || dados.length === 0) {
            alert('Não há dados para exportar.');
            return;
        }
        const colunas = Object.keys(dados[0]);
        const linhas = [colunas.join(';')];
        dados.forEach(item => {
            linhas.push(colunas.map(col => `"${String(item[col] ?? '').replace(/"/g, '""')}"`).join(';'));
        });
        const csv = linhas.join('\n');
        const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `relatorio-${chave}-${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    // Inicia carregando o dashboard
    carregarReservas();
});