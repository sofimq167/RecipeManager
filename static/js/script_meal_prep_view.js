document.addEventListener('DOMContentLoaded', function() {
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
    prevBtn.addEventListener('click', function() {
        if (currentDayIndex > 0) {
            currentDayIndex--;
            updateDay();
        }
    });
    
    nextBtn.addEventListener('click', function() {
        if (currentDayIndex < days.length - 1) {
            currentDayIndex++;
            updateDay();
        }
    });
    
    // Navegación con teclado
    document.addEventListener('keydown', function(e) {
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
});