// Загружаем JSON файл
fetch('../data/parce_rbc.json')
    .then(response => response.json())
    .then(jsonData => {
        const data = jsonData.data;  // Извлекаем данные из ключа 'data'

        // Преобразуем данные из файла в формат, который требуется для графика
        const chartData = {
            datasets: [{
                label: 'Data from JSON',
                data: data.map(item => ({
                    x: item.norm_sum,
                    y: item.total_reactions
                })),
                pointBackgroundColor: 'blue',
                pointBorderColor: 'blue'
            }]
        };

        const ctx = document.getElementById('myChart');

        new Chart(ctx, {
            type: 'scatter',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Chart.js Scatter Chart'
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error("Error loading JSON data:", error);
    });
