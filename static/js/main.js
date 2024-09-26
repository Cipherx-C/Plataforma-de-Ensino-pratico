// Obtendo os dados para o gráfico (valores fictícios, você pode passar esses dados do backend via JSON)
const projetosStatus = {
    labels: ['Pausado', 'Em Execução', 'Pronto'],
    datasets: [{
        label: 'Quantidade de Projetos',
        data: [3, 7, 2],  // Substituir por dados reais do backend
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
};

// Criando o gráfico
const ctx = document.getElementById('projectsChart').getContext('2d');
const projectsChart = new Chart(ctx, {
    type: 'doughnut',  // Você pode mudar o tipo de gráfico (bar, pie, line, etc.)
    data: projetosStatus,
});
