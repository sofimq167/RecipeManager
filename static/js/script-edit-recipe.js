document.addEventListener('DOMContentLoaded', function () {
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