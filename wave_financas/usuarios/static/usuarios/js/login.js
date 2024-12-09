document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const messageElement = document.getElementById('message');

    try {
        const response = await fetch('/usuarios/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ email, senha })
        });

        const result = await response.json();

        if (response.ok) {
            messageElement.innerText = result.mensagem;
            messageElement.style.color = '#64B5F6';
            setTimeout(() => {
                window.location.href = '/financeiro/fluxo_financeiro/';
            }, 1000);
        } else {
            messageElement.innerText = result.erro || 'Erro ao fazer login.';
            messageElement.style.color = 'red';
        }
    } catch (error) {
        //
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho'],
            datasets: [{
                label: 'Wave FinTech',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                data: [65, 59, 80, 81, 56, 55, 40]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    function updateChart() {
        chart.data.datasets.forEach((dataset) => {
            dataset.data.pop();
        });

        var newData = chart.data.datasets[0].data;
        var lastValue = newData[newData.length - 1];
        newData.push(lastValue + 4);
        newData.push(lastValue + 8);

        chart.update();
    }

    setInterval(updateChart, 1300);
});