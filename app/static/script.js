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
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке данных.');
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
        // Проверка обязательных полей

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
