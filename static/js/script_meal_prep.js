// static/js/script_meal_prep.js

document.addEventListener('DOMContentLoaded', function() {
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    
    // Configuración global
    const globalDesayuno = document.getElementById('globalDesayuno');
    const globalAlmuerzo = document.getElementById('globalAlmuerzo');
    const globalCena = document.getElementById('globalCena');
    const globalSnackCount = document.getElementById('globalSnackCount');
    const applyGlobalBtn = document.getElementById('applyGlobalConfig');
    
    // Función para mostrar/ocultar contenedores de comidas por día
    function toggleMealContainer(day, mealType, show) {
        const container = document.querySelector(`.${mealType}-container[data-day="${day}"]`);
        if (container) {
            if (show) {
                container.classList.remove('d-none');
            } else {
                container.classList.add('d-none');
                // Limpiar selección cuando se oculta
                const select = container.querySelector('select');
                if (select) select.value = '';
            }
        }
    }
    
    // Función para actualizar snacks por día
    function updateDaySnacks(day) {
        const snackSelect = document.getElementById(`${day}_snackCount`);
        const count = parseInt(snackSelect.value);
        
        // Mostrar/ocultar snacks basado en la cantidad
        toggleMealContainer(day, 'snack1', count >= 1);
        toggleMealContainer(day, 'snack2', count >= 2);
        toggleMealContainer(day, 'snack3', count >= 3);
    }
    
    // Función para configurar eventos de un día específico
    function setupDayEvents(day) {
        // Checkboxes de comidas principales
        const desayunoCheck = document.getElementById(`${day}_includeDesayuno`);
        const almuerzoCheck = document.getElementById(`${day}_includeAlmuerzo`);
        const cenaCheck = document.getElementById(`${day}_includeCena`);
        const snackSelect = document.getElementById(`${day}_snackCount`);
        
        if (desayunoCheck) {
            desayunoCheck.addEventListener('change', function() {
                toggleMealContainer(day, 'desayuno', this.checked);
            });
        }
        
        if (almuerzoCheck) {
            almuerzoCheck.addEventListener('change', function() {
                toggleMealContainer(day, 'almuerzo', this.checked);
            });
        }
        
        if (cenaCheck) {
            cenaCheck.addEventListener('change', function() {
                toggleMealContainer(day, 'cena', this.checked);
            });
        }
        
        if (snackSelect) {
            snackSelect.addEventListener('change', function() {
                updateDaySnacks(day);
            });
        }
        
        // Inicializar estado del día
        updateDaySnacks(day);
    }
    
    // Configurar eventos para todos los días
    days.forEach(day => {
        setupDayEvents(day);
    });
    
    // Aplicar configuración global a todos los días
    applyGlobalBtn.addEventListener('click', function() {
        const globalDesayunoValue = globalDesayuno.checked;
        const globalAlmuerzoValue = globalAlmuerzo.checked;
        const globalCenaValue = globalCena.checked;
        const globalSnackValue = globalSnackCount.value;
        
        days.forEach(day => {
            // Aplicar checkboxes
            const desayunoCheck = document.getElementById(`${day}_includeDesayuno`);
            const almuerzoCheck = document.getElementById(`${day}_includeAlmuerzo`);
            const cenaCheck = document.getElementById(`${day}_includeCena`);
            const snackSelect = document.getElementById(`${day}_snackCount`);
            
            if (desayunoCheck) {
                desayunoCheck.checked = globalDesayunoValue;
                toggleMealContainer(day, 'desayuno', globalDesayunoValue);
            }
            
            if (almuerzoCheck) {
                almuerzoCheck.checked = globalAlmuerzoValue;
                toggleMealContainer(day, 'almuerzo', globalAlmuerzoValue);
            }
            
            if (cenaCheck) {
                cenaCheck.checked = globalCenaValue;
                toggleMealContainer(day, 'cena', globalCenaValue);
            }
            
            if (snackSelect) {
                snackSelect.value = globalSnackValue;
                updateDaySnacks(day);
            }
        });
        
        // Mostrar mensaje de confirmación
        const originalText = applyGlobalBtn.innerHTML;
        applyGlobalBtn.innerHTML = '<i class="fas fa-check"></i> ¡Aplicado!';
        applyGlobalBtn.classList.add('btn-success');
        applyGlobalBtn.classList.remove('btn-outline-primary');
        
        setTimeout(() => {
            applyGlobalBtn.innerHTML = originalText;
            applyGlobalBtn.classList.remove('btn-success');
            applyGlobalBtn.classList.add('btn-outline-primary');
        }, 2000);
    });
    
    // Validación del formulario
    const form = document.getElementById('mealPrepForm');
    form.addEventListener('submit', function(e) {
        const name = document.getElementById('name').value.trim();
        
        if (!name) {
            e.preventDefault();
            alert('Por favor, ingresa un nombre para el meal prep.');
            return false;
        }
        
        // Verificar que al menos se haya seleccionado una receta
        const allSelects = form.querySelectorAll('select[name$="_desayuno"], select[name$="_snack1"], select[name$="_snack2"], select[name$="_snack3"], select[name$="_almuerzo"], select[name$="_cena"]');
        let hasSelection = false;
        
        allSelects.forEach(select => {
            // Solo verificar selects que están visibles
            const container = select.closest('.col-md-2');
            if (container && !container.classList.contains('d-none') && select.value) {
                hasSelection = true;
            }
        });
        
        if (!hasSelection) {
            e.preventDefault();
            alert('Por favor, selecciona al menos una receta para tu meal prep.');
            return false;
        }
        
        // Mostrar resumen antes de enviar
        if (confirm('¿Estás seguro de que quieres crear este meal prep con la configuración actual?')) {
            return true;
        } else {
            e.preventDefault();
            return false;
        }
    });
});

// Función para copiar configuración de un día específico a otros días
function copyDayConfig(sourceDay) {
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    const targetDays = days.filter(day => day !== sourceDay);
    
    if (confirm(`¿Copiar la configuración de ${sourceDay.charAt(0).toUpperCase() + sourceDay.slice(1)} a los demás días?`)) {
        // Obtener configuración del día origen
        const sourceDesayuno = document.getElementById(`${sourceDay}_includeDesayuno`).checked;
        const sourceAlmuerzo = document.getElementById(`${sourceDay}_includeAlmuerzo`).checked;
        const sourceCena = document.getElementById(`${sourceDay}_includeCena`).checked;
        const sourceSnacks = document.getElementById(`${sourceDay}_snackCount`).value;
        
        // Obtener selecciones de recetas
        const sourceSelections = {};
        ['desayuno', 'snack1', 'snack2', 'snack3', 'almuerzo', 'cena'].forEach(meal => {
            const select = document.querySelector(`select[name="${sourceDay}_${meal}"]`);
            if (select) {
                sourceSelections[meal] = select.value;
            }
        });
        
        // Aplicar a días destino
        targetDays.forEach(day => {
            // Configuración de checkboxes y snacks
            document.getElementById(`${day}_includeDesayuno`).checked = sourceDesayuno;
            document.getElementById(`${day}_includeAlmuerzo`).checked = sourceAlmuerzo;
            document.getElementById(`${day}_includeCena`).checked = sourceCena;
            document.getElementById(`${day}_snackCount`).value = sourceSnacks;
            
            // Aplicar cambios visuales
            toggleMealContainer(day, 'desayuno', sourceDesayuno);
            toggleMealContainer(day, 'almuerzo', sourceAlmuerzo);
            toggleMealContainer(day, 'cena', sourceCena);
            updateDaySnacks(day);
            
            // Copiar selecciones de recetas
            Object.keys(sourceSelections).forEach(meal => {
                const targetSelect = document.querySelector(`select[name="${day}_${meal}"]`);
                if (targetSelect && sourceSelections[meal]) {
                    targetSelect.value = sourceSelections[meal];
                }
            });
        });
    }
}

// Función auxiliar para toggle de contenedores (para uso externo)
function toggleMealContainer(day, mealType, show) {
    const container = document.querySelector(`.${mealType}-container[data-day="${day}"]`);
    if (container) {
        if (show) {
            container.classList.remove('d-none');
        } else {
            container.classList.add('d-none');
            const select = container.querySelector('select');
            if (select) select.value = '';
        }
    }
}

// Función auxiliar para actualizar snacks (para uso externo)
function updateDaySnacks(day) {
    const snackSelect = document.getElementById(`${day}_snackCount`);
    if (snackSelect) {
        const count = parseInt(snackSelect.value);
        toggleMealContainer(day, 'snack1', count >= 1);
        toggleMealContainer(day, 'snack2', count >= 2);
        toggleMealContainer(day, 'snack3', count >= 3);
    }
}