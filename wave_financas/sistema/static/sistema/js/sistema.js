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
// Função para editar uma meta
function editarMeta(metaId) {
    // Seleciona o cartão da meta a partir do ID
    const card = document.querySelector(`.btn-editar[data-id="${metaId}"]`).closest('.card-meta');

    // Extrai os dados existentes do cartão
    const descricao = card.querySelector('.card-title').innerText.trim();
    const observacao = card.querySelector('.collapse .mb-0').innerText.trim();
    const dataConclusao = card.querySelector('.card-text:nth-of-type(2)').innerText.replace('Data de Conclusão:', '').trim();
    const status = card.querySelector('.badge').innerText.trim() === 'Concluída';

    // Preenche os campos do formulário com os dados extraídos
    document.getElementById('descricao').value = descricao;
    document.getElementById('observacao').value = observacao;
    document.getElementById('data_conclusao').value = dataConclusao !== 'Não informada' ? dataConclusao.split('/').reverse().join('-') : '';
    document.getElementById('status').checked = status;

    // Adiciona um campo oculto ao formulário para identificar a meta sendo editada
    let inputId = document.querySelector('input[name="meta_id"]');
    if (!inputId) {
        inputId = document.createElement('input');
        inputId.type = 'hidden';
        inputId.name = 'meta_id';
        document.getElementById('meta-form').appendChild(inputId);
    }
    inputId.value = metaId;

    // Atualiza o texto do botão para indicar a ação de edição
    document.querySelector('#meta-form button[type="submit"]').innerText = 'Editar Meta';

    // Atualiza a ação do formulário para edição
    const form = document.getElementById('meta-form');
    form.action = '/sistema/cadastrar_meta/'; // Certifique-se de que esta seja a URL correta
    const inputEditar = document.createElement('input');
    inputEditar.type = 'hidden';
    inputEditar.name = 'editar_meta';
    form.appendChild(inputEditar);
}

// Função para excluir uma meta
function excluirMeta(metaId) {
    if (confirm('Tem certeza que deseja excluir esta meta?')) {
        const formData = new FormData();
        formData.append('meta_id', metaId);
        formData.append('excluir_meta', 'true'); // Marca como exclusão

        fetch('/sistema/gerenciar_meta/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove o cartão da meta
                const card = document.querySelector(`.btn-excluir[data-id="${metaId}"]`).closest('.card-meta');
                card.remove();
            } else {
                console.error('Erro ao excluir a meta:', data);
            }
        })
        .catch(error => console.error('Erro ao excluir a meta:', error));
    }
}
function editCliente(button) {
    const row = button.closest('tr');
    const form = document.getElementById('editFormCard');
    const fields = ['editNome', 'editContato', 'editCep', 'editCidade', 'editEstado', 'editBairro', 'editRua'];
    const values = Array.from(row.children).slice(0, -1).map(cell => cell.innerText);

    fields.forEach((field, i) => document.getElementById(field).value = values[i]);

    document.getElementById('editId').value = button.getAttribute('data-id');

    form.classList.remove('d-none');
    window.scrollTo({ top: form.offsetTop, behavior: 'smooth' });
}

function hideEditForm() {
    document.getElementById('editFormCard').classList.add('d-none');
}

async function filtrarNotas() {
    const filtroData = document.getElementById('filtro_data').value;
    const filtroClassificacao = document.getElementById('filtro_classificacao').value;

    const url = `/sistema/filtrar_notas/?filtro_data=${filtroData}&filtro_tipo=${filtroClassificacao}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
            atualizarNotas(data.notas);
        } else {
            console.error('Erro ao filtrar notas:', data.error);
        }
    } catch (error) {
        console.error('Erro ao realizar a requisição:', error);
    }
}

function atualizarNotas(notas) {
    const container = document.querySelector('.d-flex.overflow-auto');
    container.innerHTML = '';

    if (notas.length > 0) {
        notas.forEach(nota => {
            const card = `
                <div class="card text-white" style="min-width: 300px; background-color: #598392; border-radius: 10px;">
                    <div class="card-body">
                        <h5 class="card-title">${nota.descricao}</h5>
                        <p class="card-text"><strong>Classificação:</strong> ${nota.tipo}</p>
                        <p class="card-text"><strong>Data de Cadastro:</strong> ${nota.data_cadastro}</p>
                        <a href="/sistema/baixar_nota/${nota.id_nota}" class="btn btn-sm btn-secondary">Baixar Nota</a>
                    </div>
                </div>`;
            container.insertAdjacentHTML('beforeend', card);
        });
    } else {
        container.innerHTML = `<div class="text-center text-white">Nenhuma nota encontrada.</div>`;
    }
}

function limparFiltros() {
    document.getElementById('filtro_data').value = '';
    document.getElementById('filtro_classificacao').value = '';
    filtrarNotas();
}
