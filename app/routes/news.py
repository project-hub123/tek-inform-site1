from flask import Blueprint, render_template

news_bp = Blueprint(
    "news",
    __name__,
    template_folder="../templates"
)

@news_bp.route("/news")
def news():
    return render_template("news.html")
