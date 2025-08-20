/* global bootstrap */
/**
 * Modal opening function
 */
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

/**
 * Function that is counting success percentage and shows a motivation feedback.
 */
function Motivation() {
    const checkboxes = $('.list-group-item input[type="checkbox"]');
    const totalTasks = checkboxes.length;
    const completedTasks = checkboxes.filter(':checked').length;
    let percentage = (completedTasks / totalTasks) * 100;

    let message = "";

    if (totalTasks === 0) {
        message = "📋 No tasks yet!";
    } else if (percentage >= 100) {
        message = "🎉 Amazing day! Everything is done!";
    } else if (percentage >= 80) {
        message = "🔥 You're doing a good job!";
    } else if (percentage >= 50) {
        message = "💪 You're on the right way!";
    } else if (percentage >= 30) {
        message = "🏆 Push a bit harder!";
    } else if (percentage >= 10) {
        message = "⚡ You can do better!";
    } else if (percentage > 0) {
        message = "🌀 You have started, keep it up!";
    } else {
        message = "😴 You haven’t done anything yet... let's start!";
    }

    if (isNaN(percentage)) {
        percentage = 0;
    }

    document.getElementById('motivation-text').textContent = message;
    document.querySelector('.progress-bar-fill').style.width = percentage + '%';
    document.getElementById('progress-percentage').textContent = Math.round(percentage) + '%';
}

/**
 * Motivation function for sleep and water section. Calculates success procentage and gives feedback.
 */
function waterSleepMotivation() {
    const waterGoal = parseFloat($("#water-goal").text(), 10) || 8;
    const waterCount = parseFloat($("#water-count").text(), 10) || 0;
    let waterPercentage = waterGoal > 0 ? (waterCount / waterGoal) * 100 : 0;

    const sleepGoal = parseFloat($("#sleep-goal").text()) || 8;
    const sleepCount = parseFloat($("#sleep-input").val()) || 0;
    let sleepPercentage = sleepGoal > 0 ? (sleepCount / sleepGoal) * 100 : 0;

    function getMessage(percent) {
        if (percent >= 100) return "🎉 Perfect!";
        if (percent >= 80) return "🔥 Great job!";
        if (percent >= 50) return "💪 Keep going!";
        if (percent >= 30) return "🏃 Push harder!";
        if (percent >= 10) return "⚡ You can do better!";
        if (percent >= 0) return "🌀 Just starting...";
        return "😴 Not tracked yet.";
    }

    document.getElementById("water-motivation").textContent = getMessage(waterPercentage);
    document.getElementById("sleep-motivation").textContent = getMessage(sleepPercentage);

    document.querySelector(".water-progress-bar-fill").style.width = waterPercentage + "%";
    document.querySelector(".sleep-progress-bar-fill").style.width = sleepPercentage + "%";

    document.getElementById("water-progress-percentage").textContent = Math.round(waterPercentage) + "%";
    document.getElementById("sleep-progress-percentage").textContent = Math.round(sleepPercentage) + "%";

}

/**
 * Runs Motivation function  if chekboxes exist and every time checkbox is clicked.
 */
if (document.getElementById("task")) {
    const checkboxes = document.querySelectorAll(".custom-checkbox");
    Motivation();

    // Re-run every time a checkbox changes
    checkboxes.forEach(cb => cb.addEventListener("change", Motivation));
}

/**
 * Runs waterSleepMotivation function if goald on page exist and every time input changes.
 */
document.addEventListener("DOMContentLoaded", function () {
    const hasWaterSleep = document.getElementById("water-goal") || document.getElementById("sleep-goal");

    if (hasWaterSleep) {
        // Run once on page load
        waterSleepMotivation();

        // Optional: re-run whenever user updates inputs
        document.querySelectorAll("#sleep-input, #water-input").forEach(el => {
            el.addEventListener("input", waterSleepMotivation);
        });
    }
});

/**
 * Function is hiding and showing task list, changing the icon.
 */
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-arrow").forEach(function (toggle) {
        toggle.addEventListener("click", function () {
            const icon = this.querySelector("i");
            const taskList = this.closest("#task").querySelector(".list-group");

            if (!taskList) return;

            // Toggle based on the is-hidden class
            if (taskList.classList.contains("hidden")) {
                taskList.classList.remove("hidden"); // show
                icon.classList.remove("fa-chevron-down");
                icon.classList.add("fa-chevron-up");
            } else {
                taskList.classList.add("hidden"); // hide
                icon.classList.remove("fa-chevron-up");
                icon.classList.add("fa-chevron-down");
            }
        });
    });
});

/**
 * Changes the current progress toward goals.
 */
function updateCounter(type, delta = 0.5, min = 0, max = 20) {
    const countEl = document.getElementById(`${type}-count`);
    const inputEl = document.getElementById(`${type}-input`);
    if (!countEl || !inputEl) return;

    const current = parseFloat(inputEl.value) || 0;
    const curTenths = Math.round(current * 10);
    const delTenths = Math.round(delta * 10);
    let nextTenths = curTenths + delTenths;
    nextTenths = Math.max(min * 10, Math.min(max * 10, nextTenths));

    const next = nextTenths / 10;
    if (next !== current) {
        inputEl.value = next;
        countEl.textContent = Number.isInteger(next) ? next.toFixed(0) : next.toFixed(1);

        // enable the save button
        const btn = document.getElementById(`${type}-save-btn`);
        if (btn) {
            btn.disabled = false;
        }


        waterSleepMotivation();
    }
}


/**
 * Saves description. Changes area from textarea to paragraph.
 */
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
}

/**
 * Changes area back to textarea to allow changes.
 */
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

/**
 * Hides backgrounf image for main container on homepage.
 */
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/") {
        document.getElementById("main-container").style.backgroundImage = "none";
    }
});

/**
 * Handles avatar image preview before uploading
 */
document.addEventListener("DOMContentLoaded", function () {
    const avatarInput = document.getElementById("avatar-input");
    const avatarImage = document.getElementById("avatar-img");

    if (avatarInput && avatarImage) {
        avatarInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    avatarImage.src = e.target.result;
                    avatarImage.style.objectPosition = "center top";
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

/**
 * Enables the save button when an avatar image is selected.
 */
document.addEventListener("DOMContentLoaded", function () {
    const avatarInput = document.getElementById("avatar-input");
    const avatarBtn = document.getElementById("avatar-save-btn");

    if (avatarInput && avatarBtn) {
        avatarInput.addEventListener("change", function () {
            if (this.files && this.files.length > 0) {
                avatarBtn.disabled = false;
            }
        });
    }
});

/**
 * Runs function to open file input when avatar image is clicked.
 */
document.addEventListener('DOMContentLoaded', () => {
    const img = document.getElementById('avatar-img');
    const input = document.getElementById('avatar-input');
    if (img && input) {
        img.addEventListener('click', () => input.click());
    }
});

/**
 * Opening Instructions modal.
 */
document.addEventListener('DOMContentLoaded', () => {
    const trigger = document.getElementById('help-trigger');
    const modalElement = document.getElementById('InstModal');

    if (trigger && modalElement && window.bootstrap) {
        const instModal = new bootstrap.Modal(modalElement);

        trigger.addEventListener('click', (e) => {
            instModal.show();
        });
    }
});
/**
 * Enables the save button when water or sleep goal inputs change.
 */
document.addEventListener("DOMContentLoaded", () => {
    const goalsBtn = document.getElementById("goals-save-btn");
    document.querySelectorAll("#water_goal, #sleep_goal").forEach(input => {
        input.addEventListener("input", () => {
            goalsBtn.disabled = false;
        });
    });
});

/**
 * Hides messages after 10 seconds.
 */
$(document).ready(function () {
    $("#flash-messages .alert, .errorlist, .error-message").delay(10000).fadeOut(400);
});