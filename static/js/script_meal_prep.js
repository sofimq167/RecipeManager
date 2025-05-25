// static/js/script_meal_prep.js

document.addEventListener('DOMContentLoaded', function() {
    const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
    
    // Configuración global
    const globalDesayuno = document.getElementById('globalDesayuno');
    const globalAlmuerzo = document.getElementById('globalAlmuerzo');
    const globalCena = document.getElementById('globalCena');
    const globalSnackCount = document.getElementById('globalSnackCount');
    const applyGlobalBtn = document.getElementById('applyGlobalConfig');
    
    // Función para agregar una nueva receta a un momento específico
    function addRecipeToMoment(day, moment) {
        const container = document.querySelector(`.${moment}-container[data-day="${day}"] .recipes-list`);
        const recipeCount = container.children.length;
        
        const recipeDiv = document.createElement('div');
        recipeDiv.className = 'recipe-item mb-2';
        recipeDiv.innerHTML = `
            <div class="input-group input-group-sm">
                <select class="form-select" name="${day}_${moment}[]">
                    <option value="">-- Seleccionar --</option>
                    ${getRecipeOptions()}
                </select>
                <button type="button" class="btn btn-outline-danger btn-sm remove-recipe">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(recipeDiv);
        
        // Agregar evento para eliminar receta
        recipeDiv.querySelector('.remove-recipe').addEventListener('click', function() {
            recipeDiv.remove();
        });
    }
    
    // Función para obtener las opciones de recetas (necesitas pasarlas desde el template)
    function getRecipeOptions() {
        const firstSelect = document.querySelector('select[name$="_desayuno[]"]');
        if (firstSelect) {
            return firstSelect.innerHTML;
        }
        return '';
    }
    
    // Función para mostrar/ocultar contenedores de comidas por día
    function toggleMealContainer(day, mealType, show) {
        const container = document.querySelector(`.${mealType}-container[data-day="${day}"]`);
        if (container) {
            if (show) {
                container.classList.remove('d-none');
            } else {
                container.classList.add('d-none');
                // Limpiar selecciones cuando se oculta
                const selects = container.querySelectorAll('select');
                selects.forEach(select => select.value = '');
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
        
        // Configurar botones "Agregar receta"
        const moments = ['desayuno', 'snack1', 'snack2', 'snack3', 'almuerzo', 'cena'];
        moments.forEach(moment => {
            const addBtn = document.querySelector(`[data-day="${day}"][data-moment="${moment}"]`);
            if (addBtn) {
                addBtn.addEventListener('click', function() {
                    addRecipeToMoment(day, moment);
                });
            }
        });
        
        // Configurar eventos de eliminación de recetas existentes
        const removeButtons = document.querySelectorAll(`[data-day="${day}"] .remove-recipe`);
        removeButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                btn.closest('.recipe-item').remove();
            });
        });
        
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
        const allSelects = form.querySelectorAll('select[name$="[]"]');
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