"use strict";

let todolist = [];

function renderTodo(task) {
    localStorage.setItem('myTasks', JSON.stringify(todolist));
    const list_todo = document.querySelector('.list #to-do');
    const list_done = document.querySelector('.list #done');
    const exists_in_done = document.querySelector(`.list #done [data-key='${task.id}']`);
    const exists_in_todo = document.querySelector(`.list #to-do [data-key='${task.id}']`);
    const node= document.createElement("div");
    node.setAttribute('data-key',task.id);

    if (task.checked === false){
        node.setAttribute('class','to-do-item');
        node.innerHTML = `
            <label>
                <input type="checkbox" class="check-to-do" id="${task.id}">
                <span class="circle ${task.category}"></span>
            </label>
            <div class="to-do-content">
                <input type="text" value="${task.text}">
            </div>
            <div class="actions">
                <button class="delete" id="${task.id}">Delete</button>
            </div>
        `;
        if (exists_in_done){
            exists_in_done.remove();
        }
        list_todo.append(node);
    } else {
        node.setAttribute('class','done-item');
        node.innerHTML = `
            <label>
                <input type="checkbox" class="check-done" id="${task.id}">
                <span class="circle ${task.category}"></span>
            </label>
            <div class="done-content">
                <input type="text" value="${task.text}">
            </div>
            <div class="actions">
                <button class="delete" id="${task.id}">Delete</button>
            </div>
        `;
        if (exists_in_todo){
            exists_in_todo.remove();
        }
        list_done.append(node)
    }
}

function deleteTask(key) {
    const element = document.querySelector(`[data-key='${key}']`);
    let notification = new Notification('Task has been deleted!');
    setTimeout(() => {
        notification.close();
    }, 10 * 100);
    todolist = todolist.filter(item => item.id !== Number(key));
    element.remove();
    localStorage.setItem('myTasks', JSON.stringify(todolist));

}

function AddToDo (text,category) {
    const todo = {
        text,
        category,
        checked: false,
        id: Date.now(),
    };

    todolist.push(todo);
    renderTodo(todo);
    let notification = new Notification('New task added!');
    setTimeout(() => {
        notification.close();
    }, 10 * 100);
}

function toggleDone(key) {
    const index = todolist.findIndex(item => item.id === Number(key));
    todolist[index].checked = !todolist[index].checked;
    renderTodo(todolist[index]);
}

const form = document.querySelector('#new-task-form');

form.addEventListener('submit', event => {
    event.preventDefault();

    const userinput = document.querySelector('#task');
    const text = userinput.value.trim();

    const categories = document.getElementsByName("category");
    let category = '';
    for (let i=0; i<categories.length; i++) {
        if(categories[i].checked) category = categories[i].value;
        categories[i].checked = false;
    }
    if (text !== '') {
        AddToDo(text,category);
        userinput.value = '';
        userinput.focus();
    }

    let deletions = document.getElementsByClassName("delete");
    for (let i=0; i<deletions.length; i++){
        deletions[i].onclick = function(e){
            deleteTask(this.id)
       }
    };
});

const list = document.querySelector('.list');
list.addEventListener('click', event => {
    const circles1 = document.getElementsByClassName("check-to-do");
    for (let i=0; i<circles1.length; i++) {
        if(circles1[i].checked) {
            let task_id = circles1[i].id;
            console.log(circles1[i].id);
            toggleDone(task_id);
            let notification = new Notification('Task done!');
            setTimeout(() => {
                notification.close();
            }, 10 * 100);
        };
    };
    const circles2 = document.getElementsByClassName("check-done");
    for (let i=0; i<circles2.length; i++) {
        if(circles2[i].checked) {
            let task_id = circles2[i].id;
            toggleDone(task_id);
            let notification = new Notification('Redo Task!');
            setTimeout(() => {
                notification.close();
            }, 10 * 100);
        };
    };

    let deletions = document.getElementsByClassName("delete");
    for (let i=0; i<deletions.length; i++){
        deletions[i].onclick = function(e){
            deleteTask(this.id)
       }
    };
});

document.addEventListener('DOMContentLoaded', () => {
    const ref = localStorage.getItem('myTasks');
    if (ref) {
      todolist = JSON.parse(ref);
      todolist.forEach(task => {
        renderTodo(task);
      });
    }
});