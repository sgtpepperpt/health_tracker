const generate_weight_chart = (target, data) => {
    const config = {
        type: 'line',
        data: {
            datasets: [{
                data: data
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time'
                },
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    }

    new Chart($(target), config)
}

const generate_masses_chart = (target, weight, fat, muscle) => {
    const config = {
        type: 'line',
        data: {
            datasets: [{
                label: 'Fat mass',
                backgroundColor: 'blue',
                data: fat
            }, {
                label: 'Weight',
                backgroundColor: 'grey',
                data: weight
            }, {
                label: 'Muscle mass',
                backgroundColor: 'red',
                data: muscle
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time'
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Mass (kg)'
                    }
                },
            }
        }
    }

    new Chart($(target), config)
}
