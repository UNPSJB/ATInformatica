var chart;

function init_chart(){
    var blue = "rgba(54, 162, 255, 0.5)"
    var blue_line = "rgba(23, 45, 68, 1)"

    chart = new Chart($("#chart-ots-clientes"), {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'La plata señore',
                data: [],
                backgroundColor: blue,
                borderColor: blue_line,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}