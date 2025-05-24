document.addEventListener('DOMContentLoaded', function () {
    const unitSelect = document.getElementById('unit');
    const referenceText = document.getElementById('unitReference');

    const references = {
        'g': 'Para gramos, la referencia nutricional es por cada 100 gramos.',
        'ml': 'Para mililitros, la referencia nutricional es por cada 100 mililitros.',
        'taza': 'Para tazas, la referencia nutricional es por 1 taza.',
        'cdta': 'Para cucharaditas, la referencia nutricional es por 1 cucharadita.',
        'cda': 'Para cucharadas, la referencia nutricional es por 1 cucharada.',
        'unidad': 'Para unidades, la referencia nutricional es por 1 unidad.'
    };

    unitSelect.addEventListener('change', function () {
        const selectedUnit = unitSelect.value;
        referenceText.textContent = references[selectedUnit] || '';
    });

    const editButtons = document.querySelectorAll('.edit-ingredient');
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const name = this.getAttribute('data-name');
            const unit = this.getAttribute('data-unit');
            const protein = this.getAttribute('data-protein');
            const carbs = this.getAttribute('data-carbs');
            const fat = this.getAttribute('data-fat');

            document.getElementById('edit_ingredient_id').value = id;
            document.getElementById('edit_name').value = name;
            document.getElementById('edit_unit').value = unit;
            document.getElementById('edit_protein').value = protein;
            document.getElementById('edit_carbs').value = carbs;
            document.getElementById('edit_fat').value = fat;
        });
    });
});