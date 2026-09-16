import os
from datetime import datetime, timezone
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)


with app.app_context():
    db.create_all()


@app.get("/hello")
def hello():
    visit = Visit(
        visit_time=datetime.now(timezone.utc),
        ip_address=request.remote_addr or "unknown"
    )

    db.session.add(visit)
    db.session.commit()

    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)