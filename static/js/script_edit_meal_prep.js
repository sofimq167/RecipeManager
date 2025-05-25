document.addEventListener('DOMContentLoaded', function() {
    const recipeOptionsHtml = document.querySelector('select[name$="[]"]').innerHTML;
    
    // Función para agregar nueva receta a un momento específico
    function addRecipeToMoment(day, moment) {
        const container = document.querySelector(`.${moment}-container[data-day="${day}"] .recipes-list`);
        
        const newRecipeItem = document.createElement('div');
        newRecipeItem.className = 'recipe-item mb-2';
        newRecipeItem.innerHTML = `
            <div class="d-flex">
                <select class="form-select form-select-sm me-2" name="${day}_${moment}[]">
                    ${recipeOptionsHtml}
                </select>
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeRecipeItem(this)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(newRecipeItem);
    }
    
    // Función global para remover item de receta (accessible desde el HTML)
    window.removeRecipeItem = function(button) {
        button.closest('.recipe-item').remove();
    };
    
    // Event listeners para botones de agregar receta
    document.querySelectorAll('button[data-day][data-moment]').forEach(button => {
        button.addEventListener('click', function() {
            const day = this.dataset.day;
            const moment = this.dataset.moment;
            addRecipeToMoment(day, moment);
        });
    });
    
    // Función para actualizar la visibilidad de snacks
    function updateSnackVisibility(day, snackCount) {
        const snack2Container = document.querySelector(`.snack2-container[data-day="${day}"]`);
        const snack3Container = document.querySelector(`.snack3-container[data-day="${day}"]`);
        
        // Ocultar todos los snacks primero
        snack2Container.classList.add('d-none');
        snack3Container.classList.add('d-none');
        
        // Limpiar selects de snacks que se ocultan
        if (snackCount < 2) {
            snack2Container.querySelectorAll('select').forEach(select => select.value = '');
        }
        if (snackCount < 3) {
            snack3Container.querySelectorAll('select').forEach(select => select.value = '');
        }
        
        // Mostrar snacks según la cantidad seleccionada
        if (snackCount >= 2) {
            snack2Container.classList.remove('d-none');
        }
        if (snackCount >= 3) {
            snack3Container.classList.remove('d-none');
        }
    }
    
    // Función para actualizar la visibilidad de las comidas principales
    function updateMealVisibility(day, mealType, isVisible) {
        const container = document.querySelector(`.${mealType}-container[data-day="${day}"]`);
        if (isVisible) {
            container.classList.remove('d-none');
        } else {
            container.classList.add('d-none');
            // Limpiar selects cuando se oculta la comida
            container.querySelectorAll('select').forEach(select => select.value = '');
        }
    }
    
    // Event listeners para checkboxes de comidas por día
    document.querySelectorAll('.day-desayuno, .day-almuerzo, .day-cena').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const day = this.id.split('_')[0];
            const mealType = this.classList.contains('day-desayuno') ? 'desayuno' :
                           this.classList.contains('day-almuerzo') ? 'almuerzo' : 'cena';
            
            updateMealVisibility(day, mealType, this.checked);
        });
    });
    
    // Event listeners para selectores de snacks por día
    document.querySelectorAll('.day-snacks').forEach(select => {
        select.addEventListener('change', function() {
            const day = this.id.split('_')[0];
            const snackCount = parseInt(this.value);
            updateSnackVisibility(day, snackCount);
        });
    });
    
    // Configuración global
    document.getElementById('applyGlobalConfig').addEventListener('click', function() {
        const globalDesayuno = document.getElementById('globalDesayuno').checked;
        const globalAlmuerzo = document.getElementById('globalAlmuerzo').checked;
        const globalCena = document.getElementById('globalCena').checked;
        const globalSnackCount = parseInt(document.getElementById('globalSnackCount').value);
        
        const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
        
        days.forEach(day => {
            // Actualizar checkboxes de comidas principales
            document.getElementById(`${day}_includeDesayuno`).checked = globalDesayuno;
            document.getElementById(`${day}_includeAlmuerzo`).checked = globalAlmuerzo;
            document.getElementById(`${day}_includeCena`).checked = globalCena;
            
            // Actualizar selector de snacks
            document.getElementById(`${day}_snackCount`).value = globalSnackCount;
            
            // Aplicar cambios de visibilidad
            updateMealVisibility(day, 'desayuno', globalDesayuno);
            updateMealVisibility(day, 'almuerzo', globalAlmuerzo);
            updateMealVisibility(day, 'cena', globalCena);
            updateSnackVisibility(day, globalSnackCount);
        });
    });
    
    // Inicializar la visibilidad basada en el estado actual
    function initializeVisibility() {
        const days = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'];
        
        days.forEach(day => {
            // Inicializar visibilidad de comidas principales
            const desayunoChecked = document.getElementById(`${day}_includeDesayuno`).checked;
            const almuerzoChecked = document.getElementById(`${day}_includeAlmuerzo`).checked;
            const cenaChecked = document.getElementById(`${day}_includeCena`).checked;
            
            updateMealVisibility(day, 'desayuno', desayunoChecked);
            updateMealVisibility(day, 'almuerzo', almuerzoChecked);
            updateMealVisibility(day, 'cena', cenaChecked);
            
            // Inicializar visibilidad de snacks
            const snackCount = parseInt(document.getElementById(`${day}_snackCount`).value);
            updateSnackVisibility(day, snackCount);
        });
    }
    
    // Añadir botones de eliminar a recetas existentes
    function addRemoveButtonsToExistingRecipes() {
        document.querySelectorAll('.recipe-item').forEach(item => {
            // Solo agregar botón si no existe ya
            if (!item.querySelector('.btn-outline-danger')) {
                const select = item.querySelector('select');
                if (select) {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'd-flex';
                    
                    select.classList.add('me-2');
                    wrapper.appendChild(select);
                    
                    const removeButton = document.createElement('button');
                    removeButton.type = 'button';
                    removeButton.className = 'btn btn-outline-danger btn-sm';
                    removeButton.innerHTML = '<i class="fas fa-times"></i>';
                    removeButton.onclick = function() {
                        removeRecipeItem(this);
                    };
                    
                    wrapper.appendChild(removeButton);
                    item.innerHTML = '';
                    item.appendChild(wrapper);
                }
            }
        });
    }
    
    // Ejecutar inicializaciones
    initializeVisibility();
    addRemoveButtonsToExistingRecipes();
});