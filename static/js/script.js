const isLoggedIn = "{{ user.is_authenticated|yesno:'true,false' }}" === "true";
const LoggedParagraph = document.getElementById("sign-p")
const LoggedHeading = document.getElementById("sign-h")

if (isLoggedIn) {
    if (LoggedParagraph) {
        LoggedParagraph.style.display = "none";
    }
    if (LoggedHeading) {
        LoggedHeading.style.display = "none";
    }
}

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

    if (isNaN(percentage)) {
        percentage = 0;
    }

    $('#motivation-text').text(message);
    $('.progress-bar-fill').css('width', percentage + '%');
    $('#progress-percentage').text(Math.round(percentage) + '%');
}

function waterSleepMotivation() {
    const waterGoal = parseInt($("#water-goal").text(), 10) || 0;
    const waterCount = parseInt($("#water-count").text(), 10) || 0;
    let waterPercentage = waterGoal > 0 ? (waterCount / waterGoal) * 100 : 0;

    const sleepGoal = parseFloat($("#sleep-input").attr("max")) || 8;
    const sleepCount = parseFloat($("#sleep-input").val()) || 0;
    let sleepPercentage = sleepGoal > 0 ? (sleepCount / sleepGoal) * 100 : 0;

    function getMessage(percent) {
        if (percent === 100) return "🎉 Perfect!";
        if (percent >= 80) return "🔥 Great job!";
        if (percent >= 50) return "💪 Keep going!";
        if (percent >= 30) return "🏃 Push harder!";
        if (percent >= 10) return "🌀 Just starting...";
        return "😴 Not tracked yet.";
    }

    $("#water-motivation").text(getMessage(waterPercentage));
    $("#sleep-motivation").text(getMessage(sleepPercentage));

    $(".water-progress-bar-fill").css("width", waterPercentage + "%");
    $(".sleep-progress-bar-fill").css("width", sleepPercentage + "%");

    $("#water-progress-percentage").text(Math.round(waterPercentage) + "%");
    $("#sleep-progress-percentage").text(Math.round(sleepPercentage) + "%");

}

$(document).ready(function () {
    Motivation();

    // Re-run every time checkbox is clicked
    $(".custom-checkbox").on("change", function () {
        Motivation();
    });

});

$(document).ready(function () {
    waterSleepMotivation();
});

$(document).ready(function () {
    $('.toggle-arrow').on('click', function () {
        const icon = $(this).find('i');
        const taskList = $('.list-group');

        // Opens and Closes Task List
        taskList.slideToggle(200);

        // Changing icons class
        if (icon.hasClass('fa-chevron-down')) {
            icon.removeClass('fa-chevron-down').addClass('fa-chevron-up');
        } else {
            icon.removeClass('fa-chevron-up').addClass('fa-chevron-down');
        }
    });
});

function updateWater(change) {
    const countElem = document.getElementById('water-count');
    const inputElem = document.getElementById('water-input');

    let count = parseInt(countElem.textContent) || 0;
    count += change;

    // Prevent negative count
    if (count < 0) count = 0;

    countElem.textContent = count;
    inputElem.value = count;
}

function saveDescription(e) {
    const editBtn = document.getElementById("desc-edit");
    const textarea = document.getElementById("description");
    const paragraph = document.getElementById("description-text");
    const saveBtn = document.getElementById("description-button");

    // Hide textarea + save if description already exists
    if (paragraph.textContent.trim() !== "") {
        textarea.classList.add("is-hidden");
        saveBtn.classList.add("is-hidden");
    } else {
        paragraph.classList.add("is-hidden");
        editBtn.classList.add("is-hidden");
    }

    editBtn.addEventListener("click", () => {
        textarea.classList.remove("is-hidden");
        saveBtn.classList.remove("is-hidden");
        paragraph.classList.add("is-hidden");
        editBtn.classList.add("is-hidden");
    });
};

function editDescription() {
    const para = document.getElementById("description-text");
    const editBtn = document.getElementById("desc-edit");
    if (!para || !editBtn) return;

    para.style.display = "none";
    editBtn.style.display = "none";

    para.insertAdjacentHTML("afterend", `
    <textarea id="description" name="description" rows="4" maxlength="500">${para.textContent.trim()}</textarea>
    <button type="submit" id="description-button" class="custom-btn btn-add">Save</button>
  `);
}