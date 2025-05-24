
/*document.addEventListener('DOMContentLoaded', function () {
    let ingredientIndex = document.querySelectorAll('.ingredient-entry').length;
    const container = document.getElementById('ingredients-container');
    const addIngredientBtn = document.getElementById('add-ingredient');


    let stepCount = parseInt("{{ recipe.steps|length if recipe.steps else 0 }}");
    const stepsContainer = document.getElementById('steps-container');
    const addStepButton = document.getElementById('add-step');

    addStepButton.addEventListener('click', function () {
        stepCount++;
        const newStep = document.createElement('div');
        newStep.className = 'input-group mb-2';
        newStep.innerHTML = `
                <span class="input-group-text">${stepCount}</span>
                <input type="text" class="form-control" name="step_${stepCount}" placeholder="Paso ${stepCount}" required>
                <button type="button" class="btn btn-outline-danger remove-step">
                    <i class="bi bi-x"></i>
                </button>
            `;
        stepsContainer.appendChild(newStep);
    });

    addIngredientBtn.addEventListener('click', function () {
        const row = document.createElement('div');
        row.className = 'row mb-2 ingredient-entry';
        row.innerHTML = `
                <div class="col-md-6">
                    <select class="form-select" name="ingredient_${ingredientIndex}" required>
                        <option value="">Selecciona un ingrediente</option>
                        {% for ingredient in ingredients %}
                            <option value="{{ ingredient._id }}">{{ ingredient.name }} ({{ ingredient.unit }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <input type="text" class="form-control" name="amount_${ingredientIndex}" placeholder="Cantidad" required>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-outline-danger remove-ingredient">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            `;
        container.appendChild(row);
        ingredientIndex++;
    });

    container.addEventListener('click', function (e) {
        if (e.target.closest('.remove-ingredient')) {
            e.target.closest('.ingredient-entry').remove();
        }
    });
});
*/

document.addEventListener('DOMContentLoaded', function () {
    // 🍴 Ingredientes
    const ingredientContainer = document.getElementById('ingredients-container');
    const addIngredientBtn = document.getElementById('add-ingredient');
    const ingredientTemplate = ingredientContainer.querySelector('[data-template="ingredient"]');

    // Detecta cuántos ingredientes hay ya cargados
    let ingredientIndex = ingredientContainer.querySelectorAll('.ingredient-entry').length;

    addIngredientBtn.addEventListener('click', function () {
        const clone = ingredientTemplate.cloneNode(true);
        clone.removeAttribute('data-template');

        // Actualiza atributos name y limpia datos
        const select = clone.querySelector('select');
        const input = clone.querySelector('input');

        select.name = `ingredient_${ingredientIndex}`;
        select.selectedIndex = 0;

        input.name = `amount_${ingredientIndex}`;
        input.value = '';

        ingredientContainer.appendChild(clone);
        ingredientIndex++;
    });

    ingredientContainer.addEventListener('click', function (e) {
        if (e.target.closest('.remove-ingredient')) {
            const entry = e.target.closest('.ingredient-entry');
            if (entry && !entry.hasAttribute('data-template')) {
                entry.remove();
            }
        }
    });

    // 🥘 Pasos de preparación
    const stepsContainer = document.getElementById('steps-container');
    const addStepBtn = document.getElementById('add-step');
    const stepTemplate = stepsContainer.querySelector('[data-template="step"]');

    let stepIndex = stepsContainer.querySelectorAll('.step-entry').length + 1;

    function reindexSteps() {
        const entries = stepsContainer.querySelectorAll('.step-entry');
        entries.forEach((entry, index) => {
            const number = index + 1;
            entry.querySelector('.input-group-text').textContent = number;
            const input = entry.querySelector('input');
            input.name = `step_${number}`;
            input.placeholder = `Paso ${number}`;
        });
        stepIndex = entries.length + 1;
    }

    addStepBtn.addEventListener('click', function () {
        const clone = stepTemplate.cloneNode(true);
        clone.removeAttribute('data-template');

        clone.querySelector('.input-group-text').textContent = stepIndex;

        const input = clone.querySelector('input');
        input.name = `step_${stepIndex}`;
        input.placeholder = `Paso ${stepIndex}`;
        input.value = '';

        stepsContainer.appendChild(clone);
        stepIndex++;
    });

    
    stepsContainer.addEventListener('click', function (e) {
        if (e.target.closest('.remove-step')) {
            const entries = stepsContainer.querySelectorAll('.step-entry');
            if (entries.length > 1) {
                const entry = e.target.closest('.step-entry');
                entry.remove();
                reindexSteps();
            }
        }
    });
});