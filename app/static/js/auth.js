// ================================
// auth.js
// Клиентская проверка форм входа и регистрации
// ООО «ТЭК ИНФОРМ»
// ================================

document.addEventListener("DOMContentLoaded", function () {

    // ---------- Форма входа ----------
    const loginForm = document.querySelector("form[action*='login']");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const username = loginForm.querySelector("input[name='username']");
            const password = loginForm.querySelector("input[name='password']");

            if (!username.value.trim() || !password.value.trim()) {
                event.preventDefault();
                alert("Пожалуйста, заполните логин и пароль.");
            }
        });
    }

    // ---------- Форма регистрации ----------
    const registerForm = document.querySelector("form[action*='register']");
    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            const username = registerForm.querySelector("input[name='username']");
            const password = registerForm.querySelector("input[name='password']");

            if (!username.value.trim() || !password.value.trim()) {
                event.preventDefault();
                alert("Все поля формы должны быть заполнены.");
                return;
            }

            if (password.value.length < 4) {
                event.preventDefault();
                alert("Пароль должен содержать не менее 4 символов.");
            }
        });
    }

});
