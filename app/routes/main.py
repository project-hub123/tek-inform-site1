from flask import Blueprint, render_template

main_bp = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_bp.route('/')
def index():
    """
    Главная страница сайта ООО «ТЭК ИНФОРМ»
    """
    return render_template('index.html')


@main_bp.route('/about')
def about():
    """
    Страница «О компании»
    """
    return render_template('about.html')


@main_bp.route('/services')
def services():
    """
    Страница «Услуги»
    """
    return render_template('services.html')


@main_bp.route('/news')
def news():
    """
    Страница «Новости»
    """
    return render_template('news.html')


@main_bp.route('/contacts')
def contacts():
    """
    Страница «Контакты»
    """
    return render_template('contacts.html')


@main_bp.route('/sitemap')
def sitemap():
    """
    Карта сайта
    """
    return render_template('sitemap.html')
