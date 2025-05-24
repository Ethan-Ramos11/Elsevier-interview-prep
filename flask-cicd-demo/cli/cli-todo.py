import questionary
import requests
from rich.console import Console
from rich.table import Table
import subprocess
import time
import signal
import sys
import os

API_URL = "http://localhost:5000"
console = Console()


def format_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Completed", style="yellow")
    for task in tasks:
        table.add_row(
            str(task["task_id"]),
            task["name"],
            task.get("description", ""),
            task["completed"]
        )
    return table


def format_task(task):
    table = Table(title=f"Task {task['task_id']}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    for key in ["task_id", "name", "description", "completed"]:
        table.add_row(key, str(task.get(key, "")))
    return table


def start_flask():
    # Start Flask app as a subprocess
    proc = subprocess.Popen([
        sys.executable, "-m", "flask", "run", "--no-debugger", "--no-reload"
    ], env={**dict(os.environ), "FLASK_APP": "app", "FLASK_ENV": "development"})
    # Wait for server to start
    time.sleep(2)
    return proc


def stop_flask(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    flask_proc = start_flask()
    try:
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "View all tasks",
                    "View a task",
                    "Create a task",
                    "Update a task",
                    "Delete a task",
                    "Health check",
                    "Exit"
                ]
            ).ask()

            if action == "View all tasks":
                url = API_URL + "/tasks"
                response = requests.get(url)
                data = response.json().get("data", [])
                table = format_tasks(data)
                console.print(table)
            elif action == "View a task":
                task_id = questionary.text("Enter task ID:").ask()
                if not task_id or not task_id.isdigit():
                    console.print("[red]Invalid task ID[/red]")
                    continue
                url = f"{API_URL}/tasks/{task_id}"
                response = requests.get(url)
                if response.status_code != 200:
                    console.print(f"[red]Task not found (ID: {task_id})[/red]")
                else:
                    data = response.json().get("data", [])
                    if data:
                        table = format_task(data[0])
                        console.print(table)
                    else:
                        console.print(f"[red]No data for task {task_id}[/red]")
            elif action == "Create a task":
                name = questionary.text("Task name:").ask()
                description = questionary.text(
                    "Task description (optional):").ask()
                payload = {"name": name, "description": description}
                response = requests.post(f"{API_URL}/tasks", json=payload)
                if response.status_code == 201:
                    task_id = response.json().get("task_id")
                    console.print(
                        f"[green]Task created with ID: {task_id}[/green]")
                else:
                    console.print(
                        f"[red]Failed to create task: {response.json().get('message', 'Unknown error')}[/red]")
            elif action == "Update a task":
                task_id = questionary.text("Enter task ID to update:").ask()
                if not task_id or not task_id.isdigit():
                    console.print("[red]Invalid task ID[/red]")
                    continue
                name = questionary.text(
                    "New name (leave blank to skip):").ask()
                description = questionary.text(
                    "New description (leave blank to skip):").ask()
                completed = questionary.select(
                    "Completed status:",
                    choices=["skip", "incomplete", "complete"]
                ).ask()
                payload = {}
                if name:
                    payload["name"] = name
                if description:
                    payload["description"] = description
                if completed != "skip":
                    payload["completed"] = completed
                if not payload:
                    console.print("[yellow]No fields to update.[/yellow]")
                    continue
                response = requests.put(
                    f"{API_URL}/tasks/{task_id}", json=payload)
                if response.status_code == 200:
                    console.print(
                        f"[green]Task {task_id} updated successfully.[/green]")
                else:
                    console.print(
                        f"[red]Failed to update task: {response.json().get('message', 'Unknown error')}[/red]")
            elif action == "Delete a task":
                task_id = questionary.text("Enter task ID to delete:").ask()
                if not task_id or not task_id.isdigit():
                    console.print("[red]Invalid task ID[/red]")
                    continue
                confirm = questionary.confirm(
                    f"Are you sure you want to delete task {task_id}?").ask()
                if not confirm:
                    continue
                response = requests.delete(f"{API_URL}/tasks/{task_id}")
                if response.status_code == 200:
                    console.print(
                        f"[green]Task {task_id} deleted successfully.[/green]")
                else:
                    console.print(
                        f"[red]Failed to delete task: {response.json().get('message', 'Unknown error')}[/red]")
            elif action == "Health check":
                response = requests.get(f"{API_URL}/health")
                if response.status_code == 200 and response.json().get("status") == "ok":
                    console.print("[green]API is healthy![/green]")
                else:
                    console.print(
                        f"[red]API health check failed: {response.json().get('details', 'Unknown error')}[/red]")
            elif action == "Exit":
                break
    finally:
        stop_flask(flask_proc)


if __name__ == "__main__":
    main()
