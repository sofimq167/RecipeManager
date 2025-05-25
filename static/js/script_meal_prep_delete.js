document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los botones de eliminar
    const deleteButtons = document.querySelectorAll('.btn-delete-meal-prep');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const mealPrepId = this.getAttribute('data-meal-prep-id');
            const mealPrepName = this.getAttribute('data-meal-prep-name');
            
            // Mostrar modal de confirmación
            showDeleteConfirmation(mealPrepId, mealPrepName);
        });
    });
});

function showDeleteConfirmation(mealPrepId, mealPrepName) {
    // Crear el modal dinámicamente
    const modalHtml = `
        <div class="modal fade" id="deleteMealPrepModal" tabindex="-1" aria-labelledby="deleteMealPrepModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title" id="deleteMealPrepModalLabel">
                            <i class="fas fa-exclamation-triangle"></i> Confirmar Eliminación
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center">
                            <i class="fas fa-trash-alt fa-3x text-danger mb-3"></i>
                            <h6>¿Estás seguro de que deseas eliminar el meal prep:</h6>
                            <p class="fw-bold text-primary">"${mealPrepName}"</p>
                            <p class="text-muted">
                                <small>Esta acción no se puede deshacer. Se eliminarán todas las comidas planificadas asociadas.</small>
                            </p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-times"></i> Cancelar
                        </button>
                        <button type="button" class="btn btn-danger" id="confirmDeleteBtn">
                            <i class="fas fa-trash"></i> Eliminar Meal Prep
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal existente si existe
    const existingModal = document.getElementById('deleteMealPrepModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Agregar el modal al DOM
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Inicializar el modal de Bootstrap
    const modal = new bootstrap.Modal(document.getElementById('deleteMealPrepModal'));
    
    // Agregar evento al botón de confirmación
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        // Redirigir a la ruta de eliminación
        window.location.href = `/meal-prep/delete/${mealPrepId}`;
    });
    
    // Mostrar el modal
    modal.show();
    
    // Limpiar el modal del DOM cuando se cierre
    document.getElementById('deleteMealPrepModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}