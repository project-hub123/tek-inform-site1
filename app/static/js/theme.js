function enableAccessible() {
    document.getElementById("theme-style").href =
        "/static/css/accessible.css";
    localStorage.setItem("theme", "accessible");
}

function disableAccessible() {
    document.getElementById("theme-style").href =
        "/static/css/style.css";
    localStorage.setItem("theme", "default");
}

// Запоминаем выбор
document.addEventListener("DOMContentLoaded", function () {
    const theme = localStorage.getItem("theme");
    if (theme === "accessible") {
        enableAccessible();
    }
});
