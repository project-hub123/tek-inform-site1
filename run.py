from app import create_app

# Создание Flask-приложения
app = create_app()

if __name__ == "__main__":
    # Локальный запуск
    # debug=True используется только при локальной разработке
    app.run(host="0.0.0.0", port=5000, debug=True)
