from flask import Blueprint, render_template, request

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search",
    template_folder="../templates"
)

articles_data = [
    {"id": 1, "title": "Правильный уход за коровами"},
    {"id": 2, "title": "Преимущества домашнего молока"},
    {"id": 3, "title": "Как выбрать качественный сыр"},
    {"id": 4, "title": "Разведение кур в хозяйстве"},
    {"id": 5, "title": "Преимущества натуральной продукции"},
]

products_data = [
    {"id": 1, "title": "Молоко"},
    {"id": 2, "title": "Сыр"},
    {"id": 3, "title": "Мясо"},
    {"id": 4, "title": "Яйца"},
]

news_data = [
    {"id": 1, "title": "На ферме родился телёнок"},
    {"id": 2, "title": "Начался сезон свежего молока"},
    {"id": 3, "title": "Улучшение условий содержания животных"},
]


@search_bp.route("/", methods=["GET", "POST"])
def search():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").lower().strip()

        # 1. Статьи
        for a in articles_data:
            if query in a["title"].lower():
                results.append({
                    "type": "Статья",
                    "title": a["title"],
                    "url": f"/articles/{a['id']}"
                })

        # 2. Новости
        for n in news_data:
            if query in n["title"].lower():
                results.append({
                    "type": "Новость",
                    "title": n["title"],
                    "url": f"/news/{n['id']}"
                })

        # 3. Продукция
        for p in products_data:
            if query in p["title"].lower():
                results.append({
                    "type": "Продукция",
                    "title": p["title"],
                    "url": "/products"
                })

    return render_template("search.html", query=query, results=results)
