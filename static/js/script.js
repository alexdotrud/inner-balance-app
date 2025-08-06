function openTaskModal(id, title, description) {
    document.getElementById('taskModalLabel').textContent = title;
    document.getElementById('taskModalDescription').textContent = description;
    let modal = new bootstrap.Modal(document.getElementById('taskModal'));
    modal.show();
}