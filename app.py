import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 1. Загружаем переменные из .env
load_dotenv()

# 2. Создаём приложение и БД
app = Flask(__name__)

# 3. Собираем строку подключения из переменных окружения (не хардкодим!)
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# 4. Модель Visit: id, время обращения, IP клиента
class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # 45 — с запасом под IPv6


# 5. Создаём таблицу visits при старте приложения
with app.app_context():
    db.create_all()


# 6. Маршрут GET /hello
@app.route("/hello", methods=["GET"])
def hello():
    # 6.1. Текущее время
    now = datetime.utcnow()

    # 6.2. IP-адрес клиента
    #      X-Forwarded-For — если приложение за прокси (в Docker часто нужно)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    # 6.3. Сохраняем запись в таблицу Visit
    visit = Visit(visited_at=now, ip_address=ip)
    db.session.add(visit)
    db.session.commit()

    # 6.4. Отвечаем 200 OK с телом «Hello»
    return "Hello", 200


# 7. Точка входа (для локального запуска; в Docker будет gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)