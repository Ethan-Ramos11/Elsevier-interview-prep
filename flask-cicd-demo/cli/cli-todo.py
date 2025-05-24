import questionary
import requests
from rich.console import Console
from rich.table import Table
import subprocess
import time
import signal
import sys
import os

API_URL = "http://127.0.0.1:5000"
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    proc = subprocess.Popen([
        sys.executable, "-m", "flask", "run", "--no-debugger", "--no-reload"
    ],
        env={**dict(os.environ), "FLASK_APP": "app",
             "FLASK_ENV": "development"},
        cwd=project_root
    )
    time.sleep(3)
    return proc


def stop_flask(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def check_flask_health():
    """Check if Flask server is responding"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        console.print(
            f"[dim]Health check response: {response.status_code}[/dim]")
        if response.status_code == 200:
            json_response = response.json()
            console.print(
                f"[dim]Health status: {json_response.get('status')}[/dim]")
            return json_response.get('status') == 'ok'
        return False
    except requests.RequestException as e:
        console.print(f"[dim]Health check error: {e}[/dim]")
        return False


def main():
    console.print("[yellow]Starting Flask server...[/yellow]")
    flask_proc = start_flask()

    max_retries = 15
    for i in range(max_retries):
        if check_flask_health():
            console.print("[green]Flask server is ready![/green]")
            break
        console.print(
            f"[yellow]Waiting for Flask server... ({i+1}/{max_retries})[/yellow]")
        time.sleep(2)
    else:
        console.print("[red]Failed to start Flask server.[/red]")
        console.print(
            "[yellow]Checking if server is accessible directly...[/yellow]")

        try:
            response = requests.get(f"{API_URL}/", timeout=5)
            console.print(
                f"[yellow]Direct connection test - Status: {response.status_code}[/yellow]")
            console.print(
                f"[yellow]Response text: {response.text[:200]}...[/yellow]")
        except Exception as e:
            console.print(f"[red]Direct connection failed: {e}[/red]")

        console.print(
            "[yellow]You can try manually accessing the server at http://127.0.0.1:5000/[/yellow]")

        continue_anyway = questionary.confirm(
            "Continue anyway? (The server might be working)").ask()
        if not continue_anyway:
            stop_flask(flask_proc)
            return

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
                try:
                    url = API_URL + "/tasks"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json().get("data", [])
                        table = format_tasks(data)
                        console.print(table)
                    else:
                        console.print(
                            f"[red]Error: {response.status_code} - {response.text}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")

            elif action == "View a task":
                task_id = questionary.text("Enter task ID:").ask()
                if not task_id or not task_id.isdigit():
                    console.print("[red]Invalid task ID[/red]")
                    continue
                try:
                    url = f"{API_URL}/tasks/{task_id}"
                    response = requests.get(url)
                    if response.status_code != 200:
                        console.print(
                            f"[red]Task not found (ID: {task_id})[/red]")
                    else:
                        data = response.json().get("data", [])
                        if data:
                            table = format_task(data[0])
                            console.print(table)
                        else:
                            console.print(
                                f"[red]No data for task {task_id}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")

            elif action == "Create a task":
                name = questionary.text("Task name:").ask()
                if not name:
                    console.print("[red]Task name is required[/red]")
                    continue
                description = questionary.text(
                    "Task description (optional):").ask()
                payload = {"name": name, "description": description}
                try:
                    response = requests.post(f"{API_URL}/tasks", json=payload)
                    if response.status_code == 201:
                        task_id = response.json().get("task_id")
                        console.print(
                            f"[green]Task created with ID: {task_id}[/green]")
                    else:
                        console.print(
                            f"[red]Failed to create task: {response.json().get('message', 'Unknown error')}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")

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
                try:
                    response = requests.put(
                        f"{API_URL}/tasks/{task_id}", json=payload)
                    if response.status_code == 200:
                        console.print(
                            f"[green]Task {task_id} updated successfully.[/green]")
                    else:
                        console.print(
                            f"[red]Failed to update task: {response.json().get('message', 'Unknown error')}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")

            elif action == "Delete a task":
                task_id = questionary.text("Enter task ID to delete:").ask()
                if not task_id or not task_id.isdigit():
                    console.print("[red]Invalid task ID[/red]")
                    continue
                confirm = questionary.confirm(
                    f"Are you sure you want to delete task {task_id}?").ask()
                if not confirm:
                    continue
                try:
                    response = requests.delete(f"{API_URL}/tasks/{task_id}")
                    if response.status_code == 200:
                        console.print(
                            f"[green]Task {task_id} deleted successfully.[/green]")
                    else:
                        console.print(
                            f"[red]Failed to delete task: {response.json().get('message', 'Unknown error')}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Request failed: {e}[/red]")

            elif action == "Health check":
                try:
                    response = requests.get(f"{API_URL}/health")
                    if response.status_code == 200 and response.json().get("status") == "ok":
                        console.print("[green]API is healthy![/green]")
                    else:
                        console.print(
                            f"[red]API health check failed: {response.json().get('details', 'Unknown error')}[/red]")
                except requests.exceptions.RequestException as e:
                    console.print(f"[red]Health check failed: {e}[/red]")

            elif action == "Exit":
                break
    finally:
        console.print("[yellow]Stopping Flask server...[/yellow]")
        stop_flask(flask_proc)
        console.print("[green]Goodbye![/green]")


if __name__ == "__main__":
    main()
