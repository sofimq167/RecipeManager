document.addEventListener('DOMContentLoaded', function () {
    // Ingredientes
    const ingredientContainer = document.getElementById('ingredients-container');
    const addIngredientBtn = document.getElementById('add-ingredient');
    const ingredientTemplate = ingredientContainer.querySelector('[data-template="ingredient"]');

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

    // Pasos de preparación
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