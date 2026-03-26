const API_URL = 'http://127.0.0.1:5000';

// DOM Elements
const loginSection = document.getElementById('login-section');
const dashboardSection = document.getElementById('dashboard-section');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const taskBoard = document.getElementById('task-board');
const userRoleDisplay = document.getElementById('user-role');

// Check if user is already logged in on page load
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showDashboard();
    }
});

// Login Logic
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginError.textContent = '';
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const originalText = loginBtn.innerHTML;
    loginBtn.innerHTML = '<span>Loading...</span>';

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            showDashboard();
        } else {
            loginError.textContent = data.message || 'Login failed!';
        }
    } catch (error) {
        loginError.textContent = 'Server is not running or CORS error!';
        console.error(error);
    } finally {
        loginBtn.innerHTML = originalText;
    }
});

// Logout Logic
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    loginSection.style.display = 'flex';
    dashboardSection.style.display = 'none';
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
});

// Show Dashboard & Fetch Tasks
async function showDashboard() {
    loginSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    
    const role = localStorage.getItem('role');
    userRoleDisplay.textContent = `Role: ${role}`;
    
    await fetchTasks();
}

// Fetch Tasks Logic
async function fetchTasks() {
    const token = localStorage.getItem('token');
    taskBoard.innerHTML = '<p style="color: #9ca3af; text-align:center; width: 100%;">Loading tasks...</p>';

    try {
        const response = await fetch(`${API_URL}/dashboard`, {
            method: 'GET',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            }
        });

        if (response.status === 401) {
            logoutBtn.click(); // Token expired
            return;
        }

        const tasks = await response.json();
        
        if (tasks.length === 0) {
            taskBoard.innerHTML = '<p style="color: #9ca3af; text-align:center; width: 100%;">No tasks found! 🎉</p>';
            return;
        }

        taskBoard.innerHTML = '';
        tasks.forEach((task, index) => {
            // Delaying animation for each card slightly
            const animDelay = index * 0.1;
            
            // Map status to CSS classes
            let statusClass = 'status-pending';
            if (task.status === 'in progress') statusClass = 'status-inprogress';
            if (task.status === 'completed') statusClass = 'status-completed';

            const card = document.createElement('div');
            card.className = 'glass-card task-card slide-up';
            card.style.animationDelay = `${animDelay}s`;
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <h3 class="task-title">${task.title}</h3>
                    <span class="status-indicator ${statusClass}">${task.status}</span>
                </div>
                <p class="task-desc">${task.description}</p>
                <div class="task-footer">
                    <span>ID: ${task.uuid.split('-')[0]}</span>
                    <span>Assignee: ${task.assigned_to}</span>
                </div>
            `;
            taskBoard.appendChild(card);
        });

    } catch (error) {
        taskBoard.innerHTML = '<p class="error-text">Failed to fetch tasks.</p>';
        console.error(error);
    }
}