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
function showCat(event)
{
    var newCategoryForm = document.getElementById('new-category-form');
    if (newCategoryForm.style.display === 'none') {
        newCategoryForm.style.display = 'block';
    } else {
        newCategoryForm.style.display = 'none';
    }
    return false;
}
function editReceita(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) {
        // Preenche os campos do formulário com os valores da despesa
        document.getElementById('receita_id').value = id;
        document.getElementById('descricao').value = row.cells[0].textContent.trim();
        document.getElementById('valor').value = parseFloat(row.cells[1].textContent.replace('R$', '').replace(',', '.').trim());
        document.getElementById('data_receita').value = row.cells[3].textContent.split('/').reverse().join('-');
        document.getElementById('categoria').value = row.cells[4].dataset.idCategoria;

        const status = row.cells[2].textContent.trim() === 'Receita Recebida';
        const checkbox = document.getElementById('efetuada-checkbox');
        checkbox.checked = status;
        checkbox.value = status ? 'efetuada' : 'nao_efetuada';

        const toggleText = document.getElementById('toggle-text');
        toggleText.textContent = status ? 'Receita Recebida' : 'Receita Recorrente';
    }
}

function deleteReceita(id) {
    if (confirm('Tem certeza que deseja excluir esta receita?')) {
        const formData = new FormData();
        formData.append('acao', 'deletar');
        formData.append('receita_id', idReceita);

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (response.status === 200) {
                location.reload();
            }
        })
        .catch(error => console.error('Erro:', error));
    }
}