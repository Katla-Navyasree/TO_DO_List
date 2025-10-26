// Simple To-Do web app (localStorage with JSON export/import)
const STORAGE_KEY = "todo_data_v1";
let tasks = [];
let lists = ["Tasks","Personal","Work","Shopping"];
let currentList = "Tasks";
let editingIndex = null;
const listSelect = document.getElementById("listSelect");
const addListBtn = document.getElementById("addListBtn");
const taskText = document.getElementById("taskText");
const dueDate = document.getElementById("dueDate");
const priority = document.getElementById("priority");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");
const tasksContainer = document.getElementById("tasksContainer");
const themeToggle = document.getElementById("themeToggle");
const exportBtn = document.getElementById("exportBtn");
const importBtn = document.getElementById("importBtn");
const appRoot = document.getElementById("app");
const listsCount = document.getElementById("listsCount");
function nowISO(){ return new Date().toISOString(); }
function loadData(){
const raw = localStorage.getItem(STORAGE_KEY);
if(raw){
try{
const data = JSON.parse(raw);
tasks = (data.tasks || []).map(t=>{
if(t.due_date) t.due_date = t.due_date; // keep ISO yyyy-mm-dd
if (!t.priority) t.priority = "medium";
if (!t.list) t.list = "Tasks";
if (!t._id) t._id = generateId();
return t;
});
lists = data.lists || ["Tasks","Personal","Work","Shopping"];
}catch(e){
tasks = [];
lists = ["Tasks","Personal","Work","Shopping"];
}
}else{
// Seed sample if desired (comment out)
// tasks = [{
// task:"Welcome! This is a sample task",
// completed:false,
// due_date:null,
// created_at: nowISO(),
// priority:"medium",
// list:"Tasks"
// }];
}
updateListsFromTasks();
}
function saveData(){
const data = {tasks, lists};
localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
function updateListsFromTasks(){
tasks.forEach(t=>{
if(t.list && !lists.includes(t.list)) lists.push(t.list);
});
}
function renderLists(){
listSelect.innerHTML = "";
lists.forEach(l=>{
const opt = document.createElement("option");
opt.value = l;
opt.textContent = l;
listSelect.appendChild(opt);
});
listSelect.value = currentList;
listsCount.textContent = `${lists.length} lists`;
}
function renderTasks(){
tasksContainer.innerHTML = "";
const filtered = tasks.filter(t => (t.list || "Tasks") === currentList);
if(filtered.length === 0){
const el = document.createElement("div");
el.className = "empty";
el.style.padding = "40px";
el.style.color = getComputedStyle(document.body).getPropertyValue("--muted");
el.textContent = "No tasks in this list";
tasksContainer.appendChild(el);
return;
}
filtered.forEach((task, idx)=>{
const card = document.createElement("div");
card.className = "task-card";
const top = document.createElement("div");
top.className = "task-top";
const checkbox = document.createElement("input");
checkbox.type = "checkbox";
checkbox.checked = !!task.completed;
checkbox.addEventListener("change", ()=>{ toggleCompletion(task); });
const text = document.createElement("div");
text.className = "text" + (task.completed ? " completed" : "");
text.textContent = task.task;
const actions = document.createElement("div");
actions.className = "task-actions";
const editBtn = document.createElement("button");
editBtn.className = "icon";
editBtn.title = "Edit";
editBtn.textContent = "✏️";
editBtn.onclick = ()=> startEdit(task);
const delBtn = document.createElement("button");
delBtn.className = "icon";
delBtn.title = "Delete";
delBtn.textContent = "🗑️";
delBtn.onclick = ()=> deleteTask(task);
actions.appendChild(editBtn);
actions.appendChild(delBtn);
top.appendChild(checkbox);
top.appendChild(text);
top.appendChild(actions);
card.appendChild(top);
// details
const details = document.createElement("div");
details.className = "task-details";
if(task.due_date){
const dueEl = document.createElement("div");
const dueDateVal = new Date(task.due_date + "T00:00:00");
const today = new Date(); today.setHours(0,0,0,0);
let dueText = `Due: ${task.due_date}`;
if(!task.completed && dueDateVal < today){
dueEl.className = "overdue";
}else{
dueEl.style.color = getComputedStyle(document.body).getPropertyValue("--muted");
}
dueEl.textContent = dueText;
details.appendChild(dueEl);
}
if(task.priority && task.priority !== "medium"){
const p = document.createElement("div");
p.className = `priority-${task.priority}`;
p.textContent = `Priority: ${task.priority}`;
details.appendChild(p);
}
card.appendChild(details);
tasksContainer.appendChild(card);
});
}
function resetForm(){
taskText.value = "";
dueDate.value = "";
priority.value = "medium";
editingIndex = null;
saveBtn.textContent = "Save";
}
function saveNewTask(){
const text = taskText.value.trim();
if(!text){
alert("Task cannot be empty!");
return;
}
const due = dueDate.value || null;
const pr = priority.value || "medium";
if(editingIndex !== null){
// find task object by reference and update
const t = tasks.find(tk => tk._id === editingIndex);
if(t){
t.task = text;
t.due_date = due;
t.priority = pr;
t.list = currentList;
}
editingIndex = null;
} else {
const newTask = {
_id: generateId(),
task: text,
completed: false,
due_date: due,
created_at: nowISO(),
priority: pr,
list: currentList
};
tasks.push(newTask);
}
saveData();
renderLists();
renderTasks();
resetForm();
}
function generateId(){
return 't_' + Math.random().toString(36).slice(2,9);
}
function toggleCompletion(task){
task.completed = !task.completed;
saveData();
renderTasks();
}
function startEdit(task){
editingIndex = task._id;
taskText.value = task.task;
dueDate.value = task.due_date || "";
priority.value = task.priority || "medium";
saveBtn.textContent = "Update";
window.scrollTo({top:0,behavior:"smooth"});
}
function deleteTask(task){
if(!confirm(`Delete "${task.task}"?`)) return;
tasks = tasks.filter(t => t._id !== task._id);
saveData();
renderLists();
renderTasks();
}
function addNewList(){
const name = prompt("Enter new list name:");
if(name && !lists.includes(name)){
lists.push(name);
currentList = name;
renderLists();
renderTasks();
} else if (lists.includes(name)){
alert("List already exists");
}
}
function exportTasksJSON(){
const data = JSON.stringify({tasks, lists}, null, 2);
// download as file
const blob = new Blob([data], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'data.json';
a.click();
URL.revokeObjectURL(url);
}
function importData(){
const input = document.createElement('input');
input.type = 'file';
input.accept = '.json';
input.onchange = (e) => {
const file = e.target.files[0];
if(file){
const reader = new FileReader();
reader.onload = (e) => {
try{
const data = JSON.parse(e.target.result);
tasks = (data.tasks || []).map(t=>{
if(t.due_date) t.due_date = t.due_date;
if (!t.priority) t.priority = "medium";
if (!t.list) t.list = "Tasks";
if (!t._id) t._id = generateId();
return t;
});
lists = data.lists || ["Tasks","Personal","Work","Shopping"];
saveData();
renderLists();
renderTasks();
alert("Data imported successfully!");
}catch(err){
alert("Invalid JSON file!");
}
};
reader.readAsText(file);
}
};
input.click();
}
function toggleTheme(){
if(appRoot.classList.contains("light")){
appRoot.classList.remove("light"); appRoot.classList.add("dark");
themeToggle.textContent = "☀️";
localStorage.setItem("todo_theme","dark");
} else {
appRoot.classList.remove("dark"); appRoot.classList.add("light");
themeToggle.textContent = "🌙";
localStorage.setItem("todo_theme","light");
}
}
function loadTheme(){
const t = localStorage.getItem("todo_theme") || "light";
if(t === "dark"){
appRoot.classList.remove("light"); appRoot.classList.add("dark"); themeToggle.textContent =
"☀️";
} else {
appRoot.classList.remove("dark"); appRoot.classList.add("light"); themeToggle.textContent =
"🌙";
}
}
// events
listSelect.addEventListener("change", e=>{
currentList = e.target.value;
renderTasks();
});
addListBtn.addEventListener("click", addNewList);
saveBtn.addEventListener("click", saveNewTask);
cancelBtn.addEventListener("click", resetForm);
themeToggle.addEventListener("click", toggleTheme);
exportBtn.addEventListener("click", exportTasksJSON);
importBtn.addEventListener("click", importData);
// init
loadData();
loadTheme();
renderLists();
renderTasks();
