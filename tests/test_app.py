import sqlite3

import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "test.db"),
        "SEED_DATA": False,
    })
    return app.test_client()


def titles(client):
    html = client.get("/").get_data(as_text=True)
    return html


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_empty_list(client):
    assert "No tasks yet" in titles(client)


def test_add_and_list(client):
    resp = client.post("/tasks", data={"title": "Write demo notes"})
    assert resp.status_code == 302
    assert "Write demo notes" in titles(client)


def test_add_rejects_blank_title(client):
    assert client.post("/tasks", data={"title": "   "}).status_code == 400


def test_complete(client):
    client.post("/tasks", data={"title": "Finish report"})
    resp = client.post("/tasks/1/complete")
    assert resp.status_code == 302
    html = titles(client)
    assert 'class="task done"' in html


def test_delete(client):
    client.post("/tasks", data={"title": "Temporary item"})
    assert client.post("/tasks/1/delete").status_code == 302
    assert "Temporary item" not in titles(client)


def test_missing_task_returns_404(client):
    assert client.post("/tasks/999/complete").status_code == 404
    assert client.post("/tasks/999/delete").status_code == 404


def test_title_is_escaped_and_stored_as_data(client, tmp_path):
    # Parameterized queries: SQL metacharacters are stored literally.
    title = "x'); DROP TABLE tasks;--"
    client.post("/tasks", data={"title": title})
    html = titles(client)
    assert "DROP TABLE tasks" in html
    conn = sqlite3.connect(str(tmp_path / "test.db"))
    assert conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 1
    conn.close()


def test_seed_data(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "seed.db")})
    html = app.test_client().get("/").get_data(as_text=True)
    assert "Review quarterly demo checklist" in html
