document.getElementById('loginform').addEventListener('submit', function(event) {
    event.preventDefault();

    let email = document.getElementById('email').value;
    let senha = document.getElementById('senha').value;

    let data = {
        email: email,
        senha: senha
    };

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensagem === "Login realizado") {
            window.location.href = '/dashboard'; // Redirecionar para o dashboard ou página inicial
        } else {
            document.getElementById('login-error').textContent = data.erro;
            document.getElementById('login-error').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho'],
            datasets: [{
                label: 'Wave Financas',
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