from flask import Blueprint, render_template

articles_bp = Blueprint(
    "articles",
    __name__,
    template_folder="../templates"
)

@articles_bp.route("/articles")
def articles():
    return render_template("articles.html")
