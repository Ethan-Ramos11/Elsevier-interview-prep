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
        "data": [to_dict(task) for task in result]})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn, cursor = get_db_connection()
    query = "SELECT * FROM tasks where task_id = ?"
    cursor.execute(query, (task_id))
    result = cursor.fetchone()
    conn.close()
    if not result or result is None:
        return jsonify({"message": "Failed to fetch task"})
    return jsonify({
        "message": "Found task",
        "data": [to_dict(result)]
    })


@app.route('/tasks', methods=['POST'])
def create_task():
    info = request.get_json


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    pass


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    pass


@app.route('/health', methods=['GET'])
def health_check():
    pass
