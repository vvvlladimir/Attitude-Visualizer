const ctx = document.getElementById('myChart');
const colors = ['blue', 'red', 'green', 'yellow'];
const maxLength = 50;

fetch('/list_files/')
    .then(response => response.json())
    .then(data => {
        const filenames = data.files;

        const dataPromises = filenames.map(filename =>
            fetch(`../data/${filename}`).then(response => response.json())
        );

        let promise = Promise.all(dataPromises)
            .then(allData => {
                // Создаем datasets для каждого файла
                const datasets = allData.map((dataObj, index) => ({
                        label: `Data from ${dataObj.tgID}`,  // Можно модифицировать, чтобы label был информативнее
                        data: dataObj.data.map(item => ({
                            x: item.norm_sum,
                            y: item.total_reactions,
                            datetime: item.pc_date,
                            label: item.pc_text.length > maxLength ? item.pc_text.slice(0, maxLength - 3) + '...' : item.pc_text,
                        })),
                        pointBackgroundColor: colors[index],
                        pointBorderColor: colors[index]
                    })
                );
                console.log(datasets)

                const chartData = {datasets};
                const options = {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: false,
                            text: 'Chart.js Scatter Chart'
                        },
                        tooltip: {
                            callbacks: {
                                title: function (contex) {
                                    console.log(contex[0].raw)
                                    return contex[0].raw.label
                                },
                                beforeBody: function (contex) {
                                    return contex[0].raw.datetime
                                },
                                label: function (tooltipItem) {
                                    return tooltipItem.yLabel;
                                }
                            }
                        }
                    }
                };



                new Chart(ctx, {
                    type: 'scatter',
                    data: chartData,
                    options: options,
                });
            })
            .catch(error => {
                console.error("Error fetching file list:", error);
            })
    })

