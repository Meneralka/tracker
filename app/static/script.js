document.getElementById('openModal').onclick = function() {
    document.getElementById('modal').style.display = "block";
}

document.getElementsByClassName('close-button')[0].onclick = function() {
    document.getElementById('modal').style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById('modal')) {
        document.getElementById('modal').style.display = "none";
    }
}

document.getElementById('taskModalClose').onclick = function() {
    document.getElementById('taskModal').style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById('taskModal')) {
        document.getElementById('taskModal').style.display = "none";
    }
}

const taskForms = document.querySelectorAll('.task_status');

taskForms.forEach(
    form => {
        form.onsubmit = function (event) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы
            const formData = new FormData(this);

    fetch('/change_status_task', { // Отправка на маршрут Flask
        method: 'POST',
        body: formData
    })
    .then(response => {
    if(response.ok){
    const button = form.querySelector('input[type="submit"]');
    const data = response.json()
    data.then(message => {
        console.log(message)
        if (!message.message){
            button.value = '✖';
            button.className = 'status-button incomplete';
            button.title = 'Не выполнено';
        }
        else{
            button.value = '✔' ;
            button.className = 'status-button completed';
            button.title = 'Выполнено';
        }
    })
    } else {
    if (response.status=='429'){showNotification("Слишком много попыток!", 'error');}else{
    showNotification("Произошла ошибка :(", 'error');}
    }
    });
        };
        });

document.getElementById('addSectionForm').onsubmit = function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(this);

    fetch('/section_create', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            document.getElementById('add_category').display = 'none';
            document.getElementById('new_section').setAttribute('action', 'open');
            document.getElementById('new_section').textContent = '➕ Добавить раздел';
            location.reload();
            } else {
                showNotification('Произошла ошибка', 'error');
            }})
}

document.getElementById('addTaskForm').onsubmit = function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(this);

    fetch('/task_create', { // Отправка на маршрут Flask
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('modal').style.display = "none"; // Закрываем модал после успешной отправки
        document.getElementById('addTaskForm').reset(); // Сбрасываем форму
        location.reload();
    })
    .catch((error) => {
        showNotification(error, 'error');
    });
}

function checkForm() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const submitButton = document.getElementById("submit-button");

            // Активируем кнопку, если оба поля заполнены, иначе деактивируем
            if (username && password) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }
        // Проверка обязательных полей

function checkFormAddTask() {
            const name = document.getElementById("name").value;
            const submitButton = document.getElementById("submit-button");
            if (name.length > 0) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }

function checkFormAddSection() {
            const name = document.getElementById("category").value;
            const submitButton = document.getElementById("submitAddCategory");
            if (name.length > 0) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }

function checkFormRegistration() {
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password-input").value;
            const submitButton = document.getElementById("submit-button");

            if (username && email && password) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }

        // Переключение видимости пароля
function togglePassword() {
            const passwordInput = document.getElementById("password-input");
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
            } else {
                passwordInput.type = "password";
            }
        }

// Функция для создания уведомления
function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');

    // Создаем уведомление
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Добавляем уведомление в контейнер
    container.appendChild(notification);

    // Удаляем уведомление через 5 секунд
    setTimeout(() => {
        notification.style.opacity = '0'; // Анимация исчезновения
        setTimeout(() => notification.remove(), 500); // Полное удаление
    }, 5000);
}

document.getElementById('new_section').onclick = function(event) {
    const new_section_form = document.getElementById('add_category');
    if (new_section_form.style.display === 'block') {
        new_section_form.style.display = 'none';
        document.getElementById('new_section').setAttribute('action', 'open')
        document.getElementById('new_section').textContent = '➕ Добавить раздел';
    } else {
        new_section_form.style.display = 'block';
        document.getElementById('new_section').textContent = '× Отменить';
        document.getElementById('new_section').setAttribute('action', 'close')
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const taskModal = document.getElementById('taskModal');
    const taskTitle = document.getElementById('taskTitle');
    const taskDescription = document.getElementById('taskDescription');

    // Открыть модальное окно и загрузить данные
    document.querySelectorAll('.task-card').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log(event.target.className);
            if (event.target.id === 'submit') {
                return; // Если клик был на одной из кнопок, модальное окно не открывается
            }
            const taskId = button.dataset.taskId; // Получаем ID задачи из атрибута data-task-id

            // Выполняем GET-запрос
            fetch(`/task/${taskId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка загрузки данных');
                    return response.json();
                })
                .then(data => {
                    // Заполняем модальное окно данными
                    taskTitle.textContent = data.name;
                    taskDescription.textContent = data.desc;

                    // Показываем модальное окно
                    taskModal.style.display = 'block';
                })
                .catch(error => {
                    showNotification(error, 'error')
                });
        });
    });
});

const deleteForms = document.querySelectorAll('.delete-task');

deleteForms.forEach(
    form => {
        form.onsubmit = function (event) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы
            const formData = new FormData(this);

    fetch('/delete_task', { // Отправка на маршрут Flask
        method: 'POST',
        body: formData
    })
    .then(response => {
    if(response.ok){
    const data = response.json()
    data.then(message => {
        location.reload();
    })
    } else {
    if (response.status=='429'){showNotification("Слишком много попыток!", 'error');}else{
    showNotification("Произошла ошибка :(", 'error');}
    }
    });
        };
        });
