document.addEventListener('DOMContentLoaded', function () {
    let ingredientIndex = 1;
    const container = document.getElementById('ingredients-container');
    const addIngredientBtn = document.getElementById('add-ingredient');
    const template = container.querySelector('[data-template="ingredient"]');

    addIngredientBtn.addEventListener('click', function () {
        const clone = template.cloneNode(true);
        clone.removeAttribute('data-template');

        // Actualizar los atributos name en el clon
        const select = clone.querySelector('select');
        const input = clone.querySelector('input');

        select.name = `ingredient_${ingredientIndex}`;
        input.name = `amount_${ingredientIndex}`;
        input.value = "";
        select.selectedIndex = 0;

        container.appendChild(clone);
        ingredientIndex++;
    });

    container.addEventListener('click', function (e) {
        if (e.target.closest('.remove-ingredient')) {
            const entry = e.target.closest('.ingredient-entry');
            if (entry && !entry.hasAttribute('data-template')) {
                entry.remove();
            }
        }
    });


    let stepIndex = 2;
    const stepsContainer = document.getElementById('steps-container');
    const addStepBtn = document.getElementById('add-step');
    const stepTemplate = stepsContainer.querySelector('[data-template="step"]');

    addStepBtn.addEventListener('click', function () {
        const clone = stepTemplate.cloneNode(true);

        // Actualiza número del paso
        clone.querySelector('.input-group-text').textContent = stepIndex;

        // Actualiza name y placeholder del input
        const input = clone.querySelector('input');
        input.name = `step_${stepIndex}`;
        input.placeholder = `Paso ${stepIndex}`;
        input.value = '';

        stepsContainer.appendChild(clone);
        stepIndex++;
    });

});
