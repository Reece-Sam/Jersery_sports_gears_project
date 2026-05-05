from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Better connection handling (important for production / PostgreSQL)
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,   # checks connection before using it
    "pool_recycle": 280      # avoids timeout issues (especially on cloud DBs)
}
