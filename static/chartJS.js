const ctx = document.getElementById('myChart');
const colors = ['blue', 'red', 'green', 'black'];
const gradientColors = ['rgba(255, 87, 51, 0.16)', 'rgba(216, 8, 8, 0.00)'];
const gridColor = "rgba(33,33,33,0.22)";
const maxLength = 50;

const gradientBackgroundColor = {
    id: 'gradientBackgroundColor',
    beforeDraw(chart, args, plugins) {
        const {ctx, chartArea: {top, bottom, left, right, width, height}} = chart;

        ctx.save();

        const gradientBg = ctx.createLinearGradient(left, 0, width, 0);
        gradientBg.addColorStop(0, gradientColors[0]);
        gradientBg.addColorStop(1, gradientColors[1]);

        ctx.fillStyle = gradientBg;
        ctx.fillRect(left, top, width, height);
    }
}
const optionsBubble = {
    responsive: true,
    scales: {
        x: {
            ticks: {
                display: false
            },
            grid: {
                color: gridColor
            }
        },
        y: {
            grid: {
                color: gridColor
            }
        }
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                font: {
                    weight: "bold"
                }
            }
        },

        title: {
            display: false,
            text: 'Chart.js Scatter Chart'
        },
        tooltip: {
            callbacks: {
                title: function (contex) {
                    const contexLabel = contex[0].raw.label.replace(/\n/g, "");
                    return contexLabel.length > maxLength ? contexLabel.slice(0, maxLength - 3) + '...' : contexLabel;
                },
                beforeBody: function (contex) {
                    return "Post Date: " + contex[0].raw.datetime.slice(0, 10);
                },
                label: function (tooltipItem) {
                    const coordX = parseFloat(tooltipItem.parsed.x);
                    let minValue = tooltipItem.dataset.normSumMin;
                    let maxValue = tooltipItem.dataset.normSumMax
                    const [labelValue] = valueTextColor(coordX, minValue, maxValue);
                    return "Reaction: " + labelValue;
                },
                labelTextColor: function (tooltipItem) {
                    const coordX = parseFloat(tooltipItem.parsed.x);
                    let minValue = tooltipItem.dataset.normSumMin;
                    let maxValue = tooltipItem.dataset.normSumMax
                    const [, colorValue] = valueTextColor(coordX, minValue, maxValue);
                    return colorValue;
                },
                beforeFooter: function (context) {
                    return context[0].raw.sum + " | " + context[0].raw.x.toFixed(3)
                }
            }
        },
    }
}

// Function to fetch data from a given URL and return it as JSON
async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch ${url}: ${response.statusText}`);
    }
    return await response.json();
}

// Fetch all file data based on the given filenames
async function fetchAllFilesData(filenames) {
    return await Promise.all(filenames.map(filename => fetchData(`../data/${filename}`)));
}

// Convert the fetched data into a format suitable for Chart.js
function createDatasets(allData) {
    return allData.map((dataObj, index) => ({
        label: `${dataObj.tgID}`,
        // Extract all telegram links from the data.
        tags: dataObj.data.map(item => item.tg_link),
        // Extract min and max norm_sum from the data.
        normSumMin: `${dataObj.norm_sum_min}`,
        normSumMax: `${dataObj.norm_sum_max}`,
        // Prepare the main data points for plotting.
        data: dataObj.data.map(item => ({
            x: item.norm_sum,
            y: item.total_reactions,
            datetime: item.pc_date,
            label: item.pc_text,
            sum: item.sum,
            emojis: item.emojis
        })),
        // Assign a color to each dataset.
        pointBorderColor: colors[index],
        // backgroundColor: colors[index]
    }));
}

// Function to determine the text and color based on a given value
function valueTextColor(value, minValue = -3, maxValue = 3) {
    if (value <= minValue - minValue * 0.3) return ["Realy Bad", "#de284f"];
    if (value <= minValue - minValue * 0.6) return ["Bad", "#d1546f"];
    if (value <= maxValue - maxValue * 0.6) return ["Normal", "#fff"];
    if (value <= maxValue - maxValue * 0.3) return ["Good", "#a5f29d"];
    if (value <= maxValue) return ["Awesome", "#4ef520"];
    return ["No way", "#fff"];
}

// Create and return a scatter chart
function createChart(ctx, chartData, type, options) {
    return new Chart(ctx, {
        type: type,
        data: chartData,
        // Chart configuration options.
        options: options,
        plugins: [gradientBackgroundColor]
    });
}

// main function to initialize the chart
async function init() {
    try {
        const {files: filenames} = await fetchData('/list_files/');
        const allData = await fetchAllFilesData(filenames);
        const datasets = createDatasets(allData);
        const chart = createChart(ctx, {datasets}, 'bubble', optionsBubble);

        // Add an event listener to handle click events on the chart.
        chart.canvas.onclick = (evt) => {
            const res = chart.getElementsAtEventForMode(evt, 'nearest', {intersect: true}, true);
            if (res.length === 0) return;
            const tg_link = chart.data.datasets[res[0].datasetIndex].tags[res[0].index];
            openInNewTab(tg_link);
        };
    } catch (error) {
        console.error("Error fetching file list:", error);
    }
}

// Helper function to open a given link in a new tab.
function openInNewTab(tg_link) {
    window.open(tg_link, "_blank");
}

// Call the main initialization function.
init();
