from app import app
from flask import jsonify, request
from database.setup_db import create_connection, to_dict
import sqlite3


def get_db_connection():
    conn, cursor = create_connection()
    return conn, cursor


@app.route('/tasks', methods=['GET'])
@app.route('/', methods=['GET'])
def get_tasks():
    conn, cursor = get_db_connection()
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return jsonify({
        "message": "Tasks found",
        "data": [to_dict(task) for task in result]
    }), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn, cursor = get_db_connection()
    query = "SELECT * FROM tasks where task_id = ?"
    cursor.execute(query, (task_id,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        return jsonify({"message": "Failed to fetch task"}), 404
    return jsonify({
        "message": "Found task",
        "data": [to_dict(result)]
    }), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    conn, cursor = get_db_connection()
    info = request.get_json()
    if "name" not in info or not info["name"]:
        return jsonify({"message": "name is required"}), 400
    query = """
    INSERT INTO tasks (name, description, completed)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (info["name"], info.get(
        "description", ""), "incomplete"))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({
        "message": "successfully added new task",
        "task_id": task_id
    }), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    conn, cursor = get_db_connection()
    info = request.get_json()
    fields = []
    values = []

    if "name" in info:
        fields.append("name = ?")
        values.append(info["name"])
    if "description" in info:
        fields.append("description = ?")
        values.append(info["description"])
    if "completed" in info and info["completed"] in ["incomplete", "complete"]:
        fields.append("completed = ?")
        values.append(info["completed"])

    if not fields:
        conn.close()
        return jsonify({"message": "No valid fields to update"}), 400

    query = f"UPDATE tasks SET {', '.join(fields)} WHERE task_id = ?"
    values.append(task_id)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return jsonify({
        "message": "successfully updated task",
        "task_id": task_id
    }), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT task_id FROM tasks WHERE task_id = ?", (task_id, ))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return jsonify({
            "message": "task could not be found"
        }), 404
    query = "DELETE FROM tasks WHERE task_id = ?"
    cursor.execute(query, (task_id,))
    conn.commit()
    conn.close()
    return jsonify({
        "message": "successfully deleted task",
        "task_id": task_id
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn, cursor = get_db_connection()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500
