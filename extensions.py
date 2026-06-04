from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

# Better connection handling (important for production / PostgreSQL)
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,   # checks connection before using it
    "pool_recycle": 280      # avoids timeout issues (especially on cloud DBs)
}
