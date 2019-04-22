function addReminder() {
    let hasAutofocus = document.getElementById('focus');
    let addReminder = document.querySelector("#add-reminderID");
    if (addReminder.classList.contains("add-task-active")) {
        addReminder.classList.add("add-task");
        addReminder.classList.remove("add-task-active");
        hasAutofocus.autofocus = false;
    }
    else if(addReminder.classList.contains("add-task")) {
        addReminder.classList.add("add-task-active");
        addReminder.classList.remove("add-task");
        hasAutofocus.focus();
        hasAutofocus.autofocus = true;
    }
}

function addTask() {
    let hasAutofocus = document.getElementById('focus');
    let addTask = document.querySelector("#add-taskID");
    if (addTask.classList.contains("add-task-active")) {
        addTask.classList.add("add-task");
        addTask.classList.remove("add-task-active");
        hasAutofocus.autofocus = false;
    }
    else if(addTask.classList.contains("add-task")) {
        addTask.classList.add("add-task-active");
        addTask.classList.remove("add-task");
        hasAutofocus.focus();
        hasAutofocus.autofocus = true;
    }
}

