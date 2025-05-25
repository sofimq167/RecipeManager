document.addEventListener('DOMContentLoaded', function () {
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const dayNames = {
        'lunes': 'Lunes',
        'martes': 'Martes',
        'miercoles': 'Miércoles',
        'jueves': 'Jueves',
        'viernes': 'Viernes',
        'sabado': 'Sábado',
        'domingo': 'Domingo'
    };

    let currentDayIndex = 0;

    const prevBtn = document.getElementById('prevDay');
    const nextBtn = document.getElementById('nextDay');
    const dayTitle = document.getElementById('currentDayTitle');
    const dayCounter = document.getElementById('dayCounter');
    const dayPlans = document.querySelectorAll('.day-plan');

    function updateDay() {
        // Ocultar todos los días
        dayPlans.forEach(plan => plan.classList.add('d-none'));

        // Mostrar día actual
        const currentDay = days[currentDayIndex];
        const currentPlan = document.querySelector(`.day-plan[data-day="${currentDay}"]`);
        if (currentPlan) {
            currentPlan.classList.remove('d-none');
        }

        // Actualizar título y contador
        dayTitle.textContent = dayNames[currentDay];
        dayCounter.textContent = currentDayIndex + 1;

        // Habilitar/deshabilitar botones
        prevBtn.disabled = currentDayIndex === 0;
        nextBtn.disabled = currentDayIndex === days.length - 1;

        // Agregar clases CSS para botones deshabilitados
        if (currentDayIndex === 0) {
            prevBtn.classList.add('disabled');
        } else {
            prevBtn.classList.remove('disabled');
        }

        if (currentDayIndex === days.length - 1) {
            nextBtn.classList.add('disabled');
        } else {
            nextBtn.classList.remove('disabled');
        }
    }

    // Event listeners
    prevBtn.addEventListener('click', function () {
        if (currentDayIndex > 0) {
            currentDayIndex--;
            updateDay();
        }
    });

    nextBtn.addEventListener('click', function () {
        if (currentDayIndex < days.length - 1) {
            currentDayIndex++;
            updateDay();
        }
    });

    // Navegación con teclado
    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft' && currentDayIndex > 0) {
            currentDayIndex--;
            updateDay();
        } else if (e.key === 'ArrowRight' && currentDayIndex < days.length - 1) {
            currentDayIndex++;
            updateDay();
        }
    });

    // Inicializar
    updateDay();

    document.querySelectorAll('canvas[id^="macroChart_"]').forEach(chartElement => {
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
                    backgroundColor: ['#E52020', '#FE5D26', '#F5E8C7'],
                    borderWidth: 1
                }]
            },
            options: {
                cutout: '75%',
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
                        display: false
                    }
                }
            },
            plugins: [{
                id: 'centerText',
                beforeDraw(chart) {
                    const { width, height, ctx } = chart;
                    ctx.restore();
                    const fontSize = (height / 150).toFixed(2);
                    ctx.font = `${fontSize}em sans-serif`;
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = '#333';

                    const text = `${Math.round(totalCalories)} kcal`;
                    const textX = Math.round((width - ctx.measureText(text).width) / 2);
                    const textY = height / 2;

                    ctx.fillText(text, textX, textY);
                    ctx.save();
                }
            }]
        });
    });

    const weeklyChartEl = document.getElementById('weeklyMacroChart');
    if (weeklyChartEl) {
        const proteinValues = weeklyChartEl.dataset.protein.split(',').map(Number);
        const carbsValues = weeklyChartEl.dataset.carbs.split(',').map(Number);
        const fatValues = weeklyChartEl.dataset.fat.split(',').map(Number);

        const labels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

        new Chart(weeklyChartEl.getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Proteína (g)',
                        data: proteinValues,
                        borderColor: '#E52020',
                        tension: 0.4,
                        fill: false
                    },
                    {
                        label: 'Carbs (g)',
                        data: carbsValues,
                        borderColor: '#FE5D26',
                        tension: 0.4,
                        fill: false
                    },
                    {
                        label: 'Grasas (g)',
                        data: fatValues,
                        borderColor: '#F5E8C7',
                        tension: 0.4,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.dataset.label}: ${context.parsed.y.toFixed(1)}g`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Gramos'
                        }
                    }
                    
                }
            }
        });
    }


});

