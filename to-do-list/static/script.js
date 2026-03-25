function updateTask(taskId) {
    fetch(`/update/${taskId}`, { method: 'POST' })
        .then(() => location.reload());
}

// Notification for overdue tasks
setInterval(() => {
    const overdueTasks = document.querySelectorAll('.overdue');
    if (overdueTasks.length > 0) {
        alert("You have pending tasks to complete");
    }
}, 60000);