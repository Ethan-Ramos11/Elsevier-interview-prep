SCHEMA = {
    "tasks": {
        "columns": {
            "task_id": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "description": "TEXT",
            "completed": "TEXT CHECK(completed IN ('incomplete', 'complete'))",
        },
    },
}
