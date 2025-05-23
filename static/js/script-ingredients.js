document.addEventListener('DOMContentLoaded', function () {

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