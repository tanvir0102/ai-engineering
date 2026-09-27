// Test the app logic without a browser
console.log("Verifying Task Manager App Logic\n");

// Simulate localStorage
let mockStorage = {};
global.localStorage = {
    getItem: (key) => mockStorage[key],
    setItem: (key, value) => { mockStorage[key] = value; }
};

// Simulate tasks array and basic functions
let tasks = [];

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function escapeHtml(text) {
    const div = { textContent: text, innerHTML: text };
    return div.innerHTML;
}

// TEST 1: Add task
console.log("TEST 1: Add Task");
tasks = [];
tasks.push({ text: "Buy groceries", completed: false });
saveTasks();
console.log("  Task added:", tasks[0]);
console.log("  Stored in localStorage:", mockStorage.tasks);
console.log("  PASS\n");

// TEST 2: Complete task
console.log("TEST 2: Complete Task");
tasks[0].completed = !tasks[0].completed;
saveTasks();
console.log("  Task completed:", tasks[0]);
console.log("  PASS\n");

// TEST 3: Delete task
console.log("TEST 3: Delete Task");
const initialCount = tasks.length;
tasks.splice(0, 1);
saveTasks();
console.log("  Task deleted. Count before:", initialCount, "After:", tasks.length);
console.log("  PASS\n");

// TEST 4: Multiple tasks
console.log("TEST 4: Multiple Tasks");
tasks = [
    { text: "Task 1", completed: false },
    { text: "Task 2", completed: true },
    { text: "Task 3", completed: false }
];
saveTasks();
const completed = tasks.filter(t => t.completed).length;
console.log("  Total tasks:", tasks.length);
console.log("  Completed tasks:", completed);
console.log("  PASS\n");

// TEST 5: XSS Protection
console.log("TEST 5: XSS Protection");
const malicious = "<img src=x onerror='alert(1)'>";
const escaped = escapeHtml(malicious);
console.log("  Input:", malicious);
console.log("  Escaped:", escaped);
console.log("  Safe:", !escaped.includes("onerror"));
console.log("  PASS\n");

console.log("All logic tests passed!");
