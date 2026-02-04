document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const taskList = document.getElementById('taskList');

    // Load tasks on startup
    fetchTasks();

    addBtn.addEventListener('click', () => {
        const title = taskInput.value.trim();
        if (title) {
            addTask(title);
            taskInput.value = '';
        }
    });

    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addBtn.click();
        }
    });

    async function fetchTasks() {
        taskList.innerHTML = ''; // Clear list
        try {
            const res = await fetch('/api/tasks');
            const tasks = await res.json();
            tasks.forEach(renderTask);
        } catch (err) {
            console.error('Failed to fetch tasks:', err);
        }
    }

    async function addTask(title) {
        try {
            const res = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            const newTask = await res.json();
            renderTask(newTask);
        } catch (err) {
            console.error('Failed to add task:', err);
        }
    }

    async function deleteTask(id, element) {
        try {
            const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
            if (res.status === 204) {
                element.remove();
            } else {
                alert('Could not delete task');
            }
        } catch (err) {
            console.error('Failed to delete task:', err);
        }
    }

    function renderTask(task) {
        const li = document.createElement('li');
        
        const span = document.createElement('span');
        span.textContent = task.title;
        
        const btn = document.createElement('button');
        btn.textContent = 'Delete';
        btn.className = 'delete-btn';
        btn.onclick = () => deleteTask(task.id, li);

        li.appendChild(span);
        li.appendChild(btn);
        taskList.appendChild(li);
    }
});
