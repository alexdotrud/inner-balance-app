function openTaskModal(id, title, description) {

    const titleElement = document.getElementById('modal-title');
    const descElement = document.getElementById('taskDescription');

    if (titleElement) titleElement.textContent = title;
    if (descElement) descElement.textContent = description;

    const editLink = document.getElementById('modalEditLink');
    const deleteLink = document.getElementById('modalDeleteLink');

    // Creating a link
    if (editLink) editLink.href = `/tracker/task/${id}/edit/`;
    if (deleteLink) deleteLink.href = `/tracker/task/${id}/delete/`;

    // Shown a modal
    const modalElement = document.getElementById('taskModal');
    if (modalElement) {
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalInstance.show();
    }
}

function Motivation() {
    var checkboxes = $('.list-group-item input[type="checkbox"]');
    var totalTasks = checkboxes.length;
    var completedTasks = checkboxes.filter(':checked').length;
    var percentage = (completedTasks / totalTasks) * 100;

    var message = "";

    if (totalTasks === 0) {
        message = "📋 No tasks yet!";
    } else if (percentage === 100) {
        message = "🎉 Amazing day! All tasks done!";
    } else if (percentage >= 80) {
        message = "🔥 You're doing a good job!";
    } else if (percentage >= 50) {
        message = "💪 You're on the right way!";
    } else if (percentage >= 30) {
        message = "🏆 Push a bit harder!";
    } else if (percentage >= 10) {
        message = "⚡ You can do better!";
    } else {
        message = "😴 You haven’t done anything yet... let's start!";
    }

    $('#motivation-text').text(message);
    $('#progress-bar-fill').css('width', percentage + '%');
    $('#progress-percentage').text(Math.round(percentage) + '%');
}

$(document).ready(function () {
    Motivation();

    // Re-run every time checkbox is clicked
    $(".custom-checkbox").on("change", function () {
        Motivation();
    });

});