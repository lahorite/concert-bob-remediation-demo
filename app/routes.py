from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for

from . import get_db

bp = Blueprint("tasks", __name__)

MAX_TITLE_LENGTH = 200


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.get("/")
def index():
    rows = get_db().execute(
        "SELECT id, title, completed, created_at FROM tasks ORDER BY id"
    ).fetchall()
    return render_template("index.html", tasks=rows)


@bp.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    if not title or len(title) > MAX_TITLE_LENGTH:
        abort(400, description="Title is required (max 200 characters).")
    db = get_db()
    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    return redirect(url_for("tasks.index"))


@bp.post("/tasks/<int:task_id>/complete")
def complete_task(task_id):
    db = get_db()
    cur = db.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return redirect(url_for("tasks.index"))


@bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return redirect(url_for("tasks.index"))
