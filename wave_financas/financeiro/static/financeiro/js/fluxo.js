function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    var timeString = hours + ':' + minutes + ':' + seconds;

    document.getElementById('clock').textContent = timeString;
}

function showSubMenu(id)
{
    var subMenu = document.getElementById(id);
    if (subMenu.style.display === "block") {
        subMenu.style.display = "none";
    } else {
        subMenu.style.display = "block";
    }
}

function hideContainers()
{
    const cardsContainer = document.querySelector('.cards-container');
    const dashboardContainer = document.querySelector('.dashboard-container');

    if (cardsContainer) {
        cardsContainer.style.display = 'none';
    }

    if (dashboardContainer) {
        dashboardContainer.style.display = 'none';
    }
}

async function fetchFinanceData() {
    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


        const receitasRes = await fetch('/financeiro/total_receitas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });
        const receitas = await receitasRes.json();

        const despesasRes = await fetch('/financeiro/total_despesas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });
        const despesas = await despesasRes.json();

        const saldoRes = await fetch('/financeiro/saldo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });
        const saldo = await saldoRes.json();

        // Atualizando as informações na página
        document.getElementById('receitas_').textContent = 'R$ ' + receitas.total_receitas || '0';
        document.getElementById('despesas_').textContent = 'R$ ' + despesas.total_despesas || '0';
        document.getElementById('saldo_').textContent = 'R$ ' + saldo.saldo || '0';

    } catch (error) {
        console.error('Erro ao carregar os dados financeiros:', error);
    }
}
function hideContainers()
{
    const cardsContainer = document.querySelector('.card-deck');
    const dashboardContainer = document.querySelector('.dashboard-container');

    if (cardsContainer) {
        cardsContainer.style.display = 'none';
    }

    if (dashboardContainer) {
        dashboardContainer.style.display = 'none';
    }
}

function carregarProjetos(csrfToken) {
    fetch('/financeiro/gestao_projetos/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('projetos-table-body');
            tableBody.innerHTML = '';

            if (data.projetos.length > 0) {
                data.projetos.forEach(projeto => {
                    const row = `
                        <tr>
                            <td>${projeto.id_projeto}</td>
                            <td>${projeto.nome_projeto}</td>
                            <td>${projeto.observacao}</td>
                            <td>${projeto.valor_cobrado}</td>
                            <td>${projeto.valor_gasto || 'Não informado'}</td>
                            <td>${projeto.data_inicio}</td>
                            <td>${projeto.data_fim || 'Não informado'}</td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary" onclick='editarProjeto(${JSON.stringify(projeto)})'>Editar</button>
                                <button class="btn btn-sm btn-outline-danger" onclick="excluirProjeto(${projeto.id_projeto}, '${csrfToken}')">Excluir</button>
                            </td>
                        </tr>`;
                    tableBody.insertAdjacentHTML('beforeend', row);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="8">Nenhum projeto encontrado.</td></tr>';
            }
        });
}

function editarProjeto(projeto) {
    document.getElementById('id_projeto').value = projeto.id_projeto;
    document.getElementById('nome_projeto').value = projeto.nome_projeto;
    document.getElementById('observacao').value = projeto.observacao;
    document.getElementById('valor_cobrado').value = projeto.valor_cobrado;
    document.getElementById('valor_gasto').value = projeto.valor_gasto || '';
    document.getElementById('data_inicio').value = projeto.data_inicio;
    document.getElementById('data_fim').value = projeto.data_fim || '';
    document.getElementById('id_cliente').value = projeto.id_cliente || '';
}

function excluirProjeto(id, csrfToken) {
    if (confirm('Tem certeza que deseja excluir este projeto?')) {
        fetch('/financeiro/gestao_projetos/', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Projeto excluído com sucesso!');
                carregarProjetos(csrfToken);
            } else {
                alert('Erro ao excluir o projeto.');
            }
        });
    }
}

function carregarAtivos(csrfToken) {
    fetch('/financeiro/gestao_ativos/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('ativos-container');
            container.innerHTML = '';

            if (data.ativos.length > 0) {
                data.ativos.forEach(ativo => {
                    const card = `
                        <div class="card" style="background-color: #343333; width: 350px;">
                            <h5 class="card-title">${ativo.descricao}</h5>
                            <p><strong>Valor Investido:</strong> R$${ativo.valor_investido}</p>
                            <p><strong>Valor Retorno:</strong> ${ativo.valor_retorno ? 'R$' + ativo.valor_retorno : 'Não informado'}</p>
                            <p><strong>Data Investimento:</strong> ${ativo.data_investimento}</p>
                            <p><strong>Data Retorno:</strong> ${ativo.data_retorno || 'Não informado'}</p>
                            <div class="card-actions">
                                <button class="btn btn-primary" onclick='editarAtivo(${JSON.stringify(ativo)})'>Editar</button>
                                <button class="btn btn-danger" onclick="excluirAtivo(${ativo.id_ativo}, '${csrfToken}')">Excluir</button>
                            </div>
                        </div>`;
                    container.insertAdjacentHTML('beforeend', card);
                });
            } else {
                container.innerHTML = '<div class="text-center text-white">Nenhum ativo encontrado.</div>';
            }
        });
}

function editarAtivo(ativo) {
    document.getElementById('id_ativo').value = ativo.id_ativo;
    document.getElementById('descricao').value = ativo.descricao;
    document.getElementById('valor_investido').value = ativo.valor_investido;
    document.getElementById('valor_retorno').value = ativo.valor_retorno || '';
    document.getElementById('data_investimento').value = ativo.data_investimento;
    document.getElementById('data_retorno').value = ativo.data_retorno || '';
}

function excluirAtivo(id, csrftoken) {
    if (confirm('Tem certeza que deseja excluir este ativo?')) {
        fetch('/financeiro/gestao_ativos/', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_ativo: id }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.success || 'Ativo excluído com sucesso!');
            })
            .catch(() => alert('Erro ao excluir ativo.'));
    }
}

function carregarDayTrade(csrfToken) {
    fetch('/financeiro/gestao_daytrade/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('daytrade-stats');
            container.innerHTML = '';

            if (data.daytrade.length > 0) {
                data.daytrade.forEach(entry => {
                    const lucroClass = entry.lucro_liquido > 0 ? 'text-success' : 'text-danger';

                    const card = `
                        <div class="col-lg-6 col-md-8 mb-4">
                            <div class="card">
                                <div class="card-header">
                                    <span>DayTrade: ${new Date().toLocaleString('default', { month: 'long', year: 'numeric' })}</span>
                                    <button class="btn btn-sm btn-danger" onclick="excluirDayTrade(${entry.id_daytrade}, csrfToken)">
                                        Excluir
                                    </button>
                                </div>
                                <div class="card-body">
                                    <p><strong>Contratos:</strong> ${entry.contratos}</p>
                                    <p><strong>Caixa Atual:</strong> R$${entry.caixa_atual}</p>
                                    <p><strong>Gastos:</strong> R$${entry.gastos}</p>
                                    <p><strong>Lucro Líquido:</strong> <span class="${lucroClass}">R$${entry.lucro_liquido}</span></p>
                                    <div class="progress mb-3">
                                        <div
                                            class="progress-bar ${entry.lucro_liquido > 0 ? 'bg-success' : 'bg-danger'}"
                                            role="progressbar"
                                            style="width: ${Math.abs(entry.lucro_liquido) / (entry.caixa_atual || 1) * 100}%">
                                        </div>
                                    </div>
                                    <button class="btn btn-sm" style="background-color: #2D7997; color: white;"  onclick='editarDayTrade(${JSON.stringify(entry)})'>Editar</button>
                                </div>
                            </div>
                        </div>`;
                    container.insertAdjacentHTML('beforeend', card);
                });
            } else {
                container.innerHTML = '<div class="text-center text-white">Nenhum dado encontrado.</div>';
            }
        });
}


function editarDayTrade(dayTrade) {
    document.getElementById('id_daytrade').value = dayTrade.id_daytrade;
    document.getElementById('contratos').value = dayTrade.contratos;
    document.getElementById('caixa_atual').value = dayTrade.caixa_atual;
    document.getElementById('gastos').value = dayTrade.gastos;
    document.getElementById('lucro_liquido').value = dayTrade.lucro_liquido;
}

function excluirDayTrade(id, csrfToken) {
    if (confirm('Tem certeza que deseja excluir este registro de DayTrade?')) {
        fetch('/financeiro/gestao_daytrade/', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_daytrade: id }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.success || 'Registro excluído com sucesso!');
                carregarDayTrade(csrfToken);
            })
            .catch(() => alert('Erro ao excluir registro.'));
    }
}

function carregarOperacoes(csrfToken) {
    fetch('/financeiro/gestao_observacoes_daytrade/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('operacoes-container');
            container.innerHTML = '';

            if (data.obs.length > 0) {
                // Separar operações por status
                const gainOps = data.obs.filter(op => op.status === 'gain');
                const lossOps = data.obs.filter(op => op.status === 'loss');

                // Renderizar os cards
                criarSecao('Gain', gainOps, 'success', container, csrfToken);
                criarSecao('Loss', lossOps, 'danger', container, csrfToken);
            } else {
                container.innerHTML = '<div class="text-center text-white">Nenhuma operação registrada.</div>';
            }
        });
}

function criarSecao(titulo, operacoes, cor, container, csrfToken) {
    if (operacoes.length > 0) {
        // Criar uma linha para os cards
        const secao = `
            <div class="mb-3">
                <h3 class="text-${cor}">${titulo}</h3>
                <div class="row flex-nowrap" id="row-${titulo.toLowerCase()}"></div>
            </div>`;
        container.insertAdjacentHTML('beforeend', secao);

        const row = document.getElementById(`row-${titulo.toLowerCase()}`);

        operacoes.forEach(op => {
            const card = `
                <div class="col-auto mb-4">
                    <div class="card border-${cor} shadow-lg" style="min-width: 300px; max-width: 300px;">
                        <div class="card-header bg-${cor} text-white d-flex justify-content-between align-items-center">
                            <h5>${op.status.toUpperCase()}</h5>
                            <small>${new Date(op.data_cadastro).toLocaleDateString()}</small>
                        </div>
                        <div class="card-body">
                            <p>${op.detalhe}</p>
                            <div class="d-flex justify-content-between">
                                <button class="btn btn-sm" style="background-color: #2D7997; color: white;" onclick='editarOperacao(${JSON.stringify(op)})'>Editar</button>
                                <button class="btn btn-danger btn-sm" onclick="excluirOperacao(${op.id_obs}, csrfToken)">Excluir</button>
                            </div>
                        </div>
                    </div>
                </div>`;
            row.insertAdjacentHTML('beforeend', card);
        });
    }
}


function editarOperacao(op) {
    document.getElementById('id_obs').value = op.id_obs;
    document.getElementById('detalhe').value = op.detalhe;
    document.getElementById('status').value = op.status;
}

function excluirOperacao(id, csrfToken) {
    if (confirm('Tem certeza que deseja excluir esta operação?')) {
        fetch('/financeiro/gestao_observacoes_daytrade/', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_obs: id }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.success || 'Operação excluída com sucesso!');
                carregarOperacoes(csrfToken);
            })
            .catch(() => alert('Erro ao excluir operação.'));
    }
}