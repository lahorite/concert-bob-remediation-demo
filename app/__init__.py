"""Task tracker Flask application factory."""
import os
import sqlite3

from flask import Flask, current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# Synthetic demonstration data only.
SEED_TASKS = [
    "Review quarterly demo checklist",
    "Draft sample project status update",
    "Organize example meeting notes",
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with sqlite3.connect(app.config["DATABASE"]) as conn:
        conn.executescript(SCHEMA)
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0 and app.config.get("SEED_DATA", True):
            conn.executemany(
                "INSERT INTO tasks (title) VALUES (?)",
                [(t,) for t in SEED_TASKS],
            )


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.path.join(
        os.path.dirname(app.root_path), "tasks.db"
    )
    app.config["SEED_DATA"] = True
    if test_config:
        app.config.update(test_config)

    init_db(app)
    app.teardown_appcontext(close_db)

    from .routes import bp

    app.register_blueprint(bp)
    return app
