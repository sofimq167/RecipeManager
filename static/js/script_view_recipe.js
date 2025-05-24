document.addEventListener('DOMContentLoaded', function () {
    const chartElement = document.getElementById('macroChart');

    if (!chartElement) return;

    const totalProtein = parseFloat(chartElement.dataset.protein);
    const totalCarbs = parseFloat(chartElement.dataset.carbs);
    const totalFat = parseFloat(chartElement.dataset.fat);

    const totalCalories = (totalProtein * 4) + (totalCarbs * 4) + (totalFat * 9);

    new Chart(chartElement.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Proteína', 'Carbs', 'Grasas'],
            datasets: [{
                data: [
                    (totalProtein * 4).toFixed(2),
                    (totalCarbs * 4).toFixed(2),
                    (totalFat * 9).toFixed(2)
                ],
                backgroundColor: [
                    '#E52020',
                    '#FE5D26',
                    '#F5E8C7'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = parseFloat(context.raw);
                            const percentage = ((value / totalCalories) * 100).toFixed(1);
                            return `${label}: ${value} kcal (${percentage}%)`;
                        }
                    }
                },
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: `${Math.round(totalCalories)} Kcal`
                }
            }
        }
    });
});
