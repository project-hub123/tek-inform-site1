document.addEventListener("DOMContentLoaded", function () {

    // Поле поиска (должно быть на странице)
    const searchInput = document.getElementById("site-search");
    const searchButton = document.getElementById("search-button");

    if (!searchInput || !searchButton) {
        return; 
    }

    searchButton.addEventListener("click", function () {
        const query = searchInput.value.trim().toLowerCase();

        if (query.length < 2) {
            alert("Введите не менее 2 символов для поиска.");
            return;
        }

        performSearch(query);
    });

    // Поиск по тексту страницы
    function performSearch(query) {
        let found = false;

        // Ищем по основным текстовым элементам
        const elements = document.querySelectorAll(
            "h1, h2, h3, p, li"
        );

        elements.forEach(function (element) {
            const text = element.textContent.toLowerCase();

            // Сбрасываем предыдущую подсветку
            element.style.backgroundColor = "";

            if (text.includes(query)) {
                element.style.backgroundColor = "#fff3cd";
                found = true;
            }
        });

        if (!found) {
            alert("По вашему запросу ничего не найдено.");
        }
    }

});
